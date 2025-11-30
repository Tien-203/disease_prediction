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
    PredictionHistoryResponse,
    PatientPredictionResponse
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
        session_id: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> List[PredictionHistoryResponse]:
        """
        Get prediction history
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            session_id: Optional session ID filter
            user_id: Optional user ID filter (filters by current user)
            
        Returns:
            List of prediction history records
        """
        query = self.db.query(Prediction)
        
        # Filter by user_id if provided (for authenticated users)
        if user_id is not None:
            query = query.filter(Prediction.user_id == user_id)
        
        # Filter by session_id if provided (for anonymous users)
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
    
    def get_all_predictions_with_users(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[PatientPredictionResponse]:
        """
        Get all predictions with user information (for doctors)
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of predictions with user info
        """
        from sqlalchemy.orm import joinedload
        
        # Use joinedload to eagerly load user relationship
        predictions = self.db.query(Prediction).options(
            joinedload(Prediction.user)
        ).order_by(
            Prediction.timestamp.desc()
        ).offset(skip).limit(limit).all()
        
        from app.models.disease import Disease
        
        result = []
        for pred in predictions:
            user = pred.user if pred.user_id else None
            
            # Get recommendation from disease table based on predicted_disease or corrected_disease
            disease_name = pred.corrected_disease if pred.corrected_disease else pred.predicted_disease
            recommendation = None
            if disease_name:
                disease = self.db.query(Disease).filter(
                    Disease.name.ilike(disease_name.strip())
                ).first()
                if disease and disease.recommendations:
                    recommendation = disease.recommendations
            
            result.append(PatientPredictionResponse(
                id=pred.id,
                user_id=pred.user_id,
                user_name=user.name if user else None,
                user_age=user.age if user else None,
                user_gender=user.gender if user else None,
                symptoms=pred.symptoms,
                predicted_disease=pred.predicted_disease,
                confidence=pred.confidence,
                timestamp=pred.timestamp,
                corrected_disease=pred.corrected_disease,
                recommendation=recommendation
            ))
        
        return result
    
    def update_prediction(
        self,
        prediction_id: int,
        corrected_disease: str
    ) -> Optional[PredictionHistoryResponse]:
        """
        Update prediction with corrected disease
        
        Args:
            prediction_id: Prediction ID
            corrected_disease: Corrected/actual disease name
            
        Returns:
            Updated prediction record or None
        """
        prediction = self.db.query(Prediction).filter(
            Prediction.id == prediction_id
        ).first()
        
        if not prediction:
            return None
        
        prediction.corrected_disease = corrected_disease
        self.db.commit()
        self.db.refresh(prediction)
        
        return PredictionHistoryResponse.model_validate(prediction)

