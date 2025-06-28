"""
Inference Request SQLAlchemy model.
"""
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, UUIDMixin


class InferenceRequest(Base, UUIDMixin, TimestampMixin):
    """Inference Request model."""
    
    __tablename__ = "inference_requests"
    
    # Request information
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False, index=True)
    
    # Input data
    input_type = Column(String(20), nullable=False, index=True)
    text_input = Column(Text)
    json_input = Column(JSON)
    file_url = Column(String(500))
    
    # Processing options and configuration
    options = Column(JSON, default=dict)
    callback_url = Column(String(500))
    
    # Status and processing information
    status = Column(String(20), default="pending", nullable=False, index=True)
    processing_time_ms = Column(Integer)
    
    # Results
    output = Column(JSON)
    confidence = Column(String(10))  # Stored as string to handle various formats
    request_metadata = Column(JSON, default=dict)
    
    # Error information
    error_message = Column(Text)
    error_code = Column(String(50))
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="inference_requests")
    model = relationship("AIModel", back_populates="inference_requests")
    
    def __repr__(self) -> str:
        return f"<InferenceRequest(id={self.id}, status={self.status}, model_id={self.model_id})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if the request is in a completed state."""
        return self.status in ["completed", "failed", "cancelled"]
    
    @property
    def duration_ms(self) -> int:
        """Calculate total duration from creation to completion."""
        if not self.completed_at:
            return 0
        delta = self.completed_at - self.created_at
        return int(delta.total_seconds() * 1000)