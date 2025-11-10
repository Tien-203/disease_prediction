#!/usr/bin/env python3
"""
Migration check script for Docker
Checks if database migrations are up to date and runs them if needed
"""
import sys
import subprocess
from pathlib import Path
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine
from app.core.config import settings

# Import all models for Alembic autogenerate
from app.models import User, Prediction  # noqa
# Import other models directly if needed
from app.models.symptom import Symptom  # noqa
from app.models.disease import Disease  # noqa


def get_current_revision(engine):
    """Get current database revision"""
    try:
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_rev = context.get_current_revision()
            return current_rev
    except Exception as e:
        logger.warning(f"Could not get current revision (database might be empty): {e}")
        return None


def get_head_revision(alembic_cfg):
    """Get head revision from Alembic"""
    script = ScriptDirectory.from_config(alembic_cfg)
    head_rev = script.get_current_head()
    return head_rev


def run_migrations():
    """Run Alembic migrations to head"""
    try:
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.success("Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False


def check_and_migrate():
    """Check if migrations are needed and run them"""
    try:
        logger.info("Checking database migration status...")
        
        # Create database engine
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        
        # Get current and head revisions
        current_rev = get_current_revision(engine)
        alembic_cfg = Config("alembic.ini")
        head_rev = get_head_revision(alembic_cfg)
        
        logger.info(f"Current revision: {current_rev or 'None (empty database)'}")
        logger.info(f"Head revision: {head_rev}")
        
        # Check if migration is needed
        if current_rev == head_rev:
            logger.info("Database is up to date. No migrations needed.")
            return True
        
        # Run migrations
        logger.info("Database is not at head. Running migrations...")
        return run_migrations()
        
    except Exception as e:
        logger.error(f"Error checking migrations: {e}")
        return False


if __name__ == "__main__":
    # Setup logging
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    success = check_and_migrate()
    sys.exit(0 if success else 1)

