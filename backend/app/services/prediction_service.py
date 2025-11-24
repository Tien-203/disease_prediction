"""Prediction service for disease prediction"""
from typing import List, Optional
from sqlalchemy.orm import Session
from loguru import logger

from app.models.prediction import Prediction
from app.models.disease import Disease
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    AlternativePrediction,
    PredictionHistoryResponse
)
from app.ml.model_loader import model_loader
from app.ml.predictor import DiseasePredictor


class PredictionService:
    """Service for handling disease predictions"""
    
    def __init__(self, db: Session):
        self.db = db
        self.predictor = DiseasePredictor(model_loader)
    
    def predict_disease(
        self,
        request: PredictionRequest,
        user_id: Optional[int] = None
    ) -> PredictionResponse:
        """
        Predict disease based on symptoms
        
        Args:
            request: Prediction request with symptoms
            
        Returns:
            PredictionResponse with prediction results
        """
        # Remove duplicates from symptoms list and normalize
        unique_symptoms = list(dict.fromkeys(request.symptoms))  # Preserves order while removing duplicates
        logger.info(f"Received {len(request.symptoms)} symptoms, {len(unique_symptoms)} unique")
        
        # Make prediction with unique symptoms
        predicted_disease, confidence, alternatives = self.predictor.predict(unique_symptoms)
        
        # Get disease information from database
        disease_info = None
        disease_record = self.db.query(Disease).filter(
            Disease.name.ilike(predicted_disease)
        ).first()
        
        if disease_record:
            disease_info = {
                "description": disease_record.description,
                "severity": disease_record.severity,
                "precautions": disease_record.precautions,
                "recommendations": disease_record.recommendations
            }
        
        # Save prediction to database (use unique symptoms)
        prediction_record = Prediction(
            user_id=user_id,  # Can be None for anonymous predictions
            symptoms=unique_symptoms,  # Use unique symptoms
            predicted_disease=predicted_disease,
            confidence=confidence,
            session_id=request.session_id
        )
        self.db.add(prediction_record)
        self.db.commit()
        
        logger.info(f"Prediction saved with ID: {prediction_record.id}")
        
        # Prepare response
        alternative_predictions = [
            AlternativePrediction(disease=disease, confidence=conf)
            for disease, conf in alternatives
        ]
        
        return PredictionResponse(
            predicted_disease=predicted_disease,
            confidence=confidence,
            alternatives=alternative_predictions,
            symptoms_used=unique_symptoms,  # Return unique symptoms
            disease_info=disease_info
        )
    
    def get_prediction_history(
        self,
        skip: int = 0,
        limit: int = 100,
        session_id: Optional[str] = None
    ) -> List[PredictionHistoryResponse]:
        """
        Get prediction history
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            session_id: Optional session ID filter
            
        Returns:
            List of prediction history records
        """
        query = self.db.query(Prediction)
        
        if session_id:
            query = query.filter(Prediction.session_id == session_id)
        
        predictions = query.order_by(
            Prediction.timestamp.desc()
        ).offset(skip).limit(limit).all()
        
        return [
            PredictionHistoryResponse.model_validate(pred)
            for pred in predictions
        ]
    
    def get_prediction_by_id(self, prediction_id: int) -> Optional[PredictionHistoryResponse]:
        """
        Get prediction by ID
        
        Args:
            prediction_id: Prediction ID
            
        Returns:
            Prediction record or None
        """
        prediction = self.db.query(Prediction).filter(
            Prediction.id == prediction_id
        ).first()
        
        if prediction:
            return PredictionHistoryResponse.model_validate(prediction)
        return None

