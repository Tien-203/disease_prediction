"""Disease schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class DiseaseBase(BaseModel):
    """Base disease schema"""
    name: str = Field(..., min_length=1, max_length=100, description="Disease name")
    description: Optional[str] = Field(None, description="Disease description")
    severity: Optional[str] = Field(None, description="Disease severity: mild, moderate, severe")
    precautions: Optional[List[str]] = Field(None, description="List of precautions")
    recommendations: Optional[str] = Field(None, description="Medical recommendations")


class DiseaseCreate(DiseaseBase):
    """Schema for creating a new disease"""
    pass


class DiseaseUpdate(BaseModel):
    """Schema for updating a disease"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    severity: Optional[str] = None
    precautions: Optional[List[str]] = None
    recommendations: Optional[str] = None


class DiseaseResponse(DiseaseBase):
    """Schema for disease response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DiseaseListResponse(BaseModel):
    """Schema for list of diseases"""
    diseases: list[DiseaseResponse]
    total: int

