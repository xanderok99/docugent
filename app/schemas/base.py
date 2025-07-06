"""
Base Pydantic schemas for API responses.
"""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar('T')

class SuccessResponseSchema(BaseModel, Generic[T]):
    """Base success response schema."""
    success: bool = True
    data: T
    message: Optional[str] = None

class ErrorResponseSchema(BaseModel):
    """Base error response schema."""
    success: bool = False
    error: str
    message: Optional[str] = None
    details: Optional[Any] = None

class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    status: str = "healthy"
    version: str
    environment: str
    timestamp: str 