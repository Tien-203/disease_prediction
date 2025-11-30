"""Prediction endpoints"""
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from loguru import logger

from app.api.deps import get_db, get_current_user_optional, get_current_user
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    PredictionHistoryResponse,
    PredictionHistoryListResponse,
    PredictionUpdateRequest,
    PatientPredictionResponse
)
from app.services.prediction_service import PredictionService
from app.ml.model_loader import model_loader
from app.models.user import User

router = APIRouter()


@router.post("", response_model=PredictionResponse)
def predict_disease(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
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
        # Get user_id if user is authenticated, otherwise None
        user_id = current_user.id if current_user else None
        prediction = service.predict_disease(request, user_id=user_id)
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error making prediction: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making prediction: {str(e)}"
        )


@router.get("/history", response_model=PredictionHistoryListResponse)
def get_prediction_history(
    skip: int = 0,
    limit: int = 100,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    Get prediction history
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        session_id: Optional session ID filter
        current_user: Current authenticated user (optional)
    """
    try:
        service = PredictionService(db)
        # Get user_id if user is authenticated, otherwise None
        user_id = current_user.id if current_user else None
        predictions = service.get_prediction_history(
            skip=skip,
            limit=limit,
            session_id=session_id,
            user_id=user_id
        )
        
        return PredictionHistoryListResponse(
            predictions=predictions,
            total=len(predictions)
        )
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting prediction history: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting prediction history: {str(e)}"
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
    try:
        service = PredictionService(db)
        prediction = service.get_prediction_by_id(prediction_id)
        
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID {prediction_id} not found"
            )
        
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting prediction by ID {prediction_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting prediction: {str(e)}"
        )


@router.get("/patients/all", response_model=List[PatientPredictionResponse])
def get_all_patient_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all patient predictions with user info (for doctors and researchers)
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user (must be doctor or researcher)
    """
    # Check if user is a doctor or researcher
    if current_user.role not in ['doctor', 'researcher']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors and researchers can access patient predictions"
        )
    
    try:
        service = PredictionService(db)
        predictions = service.get_all_predictions_with_users(
            skip=skip,
            limit=limit
        )
        return predictions
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting patient predictions: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting patient predictions: {str(e)}"
        )


@router.put("/{prediction_id}/correct", response_model=PredictionHistoryResponse)
def correct_prediction(
    prediction_id: int,
    request: PredictionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Correct/update prediction with actual disease (for doctors and researchers)
    
    Args:
        prediction_id: Prediction ID
        request: Update request with corrected disease
        current_user: Current authenticated user (must be doctor or researcher)
    """
    # Check if user is a doctor or researcher
    if current_user.role not in ['doctor', 'researcher']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors and researchers can correct predictions"
        )
    
    try:
        service = PredictionService(db)
        prediction = service.update_prediction(
            prediction_id=prediction_id,
            corrected_disease=request.corrected_disease
        )
        
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID {prediction_id} not found"
            )
        
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error correcting prediction {prediction_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error correcting prediction: {str(e)}"
        )

