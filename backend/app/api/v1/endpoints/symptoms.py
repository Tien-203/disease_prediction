"""Symptom endpoints"""
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from loguru import logger

from app.api.deps import get_db
from app.schemas.symptom import (
    SymptomCreate,
    SymptomUpdate,
    SymptomResponse,
    SymptomListResponse,
    SymptomGroupsResponse,
    SymptomExtractionRequest,
    SymptomExtractionResponse
)
from app.services.symptom_service import SymptomService
from app.services.symptom_extraction_service import SymptomExtractionService

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
    try:
        service = SymptomService(db)
        symptoms, total = service.get_all_symptoms(skip=skip, limit=limit)
        
        return SymptomListResponse(symptoms=symptoms, total=total)
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting symptoms: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting symptoms: {str(e)}"
        )


@router.get("/groups", response_model=SymptomGroupsResponse)
def get_grouped_symptoms(
    db: Session = Depends(get_db)
):
    """
    Get symptoms grouped by categories for quick check questions
    
    Returns grouped symptoms organized by common characteristics
    """
    try:
        service = SymptomService(db)
        return service.get_grouped_symptoms()
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting grouped symptoms: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting grouped symptoms: {str(e)}"
        )


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
    try:
        service = SymptomService(db)
        symptom = service.get_symptom_by_id(symptom_id)
        
        if not symptom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Symptom with ID {symptom_id} not found"
            )
        
        return symptom
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting symptom by ID {symptom_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting symptom: {str(e)}"
        )


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
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error creating symptom: {str(e)}\n{traceback_str}")
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
    try:
        service = SymptomService(db)
        symptom = service.update_symptom(symptom_id, symptom_data)
        
        if not symptom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Symptom with ID {symptom_id} not found"
            )
        
        return symptom
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error updating symptom ID {symptom_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating symptom: {str(e)}"
        )


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
    try:
        service = SymptomService(db)
        success = service.delete_symptom(symptom_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Symptom with ID {symptom_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error deleting symptom ID {symptom_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting symptom: {str(e)}"
        )


@router.post("/extract", response_model=SymptomExtractionResponse)
def extract_symptoms_from_description(
    request: SymptomExtractionRequest
):
    """
    Extract predefined symptoms from natural language description
    
    Args:
        request: Natural language description of symptoms
        
    Returns:
        List of extracted predefined symptom names
    """
    try:
        service = SymptomExtractionService()
        symptoms = service.extract_symptoms(request.description)
        
        return SymptomExtractionResponse(
            symptoms=symptoms,
            count=len(symptoms)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error extracting symptoms: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting symptoms: {str(e)}"
        )

