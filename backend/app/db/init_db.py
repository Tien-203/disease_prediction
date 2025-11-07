"""Database initialization"""
from loguru import logger
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine
from app.models.symptom import Symptom
from app.models.disease import Disease
from app.models.prediction import Prediction


def init_db(db: Session) -> None:
    """Initialize database with base data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Check if data already exists
    symptom_count = db.query(Symptom).count()
    disease_count = db.query(Disease).count()
    
    if symptom_count > 0 or disease_count > 0:
        logger.info("Database already contains data, skipping initialization")
        return
    
    # Add sample symptoms
    sample_symptoms = [
        Symptom(name="fever", description="Elevated body temperature"),
        Symptom(name="cough", description="Frequent coughing"),
        Symptom(name="fatigue", description="Feeling of tiredness or exhaustion"),
        Symptom(name="headache", description="Pain in the head region"),
        Symptom(name="nausea", description="Feeling of sickness with an inclination to vomit"),
    ]
    
    # Add sample diseases
    sample_diseases = [
        Disease(
            name="Common Cold",
            description="A viral infection of the upper respiratory tract",
            severity="mild",
            precautions=["Rest", "Drink fluids", "Use over-the-counter medications"],
            recommendations="Most colds resolve on their own within 7-10 days"
        ),
        Disease(
            name="Influenza",
            description="A contagious respiratory illness caused by influenza viruses",
            severity="moderate",
            precautions=["Get vaccinated", "Rest", "Stay hydrated", "Isolate from others"],
            recommendations="Seek medical attention if symptoms worsen"
        ),
    ]
    
    try:
        db.add_all(sample_symptoms)
        db.add_all(sample_diseases)
        db.commit()
        logger.info(f"Added {len(sample_symptoms)} symptoms and {len(sample_diseases)} diseases")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise

