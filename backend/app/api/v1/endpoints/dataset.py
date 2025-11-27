"""Dataset endpoints for data scientist"""
import traceback
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger
from pydantic import BaseModel

from app.api.deps import get_db

router = APIRouter()


class DatasetRecord(BaseModel):
    """Dataset record schema"""
    date_modified: str
    disease: str
    symptoms: List[str]


class DatasetListResponse(BaseModel):
    """Dataset list response schema"""
    records: List[DatasetRecord]
    total: int


@router.get("/records", response_model=DatasetListResponse)
def get_dataset_records(
    search: Optional[str] = Query(None, description="Search for disease name"),
    db: Session = Depends(get_db)
):
    """
    Get dataset records (diseases with their symptoms)
    
    Args:
        search: Optional search term to filter diseases
        
    Returns:
        List of dataset records with disease names, modification dates, and symptoms
    """
    try:
        # Path to CSV file
        backend_dir = Path(__file__).parent.parent.parent.parent.parent
        csv_path = backend_dir / "ml" / "data" / "processed" / "processed_dataset_with_groups.csv"
        
        if not csv_path.exists():
            logger.warning(f"CSV file not found: {csv_path}")
            return DatasetListResponse(records=[], total=0)
        
        records = []
        disease_to_symptoms = {}
        disease_to_date = {}
        
        # Read CSV file
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                disease_name = row.get('disease', '').strip()
                if not disease_name:
                    continue
                
                # Collect all symptoms from all groups
                symptom_names = []
                group_columns = [
                    'pain', 'respiratory', 'fever', 'digestive', 'urinary',
                    'skin', 'neurological', 'vision', 'energy', 'mental',
                    'joint_muscle', 'appetite_weight', 'other'
                ]
                
                for group in group_columns:
                    symptoms_str = row.get(group, '').strip()
                    if symptoms_str:
                        # Split by comma and clean up
                        group_symptoms = [s.strip() for s in symptoms_str.split(',') if s.strip()]
                        symptom_names.extend(group_symptoms)
                
                # Use disease name as key (case-insensitive)
                disease_key = disease_name.lower()
                
                # Merge symptoms for same disease
                if disease_key not in disease_to_symptoms:
                    disease_to_symptoms[disease_key] = set()
                    disease_to_date[disease_key] = disease_name  # Store original case
                
                disease_to_symptoms[disease_key].update(symptom_names)
        
        # Convert to list of records
        for disease_key, symptoms_set in disease_to_symptoms.items():
            disease_name = disease_to_date[disease_key]
            
            # Apply search filter if provided
            if search:
                search_lower = search.lower()
                if search_lower not in disease_name.lower():
                    # Also check if search term is in symptoms
                    if not any(search_lower in s.lower() for s in symptoms_set):
                        continue
            
            # Get file modification time as date modified
            # In a real scenario, each disease would have its own modification date
            # For now, we use the CSV file modification time
            try:
                mtime = csv_path.stat().st_mtime
                date_modified = datetime.fromtimestamp(mtime).strftime('%d/%m/%Y')
            except:
                date_modified = datetime.now().strftime('%d/%m/%Y')
            
            records.append(DatasetRecord(
                date_modified=date_modified,
                disease=disease_name,
                symptoms=sorted(list(symptoms_set))  # Sort for consistency
            ))
        
        # Sort by disease name
        records.sort(key=lambda x: x.disease.lower())
        
        return DatasetListResponse(
            records=records,
            total=len(records)
        )
        
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting dataset records: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting dataset records: {str(e)}"
        )

