"""Disease service for managing diseases"""
from typing import List, Optional
from sqlalchemy.orm import Session
from loguru import logger

from app.models.disease import Disease
from app.schemas.disease import DiseaseCreate, DiseaseUpdate, DiseaseResponse


class DiseaseService:
    """Service for handling disease operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_diseases(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[DiseaseResponse], int]:
        """
        Get all diseases with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (disease list, total count)
        """
        total = self.db.query(Disease).count()
        diseases = self.db.query(Disease).offset(skip).limit(limit).all()
        
        return [DiseaseResponse.model_validate(d) for d in diseases], total
    
    def get_disease_by_id(self, disease_id: int) -> Optional[DiseaseResponse]:
        """
        Get disease by ID
        
        Args:
            disease_id: Disease ID
            
        Returns:
            Disease or None if not found
        """
        disease = self.db.query(Disease).filter(Disease.id == disease_id).first()
        
        if disease:
            return DiseaseResponse.model_validate(disease)
        return None
    
    def search_diseases(self, name: str) -> List[DiseaseResponse]:
        """
        Search diseases by name
        
        Args:
            name: Disease name to search for
            
        Returns:
            List of matching diseases
        """
        diseases = self.db.query(Disease).filter(
            Disease.name.ilike(f"%{name}%")
        ).all()
        
        return [DiseaseResponse.model_validate(d) for d in diseases]
    
    def create_disease(self, disease_data: DiseaseCreate) -> DiseaseResponse:
        """
        Create a new disease
        
        Args:
            disease_data: Disease creation data
            
        Returns:
            Created disease
        """
        disease = Disease(**disease_data.model_dump())
        self.db.add(disease)
        self.db.commit()
        self.db.refresh(disease)
        
        logger.info(f"Created disease: {disease.name}")
        return DiseaseResponse.model_validate(disease)
    
    def update_disease(
        self,
        disease_id: int,
        disease_data: DiseaseUpdate
    ) -> Optional[DiseaseResponse]:
        """
        Update a disease
        
        Args:
            disease_id: Disease ID
            disease_data: Disease update data
            
        Returns:
            Updated disease or None if not found
        """
        disease = self.db.query(Disease).filter(Disease.id == disease_id).first()
        
        if not disease:
            return None
        
        update_data = disease_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(disease, field, value)
        
        self.db.commit()
        self.db.refresh(disease)
        
        logger.info(f"Updated disease ID: {disease_id}")
        return DiseaseResponse.model_validate(disease)
    
    def delete_disease(self, disease_id: int) -> bool:
        """
        Delete a disease
        
        Args:
            disease_id: Disease ID
            
        Returns:
            True if deleted, False if not found
        """
        disease = self.db.query(Disease).filter(Disease.id == disease_id).first()
        
        if not disease:
            return False
        
        self.db.delete(disease)
        self.db.commit()
        
        logger.info(f"Deleted disease ID: {disease_id}")
        return True

