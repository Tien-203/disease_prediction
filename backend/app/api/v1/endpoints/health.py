"""Health check endpoint"""
import traceback
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from loguru import logger

from app.api.deps import get_db
from app.schemas.common import HealthCheckResponse
from app.core.config import settings
from app.ml.model_loader import model_loader

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    
    Returns the health status of the application including:
    - Application status
    - Database connectivity
    - ML model availability
    """
    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Database connection error: {e}\n{traceback_str}")
        db_status = "disconnected"
    
    # Check ML model
    ml_status = "loaded" if model_loader.is_loaded() else "not loaded"
    
    return HealthCheckResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        database=db_status,
        ml_model=ml_status
    )
