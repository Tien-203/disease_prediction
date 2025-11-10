"""User database model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    """User model for storing user accounts and authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    role = Column(String(50), nullable=False, default="patient", index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    
    # Add check constraint for role
    __table_args__ = (
        CheckConstraint(
            "role IN ('patient', 'doctor', 'researcher', 'data_scientist')",
            name="check_user_role"
        ),
        CheckConstraint("age >= 0 AND age <= 150", name="check_user_age"),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

