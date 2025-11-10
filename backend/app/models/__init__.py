"""Database models"""
from app.models.user import User
from app.models.prediction import Prediction
from app.models.symptom import Symptom
from app.models.disease import Disease

__all__ = ["User", "Prediction", "Symptom", "Disease"]

