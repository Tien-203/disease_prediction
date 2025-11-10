"""Data preprocessing script"""
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
import sys


def preprocess_disease_data(input_file: str, output_file: str):
    """
    Preprocess disease-symptom dataset
    
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
        
        # Display first few rows
        logger.info("\nFirst few rows:")
        print(df.head())
        
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
        
        # Collect all unique symptom names from all symptom columns
        logger.info("Collecting unique symptoms...")
        all_symptoms = set()
        
        for col in symptom_columns:
            # Get unique values from this column, excluding NaN, 0, and empty strings
            unique_vals = df[col].dropna().unique()
            for val in unique_vals:
                # Convert to string and strip whitespace
                val_str = str(val).strip()
                # Skip if it's 0, empty, or 'nan'
                if val_str and val_str != '0' and val_str.lower() != 'nan':
                    all_symptoms.add(val_str)
        
        logger.info(f"Found {len(all_symptoms)} unique symptoms")
        
        # Create binary encoding: each symptom becomes a feature column
        logger.info("Creating binary encoding for symptoms...")
        
        # Initialize binary feature matrix
        symptom_features = pd.DataFrame(0, index=df.index, columns=sorted(all_symptoms))
        
        # Fill in the binary matrix
        for idx, row in df.iterrows():
            for col in symptom_columns:
                symptom_val = str(row[col]).strip() if pd.notna(row[col]) else ''
                # If symptom is present (not 0, NaN, or empty)
                if symptom_val and symptom_val != '0' and symptom_val.lower() != 'nan':
                    if symptom_val in symptom_features.columns:
                        symptom_features.loc[idx, symptom_val] = 1
        
        # Combine disease column with binary symptom features
        processed_df = pd.concat([df[[target_col]], symptom_features], axis=1)
        
        logger.info(f"Processed dataset shape: {processed_df.shape}")
        logger.info(f"Features: {len(symptom_features.columns)} binary symptom features")
        
        # Save processed data
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(output_path, index=False)
        
        logger.success(f"Processed data saved to {output_path}")
        
        # Display statistics
        logger.info("\nDataset statistics:")
        logger.info(f"Number of unique diseases: {processed_df[target_col].nunique()}")
        logger.info(f"Number of symptom features: {len(symptom_features.columns)}")
        logger.info(f"Disease distribution:")
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
    output_file = processed_dir / "processed_dataset.csv"
    
    logger.info(f"Processing {input_file.name}...")
    preprocess_disease_data(str(input_file), str(output_file))
