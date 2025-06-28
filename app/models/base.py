"""
Base SQLAlchemy models with common patterns.
"""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    """Base class for all database models."""
    
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampMixin:
    """Mixin to add timestamp columns."""
    
    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )


class UUIDMixin:
    """Mixin to add UUID primary key."""
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )