"""Authentication endpoints"""
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from loguru import logger

from app.api.deps import get_db, get_current_user
from app.schemas.auth import (
    UserLogin,
    UserCreate,
    AuthResponse,
    Token,
    UserResponse,
    UserUpdate
)
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return access token
    
    Args:
        user_credentials: User email and password
        
    Returns:
        Access token and user information
    """
    try:
        auth_service = AuthService(db)
        
        # Authenticate user
        user = auth_service.authenticate_user(
            email=user_credentials.email,
            password=user_credentials.password,
            role=user_credentials.role
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        # Convert user to response schema
        user_response = auth_service.to_user_response(user)
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error during login for email {user_credentials.email}: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )


@router.post("/register", response_model=AuthResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    Args:
        user_data: User registration data
        
    Returns:
        Access token and user information
    """
    auth_service = AuthService(db)
    
    try:
        # Create user
        try:
            user = auth_service.create_user(user_data)
        except HTTPException:
            raise
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error creating user with email {user_data.email}: {str(e)}\n{traceback_str}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        # Convert user to response schema
        user_response = auth_service.to_user_response(user)
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error during registration: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during registration: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Current user information
    """
    auth_service = AuthService(db)
    return auth_service.to_user_response(current_user)


@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    Args:
        user_update: User profile update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated user information
    """
    try:
        auth_service = AuthService(db)
        
        # Convert Pydantic model to dict, excluding None values
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Update user
        updated_user = auth_service.update_user(current_user, update_data)
        
        # Return updated user
        return auth_service.to_user_response(updated_user)
    except HTTPException:
        raise
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error updating user profile: {str(e)}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )



