"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base
from app.ml.model_loader import model_loader


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting Disease Prediction API...")
    
    # Setup logging
    setup_logging()
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    
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

