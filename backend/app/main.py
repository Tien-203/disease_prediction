"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from sqlalchemy import text

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.ml.model_loader import model_loader

# Import the import script function
import sys
from pathlib import Path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))
from import_dataset import run_import


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application
    Handles startup and shutdown events
    """
    # Setup logging first
    setup_logging()
    
    # Startup
    logger.info("Starting Disease Prediction API...")
    
    # Create database tables
    try:
        # Test database connection first
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
        
        # Import dataset data to database if not already imported
        try:
            db = SessionLocal()
            try:
                run_import(db)
            except Exception as import_error:
                logger.warning(f"Could not import dataset data: {import_error}")
                logger.info("Application will continue, but symptom/disease lists may not be available")
                import traceback
                logger.debug(traceback.format_exc())
            finally:
                db.close()
        except Exception as db_error:
            logger.warning(f"Could not access database for data import: {db_error}")
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "could not connect" in error_msg.lower():
            logger.warning(
                "⚠️  PostgreSQL is not running or not accessible. "
                "Please ensure PostgreSQL is running and accessible at the configured DATABASE_URL. "
                "The application will start but database operations will fail."
            )
            logger.info(f"Attempted connection to: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured database'}")
        else:
            logger.error(f"Error creating database tables: {e}")
        logger.info("Application will continue to start, but database features will be unavailable")
    
    # Load ML models
    logger.info("Loading ML models...")
    try:
        success = model_loader.load_models(
            model_path=settings.MODEL_PATH,
            label_encoder_path=settings.LABEL_ENCODER_PATH,
            feature_names_path=settings.FEATURE_NAMES_PATH
        )
        if success:
            logger.info("ML models loaded successfully")
        else:
            logger.warning(
                "ML models not loaded. "
                "Please train the model using ml/scripts/train_model.py"
            )
    except Exception as e:
        logger.error(f"Error loading ML models: {e}")
        logger.warning("Application will start but predictions will not be available")
    
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Disease Prediction API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for disease prediction based on symptoms using Machine Learning",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": f"{settings.API_V1_PREFIX}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

