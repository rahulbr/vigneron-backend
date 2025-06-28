"""
Inference request and response Pydantic schemas.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import Field, HttpUrl

from .base import BaseSchema, IDMixin, TimestampMixin


class InferenceStatus(str, Enum):
    """Enum for inference request status."""
    
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InferenceInputType(str, Enum):
    """Enum for input data types."""
    
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    JSON = "json"
    CSV = "csv"


class InferenceRequestBase(BaseSchema):
    """Base schema for inference requests."""
    
    model_id: UUID = Field(..., description="ID of the AI model to use")
    input_type: InferenceInputType = Field(..., description="Type of input data")
    
    # Input data (one of these will be populated based on input_type)
    text_input: Optional[str] = Field(None, description="Text input for processing")
    json_input: Optional[Dict[str, Any]] = Field(None, description="JSON input data")
    file_url: Optional[HttpUrl] = Field(None, description="URL to input file (image, audio, video, csv)")
    
    # Processing options
    options: Dict[str, Any] = Field(default_factory=dict, description="Processing options")
    callback_url: Optional[HttpUrl] = Field(None, description="URL to receive results")


class InferenceRequestCreate(InferenceRequestBase):
    """Schema for creating inference requests."""
    
    user_id: Optional[UUID] = Field(None, description="ID of the requesting user")


class InferenceResponse(BaseSchema):
    """Schema for inference results."""
    
    # Result data
    output: Dict[str, Any] = Field(..., description="Inference output")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")
    
    # Processing metadata
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    model_version: str = Field(..., description="Version of the model used")
    
    # Additional metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional response metadata")


class InferenceRequestResponse(InferenceRequestBase, IDMixin, TimestampMixin):
    """Schema for inference request status and results."""
    
    user_id: Optional[UUID] = Field(None, description="ID of the requesting user")
    status: InferenceStatus = Field(..., description="Current status of the request")
    
    # Results (populated when status is COMPLETED)
    result: Optional[InferenceResponse] = Field(None, description="Inference results")
    
    # Error information (populated when status is FAILED)
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    error_code: Optional[str] = Field(None, description="Error code for failed requests")
    
    # Timing information
    started_at: Optional[datetime] = Field(None, description="When processing started")
    completed_at: Optional[datetime] = Field(None, description="When processing completed")


class BatchInferenceRequest(BaseSchema):
    """Schema for batch inference requests."""
    
    model_id: UUID = Field(..., description="ID of the AI model to use")
    inputs: List[Dict[str, Any]] = Field(..., min_items=1, max_items=1000, description="Batch input data")
    options: Dict[str, Any] = Field(default_factory=dict, description="Processing options")
    callback_url: Optional[HttpUrl] = Field(None, description="URL to receive batch results")


class BatchInferenceResponse(BaseSchema):
    """Schema for batch inference results."""
    
    batch_id: UUID = Field(..., description="Unique identifier for the batch")
    total_items: int = Field(..., description="Total number of items in the batch")
    completed_items: int = Field(..., description="Number of completed items")
    failed_items: int = Field(..., description="Number of failed items")
    results: List[InferenceResponse] = Field(..., description="Individual inference results")
    status: InferenceStatus = Field(..., description="Overall batch status")


class InferenceStatsResponse(BaseSchema):
    """Schema for inference statistics."""
    
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    average_processing_time_ms: float = Field(..., description="Average processing time")
    requests_by_model: Dict[str, int] = Field(..., description="Request count by model")
    requests_by_day: Dict[str, int] = Field(..., description="Request count by day")