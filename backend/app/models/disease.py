"""Disease database model"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from sqlalchemy.sql import func
from app.db.base import Base


class Disease(Base):
    """Disease model for storing disease information"""
    __tablename__ = "diseases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    severity = Column(String(20), nullable=True)  # mild, moderate, severe
    precautions = Column(ARRAY(Text), nullable=True)
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Disease(id={self.id}, name='{self.name}', severity='{self.severity}')>"

