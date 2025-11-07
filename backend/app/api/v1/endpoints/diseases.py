"""Disease endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db
from app.schemas.disease import (
    DiseaseCreate,
    DiseaseUpdate,
    DiseaseResponse,
    DiseaseListResponse
)
from app.services.disease_service import DiseaseService

router = APIRouter()


@router.get("", response_model=DiseaseListResponse)
def get_diseases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all diseases with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
    """
    service = DiseaseService(db)
    diseases, total = service.get_all_diseases(skip=skip, limit=limit)
    
    return DiseaseListResponse(diseases=diseases, total=total)


@router.get("/search", response_model=DiseaseListResponse)
def search_diseases(
    name: str = Query(..., description="Disease name to search for"),
    db: Session = Depends(get_db)
):
    """
    Search diseases by name
    
    Args:
        name: Disease name to search for
    """
    service = DiseaseService(db)
    diseases = service.search_diseases(name)
    
    return DiseaseListResponse(diseases=diseases, total=len(diseases))


@router.get("/{disease_id}", response_model=DiseaseResponse)
def get_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    """
    Get disease by ID
    
    Args:
        disease_id: Disease ID
    """
    service = DiseaseService(db)
    disease = service.get_disease_by_id(disease_id)
    
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease with ID {disease_id} not found"
        )
    
    return disease


@router.post("", response_model=DiseaseResponse, status_code=status.HTTP_201_CREATED)
def create_disease(
    disease_data: DiseaseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new disease
    
    Args:
        disease_data: Disease creation data
    """
    service = DiseaseService(db)
    
    try:
        disease = service.create_disease(disease_data)
        return disease
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating disease: {str(e)}"
        )


@router.put("/{disease_id}", response_model=DiseaseResponse)
def update_disease(
    disease_id: int,
    disease_data: DiseaseUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a disease
    
    Args:
        disease_id: Disease ID
        disease_data: Disease update data
    """
    service = DiseaseService(db)
    disease = service.update_disease(disease_id, disease_data)
    
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease with ID {disease_id} not found"
        )
    
    return disease


@router.delete("/{disease_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a disease
    
    Args:
        disease_id: Disease ID
    """
    service = DiseaseService(db)
    success = service.delete_disease(disease_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease with ID {disease_id} not found"
        )

