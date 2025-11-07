"""Prediction schemas"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Schema for prediction request"""
    symptoms: List[str] = Field(
        ...,
        min_length=1,
        description="List of symptom names for prediction"
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for tracking"
    )


class AlternativePrediction(BaseModel):
    """Schema for alternative prediction"""
    disease: str = Field(..., description="Disease name")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence (0-1)")


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    predicted_disease: str = Field(..., description="Predicted disease name")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence (0-1)")
    alternatives: List[AlternativePrediction] = Field(
        default_factory=list,
        description="Alternative predictions with lower confidence"
    )
    symptoms_used: List[str] = Field(..., description="Symptoms used for prediction")
    disease_info: Optional[dict] = Field(None, description="Additional disease information")


class PredictionHistoryResponse(BaseModel):
    """Schema for prediction history response"""
    id: int
    symptoms: List[str]
    predicted_disease: str
    confidence: float
    timestamp: datetime
    session_id: Optional[str]
    
    class Config:
        from_attributes = True


class PredictionHistoryListResponse(BaseModel):
    """Schema for list of prediction history"""
    predictions: List[PredictionHistoryResponse]
    total: int

