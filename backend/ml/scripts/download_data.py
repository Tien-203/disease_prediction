"""Download disease-symptom dataset from Kaggle using kagglehub"""
import kagglehub
import shutil
from pathlib import Path
from loguru import logger
import sys


def download_disease_symptom_dataset():
    """
    Download disease-symptom dataset from Kaggle
    
    This script downloads a disease-symptom dataset from Kaggle.
    Common datasets include:
    - itachi9604/disease-symptom-description-dataset
    - kaushil268/disease-prediction-using-machine-learning
    """
    try:
        logger.info("Downloading disease-symptom dataset from Kaggle...")
        
        # Download dataset using kagglehub
        # You can change this to any other disease-symptom dataset on Kaggle
        dataset_name = "itachi9604/disease-symptom-description-dataset"
        
        logger.info(f"Dataset: {dataset_name}")
        path = kagglehub.dataset_download(dataset_name)
        
        logger.info(f"Dataset downloaded to: {path}")
        
        # Setup directories
        current_dir = Path(__file__).parent.parent
        raw_data_dir = current_dir / "data" / "raw"
        raw_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files to our data directory
        downloaded_path = Path(path)
        for file in downloaded_path.glob("*"):
            if file.is_file():
                dest = raw_data_dir / file.name
                shutil.copy2(file, dest)
                logger.info(f"Copied {file.name} to {raw_data_dir}")
        
        logger.success("Dataset downloaded and copied successfully!")
        logger.info(f"Data location: {raw_data_dir}")
        
        # List downloaded files
        logger.info("\nDownloaded files:")
        for file in raw_data_dir.glob("*"):
            if file.is_file():
                logger.info(f"  - {file.name} ({file.stat().st_size / 1024:.2f} KB)")
        
        return raw_data_dir
        
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        logger.info("\nNote: Make sure you have:")
        logger.info("1. Kaggle account and API credentials configured")
        logger.info("2. kagglehub installed (pip install kagglehub)")
        logger.info("3. Kaggle API key set up (~/.kaggle/kaggle.json)")
        sys.exit(1)


if __name__ == "__main__":
    # Setup logging
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    download_disease_symptom_dataset()
