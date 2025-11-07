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
        
        # Handle missing values
        logger.info("\nHandling missing values...")
        initial_shape = df.shape
        
        # Replace NaN with 0 for symptom columns (assuming binary encoding)
        symptom_columns = [col for col in df.columns if col != 'Disease' and col != 'prognosis']
        df[symptom_columns] = df[symptom_columns].fillna(0)
        
        # Remove rows with missing disease labels
        if 'Disease' in df.columns:
            df = df.dropna(subset=['Disease'])
        elif 'prognosis' in df.columns:
            df = df.dropna(subset=['prognosis'])
        
        logger.info(f"Shape after cleaning: {df.shape} (removed {initial_shape[0] - df.shape[0]} rows)")
        
        # Normalize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Save processed data
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        
        logger.success(f"Processed data saved to {output_path}")
        
        # Display statistics
        logger.info("\nDataset statistics:")
        if 'disease' in df.columns:
            disease_col = 'disease'
        elif 'prognosis' in df.columns:
            disease_col = 'prognosis'
        else:
            disease_col = df.columns[-1]
        
        logger.info(f"Number of unique diseases: {df[disease_col].nunique()}")
        logger.info(f"Disease distribution:")
        print(df[disease_col].value_counts())
        
        return df
        
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
