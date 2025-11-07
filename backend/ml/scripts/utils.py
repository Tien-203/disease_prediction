"""Utility functions for ML scripts"""
import json
from pathlib import Path
from loguru import logger


def save_model_metadata(
    metadata: dict,
    output_path: str
):
    """
    Save model metadata to JSON file
    
    Args:
        metadata: Dictionary containing model metadata
        output_path: Path to save the metadata file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Model metadata saved to {output_path}")


def load_model_metadata(metadata_path: str) -> dict:
    """
    Load model metadata from JSON file
    
    Args:
        metadata_path: Path to metadata file
        
    Returns:
        Dictionary containing model metadata
    """
    metadata_path = Path(metadata_path)
    
    if not metadata_path.exists():
        logger.warning(f"Metadata file not found: {metadata_path}")
        return {}
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    logger.info(f"Model metadata loaded from {metadata_path}")
    return metadata


def ensure_dir(directory: str):
    """
    Ensure directory exists
    
    Args:
        directory: Directory path to create
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
