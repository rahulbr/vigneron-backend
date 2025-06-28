"""
Common API response schemas.
"""
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Human-readable response message")
    data: Optional[T] = Field(None, description="Response data")
    errors: Optional[List[str]] = Field(None, description="List of error messages")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    
    items: List[T] = Field(..., description="List of items for the current page")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number (1-based)")
    per_page: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Timestamp of the health check")
    version: str = Field(..., description="Application version")
    uptime: float = Field(..., description="Application uptime in seconds")
    database: Optional[str] = Field(None, description="Database connection status")
    external_services: Optional[Dict[str, str]] = Field(None, description="External service statuses")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")


class MessageResponse(BaseModel):
    """Simple message response schema."""
    
    message: str = Field(..., description="Response message")


class SuccessResponse(BaseModel):
    """Success response schema."""
    
    success: bool = Field(True, description="Success indicator")
    message: str = Field(..., description="Success message")