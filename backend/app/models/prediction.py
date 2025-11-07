"""Prediction database model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY, Text
from sqlalchemy.sql import func
from app.db.base import Base


class Prediction(Base):
    """Prediction model for storing prediction history"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(ARRAY(Text), nullable=False)  # Array of symptom names
    predicted_disease = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_id = Column(String(100), nullable=True, index=True)  # For tracking user sessions
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, disease='{self.predicted_disease}', confidence={self.confidence})>"

