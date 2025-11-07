"""Symptom schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SymptomBase(BaseModel):
    """Base symptom schema"""
    name: str = Field(..., min_length=1, max_length=100, description="Symptom name")
    description: Optional[str] = Field(None, description="Symptom description")


class SymptomCreate(SymptomBase):
    """Schema for creating a new symptom"""
    pass


class SymptomUpdate(BaseModel):
    """Schema for updating a symptom"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class SymptomResponse(SymptomBase):
    """Schema for symptom response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SymptomListResponse(BaseModel):
    """Schema for list of symptoms"""
    symptoms: list[SymptomResponse]
    total: int

