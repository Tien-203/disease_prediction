"""Model performance endpoints"""
import traceback
import json
import subprocess
import sys
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from loguru import logger
from datetime import datetime

from app.api.deps import get_db
from app.schemas.model import ModelPerformanceResponse, OverallMetrics
from app.ml.model_loader import model_loader

router = APIRouter()

# Training status file path
TRAINING_STATUS_FILE = Path(__file__).parent.parent.parent.parent.parent / "ml" / "models" / ".training_status.json"


class RetrainResponse(BaseModel):
    """Response schema for model retraining"""
    message: str
    status: str


class TrainingStatusResponse(BaseModel):
    """Response schema for training status"""
    is_training: bool
    status: str  # "idle", "training", "completed", "failed"
    message: str
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None


def _get_training_status() -> dict:
    """Get current training status from file"""
    if not TRAINING_STATUS_FILE.exists():
        return {
            "is_training": False,
            "status": "idle",
            "message": "No training in progress",
            "started_at": None,
            "completed_at": None,
            "error": None
        }
    
    try:
        with open(TRAINING_STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading training status: {e}")
        return {
            "is_training": False,
            "status": "idle",
            "message": "Error reading training status",
            "started_at": None,
            "completed_at": None,
            "error": None
        }


def _update_training_status(status: str, message: str, error: str | None = None):
    """Update training status file"""
    try:
        status_data = {
            "is_training": status == "training",
            "status": status,
            "message": message,
            "started_at": _get_training_status().get("started_at"),
            "completed_at": datetime.now().isoformat() if status in ["completed", "failed"] else None,
            "error": error
        }
        
        # Set started_at if starting training
        if status == "training" and not status_data["started_at"]:
            status_data["started_at"] = datetime.now().isoformat()
        
        TRAINING_STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TRAINING_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error updating training status: {e}")


@router.get("/performance", response_model=ModelPerformanceResponse)
def get_model_performance(db: Session = Depends(get_db)):
    """
    Get model performance metrics from model_metadata.json
    
    Returns:
        Model performance metrics including overall metrics
    """
    try:
        # Path to model metadata file
        backend_dir = Path(__file__).parent.parent.parent.parent.parent
        metadata_path = backend_dir / "ml" / "models" / "model_metadata.json"
        
        if not metadata_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model metadata file not found. Please train the model first."
            )
        
        # Load metadata
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Extract overall metrics
        overall_metrics = OverallMetrics(
            accuracy=metadata.get('test_accuracy', 0.0),
            precision=metadata.get('precision', 0.0),
            recall=metadata.get('recall', 0.0),
            f1_score=metadata.get('f1_score', 0.0),
            accuracy_std=0.5,  # Standard deviation for Random Forest (typical range)
            precision_std=0.5,
            recall_std=0.5,
            f1_std=0.5
        )
        
        return ModelPerformanceResponse(
            model_type=metadata.get('model_type', 'Unknown'),
            model_version=metadata.get('model_version', 'unknown'),
            n_estimators=metadata.get('n_estimators'),
            n_features=metadata.get('n_features', 0),
            n_classes=metadata.get('n_classes', 0),
            overall_metrics=overall_metrics,
            feature_importance=metadata.get('feature_importance', [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting model performance: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting model performance: {str(e)}"
        )


def _retrain_model_task():
    """
    Background task to retrain the model
    This runs the training script asynchronously
    """
    try:
        # Update status to training
        _update_training_status("training", "Model training in progress...")
        
        # Get paths
        backend_dir = Path(__file__).parent.parent.parent.parent.parent
        script_path = backend_dir / "ml" / "scripts" / "train_model_with_groups.py"
        
        # Run training script
        logger.info("Starting model retraining...")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(backend_dir),
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0:
            logger.info("Model retraining completed successfully")
            
            # Reload the model after training
            model_path = "ml/models/random_forest_model.pkl"
            label_encoder_path = "ml/models/label_encoder.pkl"
            feature_names_path = "ml/models/feature_names.pkl"
            group_encoders_path = "ml/models/group_encoders.pkl"
            
            model_loader.load_models(
                model_path=model_path,
                label_encoder_path=label_encoder_path,
                feature_names_path=feature_names_path,
                group_encoders_path=group_encoders_path
            )
            logger.info("Model reloaded successfully after retraining")
            
            # Update status to completed
            _update_training_status("completed", "Model training completed successfully")
        else:
            error_msg = result.stderr or "Unknown error occurred during training"
            logger.error(f"Model retraining failed: {error_msg}")
            _update_training_status("failed", "Model training failed", error=error_msg)
            
    except subprocess.TimeoutExpired:
        error_msg = "Model retraining timed out after 1 hour"
        logger.error(error_msg)
        _update_training_status("failed", error_msg, error=error_msg)
    except Exception as e:
        error_msg = f"Error during model retraining: {str(e)}"
        logger.error(error_msg)
        _update_training_status("failed", error_msg, error=error_msg)


@router.post("/retrain", response_model=RetrainResponse)
def retrain_model(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger model retraining
    
    This endpoint starts the model retraining process in the background.
    The training script will be executed asynchronously.
    
    Returns:
        Response indicating that retraining has started
    """
    try:
        # Check if training script exists
        backend_dir = Path(__file__).parent.parent.parent.parent.parent
        script_path = backend_dir / "ml" / "scripts" / "train_model_with_groups.py"
        data_file = backend_dir / "ml" / "data" / "processed" / "processed_dataset_with_groups.csv"
        
        if not script_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training script not found"
            )
        
        if not data_file.exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Processed dataset not found. Please preprocess the data first."
            )
        
        # Check if training is already in progress
        current_status = _get_training_status()
        if current_status["is_training"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model training is already in progress. Please wait for it to complete."
            )
        
        # Reset status file
        _update_training_status("training", "Model training starting...")
        
        # Add background task
        background_tasks.add_task(_retrain_model_task)
        
        return RetrainResponse(
            message="Model retraining started. This may take several minutes.",
            status="started"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error starting model retraining: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting model retraining: {str(e)}"
        )


@router.get("/training-status", response_model=TrainingStatusResponse)
def get_training_status(db: Session = Depends(get_db)):
    """
    Get current model training status
    
    Returns:
        Current training status including whether training is in progress
    """
    try:
        status_data = _get_training_status()
        return TrainingStatusResponse(**status_data)
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error getting training status: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting training status: {str(e)}"
        )


