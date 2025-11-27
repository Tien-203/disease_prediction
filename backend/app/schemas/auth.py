"""Authentication schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime


UserRole = Literal["patient", "doctor", "researcher", "data_scientist"]


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: UserRole = Field("patient", description="Role assigned to the user")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    role: Optional[UserRole] = Field(
        None,
        description="Expected role for the session. When provided it must match the user role."
    )


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[int] = None


class AuthResponse(BaseModel):
    """Authentication response schema"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None



