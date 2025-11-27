"""Service for managing dataset files (reference_data.json and CSV)"""
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.symptom import Symptom
from app.models.disease import Disease


class DatasetService:
    """Service for managing dataset files for ML training"""
    
    def __init__(self, db: Session):
        self.db = db
        # Paths relative to backend directory
        # __file__ is at backend/app/services/dataset_service.py
        # So parent.parent.parent gives us backend directory
        backend_dir = Path(__file__).parent.parent.parent
        self.reference_data_path = backend_dir / "app" / "db" / "reference_data.json"
        self.csv_path = backend_dir / "ml" / "data" / "processed" / "processed_dataset_with_groups.csv"
    
    def _get_symptom_group_mapping(self) -> Dict[str, str]:
        """
        Get mapping of symptom names to their groups
        Matches the logic in preprocess_data_with_groups.py and symptom_service.py
        """
        categories: Dict[str, List[str]] = {
            "pain": ["pain", "ache", "cramp", "sore"],
            "respiratory": ["cough", "breath", "sneezing", "congestion", "phlegm", "sputum", "runny_nose", "throat"],
            "fever": ["fever", "chills", "shivering", "sweating"],
            "digestive": ["abdominal", "belly", "stomach", "nausea", "vomiting", "diarrhoea", "constipation", "indigestion", "acidity", "gas"],
            "urinary": ["urine", "urination", "bladder", "micturition", "polyuria"],
            "skin": ["rash", "itching", "blister", "eruption", "patches", "peeling", "yellowish_skin", "redness", "blackheads", "pimples"],
            "neurological": ["headache", "dizziness", "vertigo", "loss_of_balance", "unsteadiness", "slurred_speech", "coma", "altered_sensorium", "weakness", "paralysis"],
            "vision": ["vision", "eyes", "blurred", "redness_of_eyes", "watering_from_eyes", "yellowing_of_eyes", "sunken_eyes"],
            "energy": ["fatigue", "lethargy", "weakness", "malaise", "loss_of_appetite", "excessive_hunger", "increased_appetite"],
            "mental": ["anxiety", "depression", "irritability", "mood_swings", "restlessness", "lack_of_concentration"],
            "joint_muscle": ["joint", "muscle", "knee", "hip", "neck", "back", "stiffness", "swelling", "movement"],
            "appetite_weight": ["appetite", "weight", "obesity", "loss_of_appetite", "increased_appetite", "excessive_hunger"]
        }
        
        symptom_to_group: Dict[str, str] = {}
        for group_name, keywords in categories.items():
            for keyword in keywords:
                symptom_to_group[keyword] = group_name
        
        return symptom_to_group, categories
    
    def _map_symptom_to_group(self, symptom_name: str, categories: Dict[str, List[str]]) -> str:
        """Map a symptom name to its group"""
        symptom_lower = symptom_name.lower().strip().replace(' ', '_')
        
        for group_name, keywords in categories.items():
            if any(keyword in symptom_lower for keyword in keywords):
                return group_name
        
        return "other"
    
    def add_disease_with_symptoms(
        self,
        disease_name: str,
        symptom_ids: List[int],
        recommendation: Optional[str] = None
    ) -> Dict:
        """
        Add a new disease with symptoms to both reference_data.json and CSV file
        
        Args:
            disease_name: Name of the disease
            symptom_ids: List of symptom IDs selected
            recommendation: Optional recommendation text
            
        Returns:
            Dictionary with success status and message
        """
        try:
            # Validate input
            if not symptom_ids:
                raise ValueError("No symptom IDs provided. Please select at least one symptom.")
            
            # Get symptom names from IDs
            symptoms = self.db.query(Symptom).filter(Symptom.id.in_(symptom_ids)).all()
            found_ids = {s.id for s in symptoms}
            missing_ids = set(symptom_ids) - found_ids
            
            if missing_ids:
                logger.warning(f"Some symptom IDs not found in database: {missing_ids}. Skipping them.")
                # Only use symptoms that exist in database
                symptom_ids = list(found_ids)
            
            if not symptom_ids:
                raise ValueError("No valid symptom IDs found. Please select at least one valid symptom.")
            
            symptom_names = [s.name for s in symptoms]
            
            # Update reference_data.json
            self._update_reference_data(disease_name, symptom_names, recommendation)
            
            # Update CSV file
            self._update_csv_file(disease_name, symptom_names)
            
            # Optionally save to database
            existing_disease = self.db.query(Disease).filter(Disease.name == disease_name).first()
            if not existing_disease:
                disease = Disease(
                    name=disease_name,
                    description=f"Disease with symptoms: {', '.join(symptom_names[:5])}...",
                    recommendations=recommendation or "Please consult a healthcare provider for proper diagnosis and treatment."
                )
                self.db.add(disease)
                self.db.commit()
                logger.info(f"Created disease in database: {disease_name}")
            
            return {
                "success": True,
                "message": f"Disease '{disease_name}' added successfully with {len(symptom_names)} symptoms"
            }
            
        except Exception as e:
            logger.error(f"Error adding disease with symptoms: {str(e)}")
            self.db.rollback()
            raise
    
    def _update_reference_data(
        self,
        disease_name: str,
        symptom_names: List[str],
        recommendation: Optional[str] = None
    ):
        """Update reference_data.json file"""
        # Read existing data
        if not self.reference_data_path.exists():
            raise FileNotFoundError(f"Reference data file not found: {self.reference_data_path}")
        
        with open(self.reference_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add disease if not exists
        if disease_name not in data.get("diseases", []):
            data["diseases"].append(disease_name)
            data["diseases"].sort()
        
        # Add symptoms if not exists
        existing_symptoms = set(data.get("symptoms", []))
        new_symptoms = [s for s in symptom_names if s not in existing_symptoms]
        if new_symptoms:
            data["symptoms"].extend(new_symptoms)
            data["symptoms"].sort()
        
        # Add recommendation
        if "disease_recommendations" not in data:
            data["disease_recommendations"] = {}
        
        if recommendation:
            data["disease_recommendations"][disease_name] = recommendation
        elif disease_name not in data["disease_recommendations"]:
            # Default recommendation if not provided
            data["disease_recommendations"][disease_name] = "Please consult a healthcare provider for proper diagnosis and treatment."
        
        # Update statistics
        data["statistics"] = {
            "total_symptoms": len(data["symptoms"]),
            "total_diseases": len(data["diseases"])
        }
        
        # Update timestamp
        data["import_timestamp"] = datetime.utcnow().isoformat()
        
        # Write back
        with open(self.reference_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Updated reference_data.json with disease: {disease_name}")
    
    def _update_csv_file(self, disease_name: str, symptom_names: List[str]):
        """Update processed_dataset_with_groups.csv file"""
        # Get group mapping
        symptom_to_group, categories = self._get_symptom_group_mapping()
        
        # Group symptoms by their groups
        grouped_symptoms: Dict[str, List[str]] = {
            "pain": [],
            "respiratory": [],
            "fever": [],
            "digestive": [],
            "urinary": [],
            "skin": [],
            "neurological": [],
            "vision": [],
            "energy": [],
            "mental": [],
            "joint_muscle": [],
            "appetite_weight": [],
            "other": []
        }
        
        for symptom_name in symptom_names:
            group = self._map_symptom_to_group(symptom_name, categories)
            grouped_symptoms[group].append(symptom_name)
        
        # Prepare CSV row
        csv_row = {
            "disease": disease_name,
            "pain": ",".join(grouped_symptoms["pain"]) if grouped_symptoms["pain"] else "",
            "respiratory": ",".join(grouped_symptoms["respiratory"]) if grouped_symptoms["respiratory"] else "",
            "fever": ",".join(grouped_symptoms["fever"]) if grouped_symptoms["fever"] else "",
            "digestive": ",".join(grouped_symptoms["digestive"]) if grouped_symptoms["digestive"] else "",
            "urinary": ",".join(grouped_symptoms["urinary"]) if grouped_symptoms["urinary"] else "",
            "skin": ",".join(grouped_symptoms["skin"]) if grouped_symptoms["skin"] else "",
            "neurological": ",".join(grouped_symptoms["neurological"]) if grouped_symptoms["neurological"] else "",
            "vision": ",".join(grouped_symptoms["vision"]) if grouped_symptoms["vision"] else "",
            "energy": ",".join(grouped_symptoms["energy"]) if grouped_symptoms["energy"] else "",
            "mental": ",".join(grouped_symptoms["mental"]) if grouped_symptoms["mental"] else "",
            "joint_muscle": ",".join(grouped_symptoms["joint_muscle"]) if grouped_symptoms["joint_muscle"] else "",
            "appetite_weight": ",".join(grouped_symptoms["appetite_weight"]) if grouped_symptoms["appetite_weight"] else "",
            "other": ",".join(grouped_symptoms["other"]) if grouped_symptoms["other"] else ""
        }
        
        # Check if CSV file exists and has header
        file_exists = self.csv_path.exists()
        
        # Write to CSV
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            fieldnames = [
                "disease", "pain", "respiratory", "fever", "digestive", "urinary",
                "skin", "neurological", "vision", "energy", "mental",
                "joint_muscle", "appetite_weight", "other"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write row
            writer.writerow(csv_row)
        
        logger.info(f"Added row to CSV for disease: {disease_name}")
    
    def _replace_csv_rows(self, disease_name: str, symptom_names: List[str]):
        """
        Replace all existing rows for a disease with a new row in CSV file
        
        Args:
            disease_name: Name of the disease
            symptom_names: List of symptom names
        """
        # Get group mapping
        symptom_to_group, categories = self._get_symptom_group_mapping()
        
        # Group symptoms by their groups
        grouped_symptoms: Dict[str, List[str]] = {
            "pain": [],
            "respiratory": [],
            "fever": [],
            "digestive": [],
            "urinary": [],
            "skin": [],
            "neurological": [],
            "vision": [],
            "energy": [],
            "mental": [],
            "joint_muscle": [],
            "appetite_weight": [],
            "other": []
        }
        
        for symptom_name in symptom_names:
            group = self._map_symptom_to_group(symptom_name, categories)
            grouped_symptoms[group].append(symptom_name)
        
        # Prepare CSV row
        csv_row = {
            "disease": disease_name,
            "pain": ",".join(grouped_symptoms["pain"]) if grouped_symptoms["pain"] else "",
            "respiratory": ",".join(grouped_symptoms["respiratory"]) if grouped_symptoms["respiratory"] else "",
            "fever": ",".join(grouped_symptoms["fever"]) if grouped_symptoms["fever"] else "",
            "digestive": ",".join(grouped_symptoms["digestive"]) if grouped_symptoms["digestive"] else "",
            "urinary": ",".join(grouped_symptoms["urinary"]) if grouped_symptoms["urinary"] else "",
            "skin": ",".join(grouped_symptoms["skin"]) if grouped_symptoms["skin"] else "",
            "neurological": ",".join(grouped_symptoms["neurological"]) if grouped_symptoms["neurological"] else "",
            "vision": ",".join(grouped_symptoms["vision"]) if grouped_symptoms["vision"] else "",
            "energy": ",".join(grouped_symptoms["energy"]) if grouped_symptoms["energy"] else "",
            "mental": ",".join(grouped_symptoms["mental"]) if grouped_symptoms["mental"] else "",
            "joint_muscle": ",".join(grouped_symptoms["joint_muscle"]) if grouped_symptoms["joint_muscle"] else "",
            "appetite_weight": ",".join(grouped_symptoms["appetite_weight"]) if grouped_symptoms["appetite_weight"] else "",
            "other": ",".join(grouped_symptoms["other"]) if grouped_symptoms["other"] else ""
        }
        
        if not self.csv_path.exists():
            logger.warning(f"CSV file not found: {self.csv_path}")
            return
        
        # Read all rows, filter out old rows for this disease, then write back
        fieldnames = [
            "disease", "pain", "respiratory", "fever", "digestive", "urinary",
            "skin", "neurological", "vision", "energy", "mental",
            "joint_muscle", "appetite_weight", "other"
        ]
        
        rows = []
        disease_name_lower = disease_name.strip().lower()
        
        # Read all rows except the ones for this disease
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_disease = row.get('disease', '').strip().lower()
                if row_disease != disease_name_lower:
                    rows.append(row)
        
        # Add the new row
        rows.append(csv_row)
        
        # Write all rows back
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Replaced rows in CSV for disease: {disease_name}")
    
    def update_disease_symptoms(
        self,
        disease_name: str,
        symptom_ids: List[int],
        recommendation: Optional[str] = None
    ) -> Dict:
        """
        Update an existing disease's symptoms
        
        Args:
            disease_name: Name of the disease to update
            symptom_ids: List of symptom IDs
            recommendation: Optional recommendation text
            
        Returns:
            Dictionary with success status and message
        """
        try:
            # Get symptom names from IDs
            symptoms = self.db.query(Symptom).filter(Symptom.id.in_(symptom_ids)).all()
            found_ids = {s.id for s in symptoms}
            missing_ids = set(symptom_ids) - found_ids
            
            if missing_ids:
                logger.warning(f"Some symptom IDs not found in database: {missing_ids}. Skipping them.")
                # Only use symptoms that exist in database
                symptom_ids = list(found_ids)
            
            if not symptom_ids:
                raise ValueError("No valid symptom IDs found. Please select at least one valid symptom.")
            
            symptom_names = [s.name for s in symptoms]
            
            # Update reference_data.json (recommendation only, disease already exists)
            if recommendation:
                self._update_reference_data(disease_name, symptom_names, recommendation)
            
            # Update CSV file - replace all old rows with new one
            self._replace_csv_rows(disease_name, symptom_names)
            
            # Update database
            disease = self.db.query(Disease).filter(Disease.name == disease_name).first()
            if disease:
                if recommendation:
                    disease.recommendations = recommendation
                self.db.commit()
                logger.info(f"Updated disease in database: {disease_name}")
            
            return {
                "success": True,
                "message": f"Disease '{disease_name}' updated successfully with {len(symptom_names)} symptoms"
            }
            
        except Exception as e:
            logger.error(f"Error updating disease symptoms: {str(e)}")
            self.db.rollback()
            raise
    
    def get_disease_symptoms(self, disease_name: str) -> Optional[Dict]:
        """
        Get symptoms for a disease from CSV file
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Dictionary with disease name and list of symptom names, or None if not found
        """
        try:
            if not self.csv_path.exists():
                logger.warning(f"CSV file not found: {self.csv_path}")
                return None
            
            # Read CSV file
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('disease', '').strip().lower() == disease_name.strip().lower():
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
                        
                        return {
                            'disease_name': row.get('disease', disease_name),
                            'symptom_names': list(set(symptom_names))  # Remove duplicates
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting disease symptoms: {str(e)}")
            return None
    
    def delete_disease(self, disease_name: str) -> Dict:
        """
        Delete a disease from reference_data.json and CSV file
        Does not delete the symptoms themselves
        
        Args:
            disease_name: Name of the disease to delete
            
        Returns:
            Dictionary with success status and message
        """
        try:
            # Delete from reference_data.json
            if not self.reference_data_path.exists():
                raise FileNotFoundError(f"Reference data file not found: {self.reference_data_path}")
            
            with open(self.reference_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Remove disease from diseases list
            if disease_name in data.get("diseases", []):
                data["diseases"].remove(disease_name)
                data["diseases"].sort()
            
            # Remove recommendation
            if "disease_recommendations" in data and disease_name in data["disease_recommendations"]:
                del data["disease_recommendations"][disease_name]
            
            # Update statistics
            data["statistics"] = {
                "total_symptoms": len(data.get("symptoms", [])),
                "total_diseases": len(data.get("diseases", []))
            }
            
            # Update timestamp
            data["import_timestamp"] = datetime.utcnow().isoformat()
            
            # Write back
            with open(self.reference_data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Removed disease from reference_data.json: {disease_name}")
            
            # Delete from CSV file
            if self.csv_path.exists():
                fieldnames = [
                    "disease", "pain", "respiratory", "fever", "digestive", "urinary",
                    "skin", "neurological", "vision", "energy", "mental",
                    "joint_muscle", "appetite_weight", "other"
                ]
                
                rows = []
                disease_name_lower = disease_name.strip().lower()
                
                # Read all rows except the ones for this disease
                with open(self.csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        row_disease = row.get('disease', '').strip().lower()
                        if row_disease != disease_name_lower:
                            rows.append(row)
                
                # Write all rows back (excluding deleted disease)
                with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                
                logger.info(f"Removed disease rows from CSV: {disease_name}")
            
            # Delete from database (optional)
            disease = self.db.query(Disease).filter(Disease.name == disease_name).first()
            if disease:
                self.db.delete(disease)
                self.db.commit()
                logger.info(f"Deleted disease from database: {disease_name}")
            
            return {
                "success": True,
                "message": f"Disease '{disease_name}' deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting disease: {str(e)}")
            self.db.rollback()
            raise

