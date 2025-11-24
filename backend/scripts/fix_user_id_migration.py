"""Script to make user_id nullable in predictions table"""
import sys
from pathlib import Path

# Add backend directory to Python path when run as script
if __name__ == "__main__":
    backend_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.db.session import SessionLocal
from loguru import logger

def fix_user_id_nullable():
    """Make user_id column nullable in predictions table"""
    db = SessionLocal()
    try:
        logger.info("Making user_id nullable in predictions table...")
        
        # Check if column is already nullable
        result = db.execute(text("""
            SELECT is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'predictions' 
            AND column_name = 'user_id'
        """))
        
        row = result.fetchone()
        if row and row[0] == 'YES':
            logger.info("user_id is already nullable. No changes needed.")
            return True
        
        # Make user_id nullable
        db.execute(text("ALTER TABLE predictions ALTER COLUMN user_id DROP NOT NULL"))
        db.commit()
        
        logger.success("Successfully made user_id nullable in predictions table")
        return True
    except Exception as e:
        logger.error(f"Error making user_id nullable: {e}")
        db.rollback()
        import traceback
        logger.error(traceback.format_exc())
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = fix_user_id_nullable()
    sys.exit(0 if success else 1)

