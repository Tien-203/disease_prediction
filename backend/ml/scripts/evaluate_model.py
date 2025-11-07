"""Evaluate trained model"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
from loguru import logger
import sys
import json


def evaluate_model(models_dir: str, data_file: str):
    """
    Evaluate trained model
    
    Args:
        models_dir: Directory containing trained models
        data_file: Path to test dataset
    """
    models_path = Path(models_dir)
    
    # Load models
    logger.info("Loading models...")
    model = joblib.load(models_path / "random_forest_model.pkl")
    label_encoder = joblib.load(models_path / "label_encoder.pkl")
    feature_names = joblib.load(models_path / "feature_names.pkl")
    
    # Load metadata
    with open(models_path / "model_metadata.json", 'r') as f:
        metadata = json.load(f)
    
    logger.info("\nModel Information:")
    logger.info(f"Model Type: {metadata['model_type']}")
    logger.info(f"Number of Features: {metadata['n_features']}")
    logger.info(f"Number of Classes: {metadata['n_classes']}")
    logger.info(f"Test Accuracy: {metadata['test_accuracy']:.4f}")
    logger.info(f"Precision: {metadata['precision']:.4f}")
    logger.info(f"Recall: {metadata['recall']:.4f}")
    logger.info(f"F1-Score: {metadata['f1_score']:.4f}")
    
    logger.info("\nTop 10 Important Features:")
    for i, feature in enumerate(metadata['top_10_features'][:10], 1):
        logger.info(f"{i}. {feature['feature']}: {feature['importance']:.4f}")
    
    logger.info(f"\nAll diseases ({len(metadata['classes'])}):")
    for i, disease in enumerate(metadata['classes'], 1):
        print(f"{i}. {disease}")


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
    models_dir = base_dir / "models"
    data_file = base_dir / "data" / "processed" / "processed_dataset.csv"
    
    if not (models_dir / "model_metadata.json").exists():
        logger.error("Model not found. Please run train_model.py first")
        sys.exit(1)
    
    evaluate_model(str(models_dir), str(data_file))
