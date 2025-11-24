"""Data preprocessing script with symptom groups"""
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
import sys
from typing import Dict, List


def get_symptom_group_mapping() -> Dict[str, str]:
    """
    Get mapping of symptom names to their groups
    This matches the grouping logic in symptom_service.py
    
    Returns:
        Dictionary mapping symptom name (lowercase) to group name
    """
    # Define symptom categories based on common characteristics
    # This matches the categories in backend/app/services/symptom_service.py
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
    
    # Create mapping from symptom name to group
    symptom_to_group: Dict[str, str] = {}
    
    # Map each symptom to its group based on keywords
    for group_name, keywords in categories.items():
        for keyword in keywords:
            symptom_to_group[keyword] = group_name
    
    return symptom_to_group, categories


def map_symptom_to_group(symptom_name: str, categories: Dict[str, List[str]]) -> str:
    """
    Map a symptom name to its group
    
    Args:
        symptom_name: Name of the symptom
        categories: Dictionary of group names to keywords
        
    Returns:
        Group name or "other" if no match found
    """
    symptom_lower = symptom_name.lower().strip().replace(' ', '_')
    
    # Check each category
    for group_name, keywords in categories.items():
        # Check if any keyword matches the symptom name
        if any(keyword in symptom_lower for keyword in keywords):
            return group_name
    
    # If no match, return "other"
    return "other"


def preprocess_disease_data_with_groups(input_file: str, output_file: str):
    """
    Preprocess disease-symptom dataset using symptom groups instead of individual symptoms
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to save processed CSV file
    """
    logger.info(f"Loading data from {input_file}...")
    
    try:
        # Load the dataset
        df = pd.read_csv(input_file)
        
        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        
        # Normalize column names first
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Identify target column (disease/prognosis)
        target_columns = ['disease', 'prognosis']
        target_col = None
        for col in target_columns:
            if col in df.columns:
                target_col = col
                break
        
        if target_col is None:
            # Use last column as target
            target_col = df.columns[-1]
            logger.warning(f"No standard target column found, using '{target_col}' as target")
        
        # Get symptom columns (all columns except target)
        symptom_columns = [col for col in df.columns if col != target_col]
        logger.info(f"Found {len(symptom_columns)} symptom columns")
        
        # Remove rows with missing disease labels
        initial_shape = df.shape
        df = df.dropna(subset=[target_col])
        logger.info(f"Shape after removing missing diseases: {df.shape} (removed {initial_shape[0] - df.shape[0]} rows)")
        
        # Get group mapping
        symptom_to_group, categories = get_symptom_group_mapping()
        
        # Define all 13 groups (12 defined + "other")
        all_groups = list(categories.keys()) + ["other"]
        logger.info(f"Using {len(all_groups)} symptom groups: {all_groups}")
        
        # Create group-based feature matrix - each column will contain symptom names
        logger.info("Creating group-based feature matrix with symptom names...")
        # Initialize with empty strings
        group_features = pd.DataFrame('', index=df.index, columns=all_groups)
        
        # Process each row
        for idx, row in df.iterrows():
            # Track symptoms for each group
            group_symptoms: Dict[str, List[str]] = {group: [] for group in all_groups}
            
            # Check each symptom column
            for col in symptom_columns:
                symptom_val = str(row[col]).strip() if pd.notna(row[col]) else ''
                # If symptom is present (not 0, NaN, or empty)
                if symptom_val and symptom_val != '0' and symptom_val.lower() != 'nan':
                    # Map symptom to group
                    group = map_symptom_to_group(symptom_val, categories)
                    # Add symptom name to the group's list
                    if group in group_symptoms:
                        group_symptoms[group].append(symptom_val)
            
            # Store symptom names for each group (comma-separated)
            # Normalize and sort to ensure consistent format
            for group in all_groups:
                if group_symptoms[group]:
                    # Normalize symptom names: strip, lowercase, and replace spaces with underscores
                    # This ensures consistent format matching inference
                    normalized = []
                    for s in group_symptoms[group]:
                        # Normalize: strip whitespace, lowercase, replace spaces with underscores
                        norm = s.strip().lower().replace(' ', '_')
                        if norm:
                            normalized.append(norm)
                    normalized = sorted(set(normalized))  # Sort and remove duplicates
                    # Join symptom names with comma (no spaces)
                    group_features.loc[idx, group] = ','.join(normalized)
                else:
                    # Empty string if no symptoms in this group
                    group_features.loc[idx, group] = ''
        
        # Combine disease column with group features
        processed_df = pd.concat([df[[target_col]], group_features], axis=1)
        
        logger.info(f"Processed dataset shape: {processed_df.shape}")
        logger.info(f"Features: {len(group_features.columns)} group-based features")
        logger.info(f"Group features: {list(group_features.columns)}")
        
        # Save processed data
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(output_path, index=False)
        
        logger.success(f"Processed data saved to {output_path}")
        
        # Display statistics
        logger.info("\nDataset statistics:")
        logger.info(f"Number of unique diseases: {processed_df[target_col].nunique()}")
        logger.info(f"Number of group features: {len(group_features.columns)}")
        logger.info(f"Group feature distribution:")
        for group in all_groups:
            # Count non-empty values
            count = (group_features[group] != '').sum()
            percentage = (count / len(group_features)) * 100
            logger.info(f"  {group}: {count} rows ({percentage:.1f}%)")
        
        logger.info(f"\nDisease distribution:")
        print(processed_df[target_col].value_counts().head(10))
        
        return processed_df
        
    except Exception as e:
        logger.error(f"Error preprocessing data: {e}")
        raise


if __name__ == "__main__":
    # Setup logging
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Paths
    base_dir = Path(__file__).parent.parent
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    
    # Find CSV files in raw directory
    csv_files = list(raw_dir.glob("*.csv"))
    
    if not csv_files:
        logger.error(f"No CSV files found in {raw_dir}")
        logger.info("Please run download_data.py first")
        sys.exit(1)
    
    logger.info(f"Found {len(csv_files)} CSV file(s)")
    
    # Process the first dataset file (usually dataset.csv or similar)
    input_file = csv_files[0]
    output_file = processed_dir / "processed_dataset_with_groups.csv"
    
    logger.info(f"Processing {input_file.name} with symptom groups...")
    preprocess_disease_data_with_groups(str(input_file), str(output_file))


