"""Logging configuration using loguru"""
import sys
import logging
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging():
    """Configure loguru logger"""
    # Remove default logger
    logger.remove()
    
    # Suppress SQLAlchemy engine logging
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Add console logger with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True,
        filter=lambda record: "sqlalchemy.engine" not in record["name"].lower(),
    )
    
    # Add file logger
    logger.add(
        logs_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        filter=lambda record: "sqlalchemy.engine" not in record["name"].lower(),
    )
    
    logger.info(f"Logging configured with level: {settings.LOG_LEVEL}")
    return logger

