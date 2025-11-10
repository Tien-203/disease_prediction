"""Application configuration using Pydantic Settings"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://disease_user:disease_password@localhost:5432/disease_prediction",
        description="PostgreSQL database URL"
    )
    
    # Application
    APP_NAME: str = Field(default="Disease Prediction API", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=True, description="Debug mode")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    
    # ML Model paths
    MODEL_PATH: str = Field(default="ml/models/random_forest_model.pkl", description="ML model path")
    LABEL_ENCODER_PATH: str = Field(default="ml/models/label_encoder.pkl", description="Label encoder path")
    FEATURE_NAMES_PATH: str = Field(default="ml/models/feature_names.pkl", description="Feature names path")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:4200"],
        description="Allowed CORS origins"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # JWT Authentication
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production-use-openssl-rand-hex-32",
        description="Secret key for JWT token signing"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration in minutes")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env file
    )


# Global settings instance
settings = Settings()

