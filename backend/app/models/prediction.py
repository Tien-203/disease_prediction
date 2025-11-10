"""Prediction database model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Prediction(Base):
    """Prediction model for storing prediction history"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    symptoms = Column(ARRAY(Text), nullable=False)  # Array of symptom names
    predicted_disease = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    alternatives = Column(JSONB, nullable=True)  # Alternative predictions as JSON
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_id = Column(String(100), nullable=True, index=True)  # For tracking user sessions
    
    # Relationship to user
    user = relationship("User", back_populates="predictions")
    
    # Add check constraint for confidence
    __table_args__ = (
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="check_confidence_range"),
    )
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, user_id={self.user_id}, disease='{self.predicted_disease}', confidence={self.confidence})>"

