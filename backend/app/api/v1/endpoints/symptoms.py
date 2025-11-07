"""Symptom endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db
from app.schemas.symptom import (
    SymptomCreate,
    SymptomUpdate,
    SymptomResponse,
    SymptomListResponse
)
from app.services.symptom_service import SymptomService

router = APIRouter()


@router.get("", response_model=SymptomListResponse)
def get_symptoms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all symptoms with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
    """
    service = SymptomService(db)
    symptoms, total = service.get_all_symptoms(skip=skip, limit=limit)
    
    return SymptomListResponse(symptoms=symptoms, total=total)


@router.get("/{symptom_id}", response_model=SymptomResponse)
def get_symptom(
    symptom_id: int,
    db: Session = Depends(get_db)
):
    """
    Get symptom by ID
    
    Args:
        symptom_id: Symptom ID
    """
    service = SymptomService(db)
    symptom = service.get_symptom_by_id(symptom_id)
    
    if not symptom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symptom with ID {symptom_id} not found"
        )
    
    return symptom


@router.post("", response_model=SymptomResponse, status_code=status.HTTP_201_CREATED)
def create_symptom(
    symptom_data: SymptomCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new symptom
    
    Args:
        symptom_data: Symptom creation data
    """
    service = SymptomService(db)
    
    try:
        symptom = service.create_symptom(symptom_data)
        return symptom
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating symptom: {str(e)}"
        )


@router.put("/{symptom_id}", response_model=SymptomResponse)
def update_symptom(
    symptom_id: int,
    symptom_data: SymptomUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a symptom
    
    Args:
        symptom_id: Symptom ID
        symptom_data: Symptom update data
    """
    service = SymptomService(db)
    symptom = service.update_symptom(symptom_id, symptom_data)
    
    if not symptom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symptom with ID {symptom_id} not found"
        )
    
    return symptom


@router.delete("/{symptom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_symptom(
    symptom_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a symptom
    
    Args:
        symptom_id: Symptom ID
    """
    service = SymptomService(db)
    success = service.delete_symptom(symptom_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symptom with ID {symptom_id} not found"
        )

