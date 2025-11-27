"""Authentication service"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse
from app.core.security import verify_password, get_password_hash


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def authenticate_user(self, email: str, password: str, role: str | None = None) -> User | None:
        """Authenticate user with email, password and optional role validation"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None

        if role and user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role mismatch"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name,
            age=user_data.age,
            gender=user_data.gender,
            role=user_data.role or "patient"  # Default role
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user(self, user: User, user_data: dict) -> User:
        """Update user profile information"""
        if "name" in user_data and user_data["name"] is not None:
            user.name = user_data["name"]
        if "age" in user_data and user_data["age"] is not None:
            user.age = user_data["age"]
        if "gender" in user_data and user_data["gender"] is not None:
            user.gender = user_data["gender"]
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def to_user_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse schema"""
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            age=user.age,
            gender=user.gender,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )



