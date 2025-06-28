"""
AI Model-related Pydantic schemas.
"""
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import Field, HttpUrl

from .base import BaseSchema, IDMixin, TimestampMixin


class ModelStatus(str, Enum):
    """Enum for AI model status."""
    
    DRAFT = "draft"
    TRAINING = "training"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


class ModelType(str, Enum):
    """Enum for AI model types."""
    
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    GENERATION = "generation"
    EMBEDDING = "embedding"
    CUSTOM = "custom"


class AIModelBase(BaseSchema):
    """Base AI model schema."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Model name")
    description: Optional[str] = Field(None, max_length=500, description="Model description")
    model_type: ModelType = Field(..., description="Type of AI model")
    version: str = Field(..., min_length=1, max_length=20, description="Model version")
    status: ModelStatus = Field(default=ModelStatus.DRAFT, description="Model status")
    
    # Model configuration and metadata
    config: Dict[str, Any] = Field(default_factory=dict, description="Model configuration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Performance metrics
    accuracy: Optional[float] = Field(None, ge=0, le=1, description="Model accuracy")
    precision: Optional[float] = Field(None, ge=0, le=1, description="Model precision")
    recall: Optional[float] = Field(None, ge=0, le=1, description="Model recall")


class AIModelCreate(AIModelBase):
    """Schema for creating a new AI model."""
    
    owner_id: UUID = Field(..., description="ID of the user who owns this model")


class AIModelUpdate(BaseSchema):
    """Schema for updating AI model information."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Model name")
    description: Optional[str] = Field(None, max_length=500, description="Model description")
    status: Optional[ModelStatus] = Field(None, description="Model status")
    config: Optional[Dict[str, Any]] = Field(None, description="Model configuration")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    accuracy: Optional[float] = Field(None, ge=0, le=1, description="Model accuracy")
    precision: Optional[float] = Field(None, ge=0, le=1, description="Model precision")
    recall: Optional[float] = Field(None, ge=0, le=1, description="Model recall")


class AIModelResponse(AIModelBase, IDMixin, TimestampMixin):
    """Schema for AI model responses."""
    
    owner_id: UUID = Field(..., description="ID of the user who owns this model")
    
    # Model files and endpoints
    model_url: Optional[HttpUrl] = Field(None, description="URL to the model file")
    api_endpoint: Optional[str] = Field(None, description="API endpoint for inference")
    
    # Usage statistics
    total_requests: int = Field(default=0, description="Total number of inference requests")
    successful_requests: int = Field(default=0, description="Number of successful requests")


class AIModelListResponse(BaseSchema):
    """Schema for paginated AI model list responses."""
    
    models: List[AIModelResponse] = Field(..., description="List of AI models")
    total: int = Field(..., description="Total number of models")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of models per page")
    has_next: bool = Field(..., description="Whether there are more pages")