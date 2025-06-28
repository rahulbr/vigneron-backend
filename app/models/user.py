"""
User SQLAlchemy model.
"""
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """User model."""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    ai_models = relationship("AIModel", back_populates="owner", cascade="all, delete-orphan")
    inference_requests = relationship("InferenceRequest", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"