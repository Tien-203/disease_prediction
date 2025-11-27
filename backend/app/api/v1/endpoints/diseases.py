"""Disease endpoints"""
import traceback
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from loguru import logger

from app.api.deps import get_db
from app.schemas.disease import (
    DiseaseCreate,
    DiseaseUpdate,
    DiseaseResponse,
    DiseaseListResponse
)
from app.services.disease_service import DiseaseService
from app.services.dataset_service import DatasetService

router = APIRouter()


# Schema for saving disease with symptoms
class DiseaseWithSymptomsCreate(BaseModel):
    """Schema for creating disease with symptoms"""
    disease_name: str
    symptom_ids: List[int]
    recommendation: Optional[str] = None


class DiseaseWithSymptomsUpdate(BaseModel):
    """Schema for updating disease with symptoms"""
    symptom_ids: List[int]
    recommendation: Optional[str] = None


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
    try:
        service = DiseaseService(db)
        diseases, total = service.get_all_diseases(skip=skip, limit=limit)
        
        return DiseaseListResponse(diseases=diseases, total=total)
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting diseases: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting diseases: {str(e)}"
        )


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
    try:
        service = DiseaseService(db)
        diseases = service.search_diseases(name)
        
        return DiseaseListResponse(diseases=diseases, total=len(diseases))
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error searching diseases with name '{name}': {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching diseases: {str(e)}"
        )


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
    try:
        service = DiseaseService(db)
        disease = service.get_disease_by_id(disease_id)
        
        if not disease:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Disease with ID {disease_id} not found"
            )
        
        return disease
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting disease by ID {disease_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting disease: {str(e)}"
        )


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
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error creating disease: {str(e)}\n{traceback_str}")
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
    try:
        service = DiseaseService(db)
        disease = service.update_disease(disease_id, disease_data)
        
        if not disease:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Disease with ID {disease_id} not found"
            )
        
        return disease
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error updating disease ID {disease_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating disease: {str(e)}"
        )


@router.delete("/by-name/{disease_name}", status_code=status.HTTP_200_OK)
def delete_disease_by_name(
    disease_name: str,
    db: Session = Depends(get_db)
):
    """
    Delete a disease from reference_data.json and CSV file
    Does not delete the symptoms themselves
    
    Args:
        disease_name: Name of the disease to delete (URL encoded)
    """
    try:
        from urllib.parse import unquote
        decoded_name = unquote(disease_name)
        
        dataset_service = DatasetService(db)
        result = dataset_service.delete_disease(decoded_name)
        return result
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error deleting disease: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting disease: {str(e)}"
        )


@router.delete("/{disease_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a disease by ID
    
    Args:
        disease_id: Disease ID
    """
    try:
        service = DiseaseService(db)
        success = service.delete_disease(disease_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Disease with ID {disease_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error deleting disease ID {disease_id}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting disease: {str(e)}"
        )


@router.post("/with-symptoms", status_code=status.HTTP_201_CREATED)
def create_disease_with_symptoms(
    disease_data: DiseaseWithSymptomsCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new disease with symptoms and save to reference_data.json and CSV
    
    Args:
        disease_data: Disease name, symptom IDs, and optional recommendation
    """
    try:
        dataset_service = DatasetService(db)
        result = dataset_service.add_disease_with_symptoms(
            disease_name=disease_data.disease_name,
            symptom_ids=disease_data.symptom_ids,
            recommendation=disease_data.recommendation
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error creating disease with symptoms: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating disease with symptoms: {str(e)}"
        )


@router.get("/{disease_name}/symptoms", status_code=status.HTTP_200_OK)
def get_disease_symptoms(
    disease_name: str,
    db: Session = Depends(get_db)
):
    """
    Get symptoms for a disease from CSV file
    
    Args:
        disease_name: Name of the disease (URL encoded)
    """
    try:
        from urllib.parse import unquote
        decoded_name = unquote(disease_name)
        
        dataset_service = DatasetService(db)
        result = dataset_service.get_disease_symptoms(decoded_name)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Disease '{decoded_name}' not found in dataset"
            )
        
        # Get symptom IDs from symptom names
        from app.models.symptom import Symptom
        symptoms = db.query(Symptom).filter(Symptom.name.in_(result['symptom_names'])).all()
        symptom_ids = [s.id for s in symptoms]
        found_names = {s.name for s in symptoms}
        missing_names = set(result['symptom_names']) - found_names
        
        if missing_names:
            logger.warning(f"Some symptom names from CSV not found in database: {missing_names}")
        
        return {
            "disease_name": result['disease_name'],
            "symptom_names": result['symptom_names'],
            "symptom_ids": symptom_ids,
            "missing_symptoms": list(missing_names) if missing_names else []
        }
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting disease symptoms: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting disease symptoms: {str(e)}"
        )


@router.put("/{disease_name}/symptoms", status_code=status.HTTP_200_OK)
def update_disease_symptoms(
    disease_name: str,
    disease_data: DiseaseWithSymptomsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing disease's symptoms and save to CSV
    
    Args:
        disease_name: Name of the disease to update (URL encoded)
        disease_data: Symptom IDs and optional recommendation
    """
    try:
        from urllib.parse import unquote
        decoded_name = unquote(disease_name)
        
        dataset_service = DatasetService(db)
        result = dataset_service.update_disease_symptoms(
            disease_name=decoded_name,
            symptom_ids=disease_data.symptom_ids,
            recommendation=disease_data.recommendation
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error updating disease symptoms: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating disease symptoms: {str(e)}"
        )



