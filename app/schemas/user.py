"""
User-related Pydantic schemas.
"""
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, Field

from .base import BaseSchema, IDMixin, TimestampMixin


class UserBase(BaseSchema):
    """Base user schema with common fields."""
    
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    is_active: bool = Field(default=True, description="Whether the user account is active")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, max_length=128, description="User's password")


class UserUpdate(BaseSchema):
    """Schema for updating user information."""
    
    email: Optional[EmailStr] = Field(None, description="User's email address")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    is_active: Optional[bool] = Field(None, description="Whether the user account is active")


class UserResponse(UserBase, IDMixin, TimestampMixin):
    """Schema for user responses (excludes sensitive data)."""
    
    pass


class UserInDB(UserResponse):
    """Schema for user as stored in database."""
    
    hashed_password: str = Field(..., description="User's hashed password")