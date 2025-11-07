"""Prediction endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    PredictionHistoryResponse,
    PredictionHistoryListResponse
)
from app.services.prediction_service import PredictionService
from app.ml.model_loader import model_loader

router = APIRouter()


@router.post("", response_model=PredictionResponse)
def predict_disease(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict disease based on symptoms
    
    Args:
        request: Prediction request with symptoms list
        
    Returns:
        Prediction result with disease name, confidence, and alternatives
    """
    # Check if ML model is loaded
    if not model_loader.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not loaded. Please train the model first."
        )
    
    # Validate symptoms
    if not request.symptoms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one symptom is required"
        )
    
    try:
        service = PredictionService(db)
        prediction = service.predict_disease(request)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making prediction: {str(e)}"
        )


@router.get("/history", response_model=PredictionHistoryListResponse)
def get_prediction_history(
    skip: int = 0,
    limit: int = 100,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get prediction history
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        session_id: Optional session ID filter
    """
    service = PredictionService(db)
    predictions = service.get_prediction_history(
        skip=skip,
        limit=limit,
        session_id=session_id
    )
    
    return PredictionHistoryListResponse(
        predictions=predictions,
        total=len(predictions)
    )


@router.get("/{prediction_id}", response_model=PredictionHistoryResponse)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    """
    Get prediction by ID
    
    Args:
        prediction_id: Prediction ID
    """
    service = PredictionService(db)
    prediction = service.get_prediction_by_id(prediction_id)
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction with ID {prediction_id} not found"
        )
    
    return prediction

