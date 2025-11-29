"""Model performance schemas"""
from typing import List, Optional
from pydantic import BaseModel


class OverallMetrics(BaseModel):
    """Overall model performance metrics"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    accuracy_std: Optional[float] = None
    precision_std: Optional[float] = None
    recall_std: Optional[float] = None
    f1_std: Optional[float] = None


class ModelPerformanceResponse(BaseModel):
    """Model performance response schema"""
    model_type: str
    model_version: str
    n_estimators: Optional[int] = None
    n_features: int
    n_classes: int
    overall_metrics: OverallMetrics
    feature_importance: List[dict]


