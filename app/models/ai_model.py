"""
AI Model SQLAlchemy model.
"""
from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, UUIDMixin


class AIModel(Base, UUIDMixin, TimestampMixin):
    """AI Model model."""
    
    __tablename__ = "ai_models"
    
    # Basic information
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    model_type = Column(String(50), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    status = Column(String(20), default="draft", nullable=False, index=True)
    
    # Owner relationship
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Configuration and metadata
    config = Column(JSON, default=dict)
    model_metadata = Column(JSON, default=dict)
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    
    # Model deployment information
    model_url = Column(String(500))
    api_endpoint = Column(String(200))
    
    # Usage statistics
    total_requests = Column(Integer, default=0, nullable=False)
    successful_requests = Column(Integer, default=0, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="ai_models")
    inference_requests = relationship("InferenceRequest", back_populates="model")
    
    def __repr__(self) -> str:
        return f"<AIModel(id={self.id}, name={self.name}, version={self.version})>"
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100