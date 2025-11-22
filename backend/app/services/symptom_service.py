"""Symptom service for managing symptoms"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from loguru import logger

from app.models.symptom import Symptom
from app.schemas.symptom import (
    SymptomCreate, 
    SymptomUpdate, 
    SymptomResponse,
    SymptomGroup,
    SymptomOption,
    SymptomGroupsResponse
)


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
    
    def get_grouped_symptoms(self) -> SymptomGroupsResponse:
        """
        Get symptoms grouped by categories for quick check questions
        
        Returns:
            Grouped symptoms response
        """
        # Get all symptoms
        all_symptoms = self.db.query(Symptom).all()
        
        # Define symptom categories based on common characteristics
        categories: Dict[str, Dict] = {
            "pain": {
                "question": "Are you experiencing any pain?",
                "keywords": ["pain", "ache", "cramp", "sore"],
                "allow_multiple": True
            },
            "respiratory": {
                "question": "Do you have any respiratory symptoms?",
                "keywords": ["cough", "breath", "sneezing", "congestion", "phlegm", "sputum", "runny_nose", "throat"],
                "allow_multiple": True
            },
            "fever": {
                "question": "Do you have a fever or temperature-related symptoms?",
                "keywords": ["fever", "chills", "shivering", "sweating"],
                "allow_multiple": False
            },
            "digestive": {
                "question": "Are you experiencing any digestive issues?",
                "keywords": ["abdominal", "belly", "stomach", "nausea", "vomiting", "diarrhoea", "constipation", "indigestion", "acidity", "gas"],
                "allow_multiple": True
            },
            "urinary": {
                "question": "Do you have any urinary symptoms?",
                "keywords": ["urine", "urination", "bladder", "micturition", "polyuria"],
                "allow_multiple": True
            },
            "skin": {
                "question": "Are you experiencing any skin-related symptoms?",
                "keywords": ["rash", "itching", "blister", "eruption", "patches", "peeling", "yellowish_skin", "redness", "blackheads", "pimples"],
                "allow_multiple": True
            },
            "neurological": {
                "question": "Do you have any neurological symptoms?",
                "keywords": ["headache", "dizziness", "vertigo", "loss_of_balance", "unsteadiness", "slurred_speech", "coma", "altered_sensorium", "weakness", "paralysis"],
                "allow_multiple": True
            },
            "vision": {
                "question": "Are you experiencing any vision problems?",
                "keywords": ["vision", "eyes", "blurred", "redness_of_eyes", "watering_from_eyes", "yellowing_of_eyes", "sunken_eyes"],
                "allow_multiple": True
            },
            "energy": {
                "question": "How is your energy level?",
                "keywords": ["fatigue", "lethargy", "weakness", "malaise", "loss_of_appetite", "excessive_hunger", "increased_appetite"],
                "allow_multiple": True
            },
            "mental": {
                "question": "How are you feeling mentally or emotionally?",
                "keywords": ["anxiety", "depression", "irritability", "mood_swings", "restlessness", "lack_of_concentration"],
                "allow_multiple": True
            },
            "joint_muscle": {
                "question": "Do you have any joint or muscle problems?",
                "keywords": ["joint", "muscle", "knee", "hip", "neck", "back", "stiffness", "swelling", "movement"],
                "allow_multiple": True
            },
            "appetite_weight": {
                "question": "Have you noticed any changes in appetite or weight?",
                "keywords": ["appetite", "weight", "obesity", "loss_of_appetite", "increased_appetite", "excessive_hunger"],
                "allow_multiple": False
            }
        }
        
        groups: List[SymptomGroup] = []
        
        for category_id, category_info in categories.items():
            # Find symptoms that match this category
            matched_symptoms: List[Symptom] = []
            
            for symptom in all_symptoms:
                symptom_name_lower = symptom.name.lower()
                # Check if any keyword matches
                if any(keyword in symptom_name_lower for keyword in category_info["keywords"]):
                    matched_symptoms.append(symptom)
            
            # Only create group if there are matched symptoms
            if matched_symptoms:
                options = [
                    SymptomOption(
                        id=s.id,
                        name=s.name,
                        display_name=s.name.replace("_", " ").title()
                    )
                    for s in matched_symptoms
                ]
                
                groups.append(SymptomGroup(
                    id=category_id,
                    question=category_info["question"],
                    options=options,
                    allow_multiple=category_info["allow_multiple"]
                ))
        
        # Add a catch-all group for remaining symptoms
        categorized_symptom_ids = set()
        for group in groups:
            categorized_symptom_ids.update(opt.id for opt in group.options)
        
        remaining_symptoms = [
            s for s in all_symptoms 
            if s.id not in categorized_symptom_ids
        ]
        
        if remaining_symptoms:
            options = [
                SymptomOption(
                    id=s.id,
                    name=s.name,
                    display_name=s.name.replace("_", " ").title()
                )
                for s in remaining_symptoms[:20]  # Limit to 20 to avoid overwhelming
            ]
            
            if options:
                groups.append(SymptomGroup(
                    id="other",
                    question="Do you have any other symptoms?",
                    options=options,
                    allow_multiple=True
                ))
        
        logger.info(f"Grouped {len(all_symptoms)} symptoms into {len(groups)} categories")
        return SymptomGroupsResponse(groups=groups)

