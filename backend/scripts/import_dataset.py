"""Standalone script to import dataset data to database"""
import sys
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Set, Optional

# Add backend to path when run as script
if __name__ == "__main__":
    backend_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from loguru import logger

from app.db.session import SessionLocal
from app.models.symptom import Symptom
from app.models.disease import Disease


class DatasetImporter:
    """Import symptoms and diseases from ML dataset"""
    
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        # Get backend directory (parent of app directory)
        # File is at: backend/scripts/import_dataset.py
        # So parent.parent = backend/
        backend_dir = Path(__file__).parent.parent
        
        # ML directory is at root level (same level as backend/)
        # So we go up from backend/ to root, then into ml/
        project_root = backend_dir.parent
        self.ml_dir = project_root / "ml"
        self.data_dir = self.ml_dir / "data"
        self.processed_data_path = self.data_dir / "processed" / "processed_dataset.csv"
        self.metadata_path = self.ml_dir / "models" / "model_metadata.json"
        
        # Save reference data in backend/app/db directory
        self.reference_data_path = backend_dir / "app" / "db" / "reference_data.json"
        
        # Log paths for debugging
        logger.debug(f"Backend dir: {backend_dir}")
        logger.debug(f"ML dir: {self.ml_dir}")
        logger.debug(f"Processed data path: {self.processed_data_path}")
        logger.debug(f"Metadata path: {self.metadata_path}")
        logger.debug(f"Reference data path: {self.reference_data_path}")
    
    def extract_from_processed_dataset(self) -> tuple[Set[str], Set[str]]:
        """
        Extract symptoms and diseases from processed dataset CSV
        
        Returns:
            tuple: (set of symptoms, set of diseases)
        """
        if not self.processed_data_path.exists():
            logger.warning(f"Processed dataset not found at {self.processed_data_path}")
            return set(), set()
        
        try:
            logger.info(f"Loading processed dataset from {self.processed_data_path}")
            df = pd.read_csv(self.processed_data_path)
            
            # Normalize column names
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Identify target column (disease/prognosis)
            target_columns = ['disease', 'prognosis']
            target_col = None
            for col in target_columns:
                if col in df.columns:
                    target_col = col
                    break
            
            if target_col is None:
                target_col = df.columns[-1]
                logger.warning(f"No standard target column found, using '{target_col}' as target")
            
            # Get diseases (unique values from target column)
            diseases = set(df[target_col].dropna().unique())
            logger.info(f"Found {len(diseases)} unique diseases")
            
            # Get symptoms (all columns except target)
            symptom_columns = [col for col in df.columns if col != target_col]
            symptoms = set(symptom_columns)
            logger.info(f"Found {len(symptoms)} unique symptoms")
            
            return symptoms, diseases
            
        except Exception as e:
            logger.error(f"Error extracting data from processed dataset: {e}")
            return set(), set()
    
    def extract_from_metadata(self) -> tuple[List[str], List[str]]:
        """
        Extract symptoms and diseases from model metadata JSON
        
        Returns:
            tuple: (list of symptoms/features, list of diseases/classes)
        """
        if not self.metadata_path.exists():
            logger.warning(f"Model metadata not found at {self.metadata_path}")
            return [], []
        
        try:
            logger.info(f"Loading model metadata from {self.metadata_path}")
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Get feature names (symptoms)
            features = metadata.get('feature_names', [])
            logger.info(f"Found {len(features)} features in metadata")
            
            # Get disease classes
            classes = metadata.get('classes', [])
            logger.info(f"Found {len(classes)} disease classes in metadata")
            
            return features, classes
            
        except Exception as e:
            logger.error(f"Error extracting data from metadata: {e}")
            return [], []
    
    def get_reference_data(self) -> Optional[Dict]:
        """Load reference data from JSON file"""
        if not self.reference_data_path.exists():
            return None
        
        try:
            with open(self.reference_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading reference data: {e}")
            return None
    
    def import_data(self) -> bool:
        """
        Import symptoms and diseases from dataset to database
        
        Returns:
            bool: True if import was successful, False otherwise
        """
        logger.info("Starting data import from ML dataset...")
        
        # Check if database session is available
        if not self.db:
            logger.error("Database session is required for importing to database")
            return False
        
        # Load reference data once at the beginning
        reference_data = self.get_reference_data()
        disease_recommendations = {}
        symptoms_from_json = []
        diseases_from_json = []
        
        if reference_data:
            logger.info("Loading data from existing reference_data.json")
            symptoms_from_json = reference_data.get('symptoms', [])
            diseases_from_json = reference_data.get('diseases', [])
            disease_recommendations = reference_data.get('disease_recommendations', {})
        
        # Check if data already exists in database
        existing_symptoms = self.db.query(Symptom).count()
        existing_diseases = self.db.query(Disease).count()
        
        # Always update recommendations for existing diseases if available
        if existing_diseases > 0 and disease_recommendations:
            logger.info("Updating recommendations for existing diseases...")
            updated_count = 0
            for disease_name, recommendation in disease_recommendations.items():
                existing = self.db.query(Disease).filter(Disease.name == disease_name.strip()).first()
                if existing and (existing.recommendations != recommendation):
                    existing.recommendations = recommendation
                    updated_count += 1
            
            if updated_count > 0:
                self.db.commit()
                logger.info(f"Updated recommendations for {updated_count} existing diseases")
        
        if existing_symptoms > 0 or existing_diseases > 0:
            logger.info(f"Database already contains {existing_symptoms} symptoms and {existing_diseases} diseases")
            logger.info("Skipping database import. Use --force flag to re-import if needed.")
            return True
        if symptoms_from_json and diseases_from_json:
            symptoms = symptoms_from_json
            diseases = diseases_from_json
            source = "reference_data.json"
        else:
            logger.error("No data source available for import")
            logger.info("Please ensure either:")
            logger.info(f"  1. Processed dataset exists at: {self.processed_data_path}")
            logger.info(f"  2. Model metadata exists at: {self.metadata_path}")
            logger.info(f"  3. Reference data exists at: {self.reference_data_path}")
            return False
        
        # Import to database
        try:
            logger.info(f"Importing {len(symptoms)} symptoms and {len(diseases)} diseases to database...")
            
            # Import symptoms
            symptom_objects = []
            for symptom_name in symptoms:
                # Check if symptom already exists
                existing = self.db.query(Symptom).filter(Symptom.name == symptom_name).first()
                if not existing:
                    symptom_obj = Symptom(
                        name=symptom_name,
                        description=None  # Can be filled later if needed
                    )
                    symptom_objects.append(symptom_obj)
            
            if symptom_objects:
                self.db.add_all(symptom_objects)
                logger.info(f"Added {len(symptom_objects)} new symptoms to database")
            
            # Import diseases
            disease_objects = []
            updated_count = 0
            for disease_name in diseases:
                disease_name_clean = disease_name.strip()
                # Check if disease already exists
                existing = self.db.query(Disease).filter(Disease.name == disease_name_clean).first()
                
                # Get recommendation from reference data if available
                recommendation = disease_recommendations.get(disease_name, None)
                
                if not existing:
                    # Create new disease
                    disease_obj = Disease(
                        name=disease_name_clean,
                        description=None,  # Can be filled later if needed
                        severity=None,
                        precautions=None,
                        recommendations=recommendation
                    )
                    disease_objects.append(disease_obj)
                else:
                    # Update existing disease with recommendation if it's missing or different
                    if recommendation and (existing.recommendations != recommendation):
                        existing.recommendations = recommendation
                        updated_count += 1
            
            if disease_objects:
                self.db.add_all(disease_objects)
                logger.info(f"Added {len(disease_objects)} new diseases to database")
            
            if updated_count > 0:
                logger.info(f"Updated recommendations for {updated_count} existing diseases")
            
            # Commit changes
            self.db.commit()
            
            logger.success(f"Data imported successfully from {source}")
            logger.info(f"  - Symptoms imported: {len(symptom_objects)}")
            logger.info(f"  - Diseases imported: {len(disease_objects)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error importing data to database: {e}")
            self.db.rollback()
            import traceback
            logger.debug(traceback.format_exc())
            return False


def import_dataset_data(db: Optional[Session] = None) -> bool:
    """
    Import dataset data to database if not already imported
    
    Args:
        db: Database session (required for database import)
        
    Returns:
        bool: True if import was successful or already exists, False otherwise
    """
    # Create importer
    importer = DatasetImporter(db)
    
    # Import to database (will check if data exists)
    logger.info("Checking if dataset data needs to be imported to database...")
    return importer.import_data()


def run_import(db: Optional[Session] = None) -> bool:
    """
    Run dataset data import to database
    
    Args:
        db: Optional database session. If None, creates a new session.
        
    Returns:
        bool: True if import was successful, False otherwise
    """
    logger.info("Starting dataset data import to database...")
    
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    
    try:
        success = import_dataset_data(db)
        if success:
            logger.success("Dataset data import completed successfully!")
            return True
        else:
            logger.error("Dataset data import failed!")
            logger.info("Check the logs above for details on what went wrong.")
            return False
    except Exception as e:
        logger.error(f"Error during data import: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return False
    finally:
        if should_close:
            db.close()


def main() -> int:
    """Main function for command-line execution"""
    db = SessionLocal()
    try:
        success = run_import(db)
        return 0 if success else 1
    finally:
        db.close()


if __name__ == "__main__":
    # Setup logging
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    sys.exit(main())
