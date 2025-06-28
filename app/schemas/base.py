"""
Base Pydantic schemas for common patterns.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for models with timestamp fields."""
    
    created_at: datetime
    updated_at: datetime


class IDMixin(BaseModel):
    """Mixin for models with ID field."""
    
    id: UUID