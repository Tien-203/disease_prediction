"""Symptom service for managing symptoms"""
from typing import List, Optional
from sqlalchemy.orm import Session
from loguru import logger

from app.models.symptom import Symptom
from app.schemas.symptom import SymptomCreate, SymptomUpdate, SymptomResponse


class SymptomService:
    """Service for handling symptom operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_symptoms(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[SymptomResponse], int]:
        """
        Get all symptoms with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (symptom list, total count)
        """
        total = self.db.query(Symptom).count()
        symptoms = self.db.query(Symptom).offset(skip).limit(limit).all()
        
        return [SymptomResponse.model_validate(s) for s in symptoms], total
    
    def get_symptom_by_id(self, symptom_id: int) -> Optional[SymptomResponse]:
        """
        Get symptom by ID
        
        Args:
            symptom_id: Symptom ID
            
        Returns:
            Symptom or None if not found
        """
        symptom = self.db.query(Symptom).filter(Symptom.id == symptom_id).first()
        
        if symptom:
            return SymptomResponse.model_validate(symptom)
        return None
    
    def create_symptom(self, symptom_data: SymptomCreate) -> SymptomResponse:
        """
        Create a new symptom
        
        Args:
            symptom_data: Symptom creation data
            
        Returns:
            Created symptom
        """
        symptom = Symptom(**symptom_data.model_dump())
        self.db.add(symptom)
        self.db.commit()
        self.db.refresh(symptom)
        
        logger.info(f"Created symptom: {symptom.name}")
        return SymptomResponse.model_validate(symptom)
    
    def update_symptom(
        self,
        symptom_id: int,
        symptom_data: SymptomUpdate
    ) -> Optional[SymptomResponse]:
        """
        Update a symptom
        
        Args:
            symptom_id: Symptom ID
            symptom_data: Symptom update data
            
        Returns:
            Updated symptom or None if not found
        """
        symptom = self.db.query(Symptom).filter(Symptom.id == symptom_id).first()
        
        if not symptom:
            return None
        
        update_data = symptom_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(symptom, field, value)
        
        self.db.commit()
        self.db.refresh(symptom)
        
        logger.info(f"Updated symptom ID: {symptom_id}")
        return SymptomResponse.model_validate(symptom)
    
    def delete_symptom(self, symptom_id: int) -> bool:
        """
        Delete a symptom
        
        Args:
            symptom_id: Symptom ID
            
        Returns:
            True if deleted, False if not found
        """
        symptom = self.db.query(Symptom).filter(Symptom.id == symptom_id).first()
        
        if not symptom:
            return False
        
        self.db.delete(symptom)
        self.db.commit()
        
        logger.info(f"Deleted symptom ID: {symptom_id}")
        return True

