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


class SymptomOption(BaseModel):
    """Schema for a symptom option in a group"""
    id: int
    name: str
    display_name: str  # Human-readable name


class SymptomGroup(BaseModel):
    """Schema for a group of symptoms (question)"""
    id: str  # Category ID
    question: str  # Question text
    options: list[SymptomOption]  # Available symptom options
    allow_multiple: bool = True  # Whether multiple selections are allowed


class SymptomGroupsResponse(BaseModel):
    """Schema for grouped symptoms response"""
    groups: list[SymptomGroup]


class SymptomExtractionRequest(BaseModel):
    """Schema for symptom extraction from natural language"""
    description: str = Field(..., min_length=1, description="Natural language description of symptoms")


class SymptomExtractionResponse(BaseModel):
    """Schema for symptom extraction response"""
    symptoms: list[str] = Field(..., description="List of extracted predefined symptom names")
    count: int = Field(..., description="Number of symptoms extracted")
