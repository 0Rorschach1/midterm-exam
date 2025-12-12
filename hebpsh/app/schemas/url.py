"""Pydantic schemas for request and response validation."""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, HttpUrl, Field


class URLCreate(BaseModel):
    """Schema for creating a new short URL."""
    original_url: HttpUrl = Field(..., description="The original URL to shorten (must be a valid URL starting with http:// or https://)")


class URLResponse(BaseModel):
    """Schema for URL response."""
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    """Standard API response format."""
    status: Literal["success", "failure"]
    message: Optional[str] = None
    data: Optional[dict] = None


class URLCreateResponse(APIResponse):
    """Response for URL creation."""
    status: Literal["success"] = "success"
    data: Optional[URLResponse] = None


class URLListResponse(APIResponse):
    """Response for URL list."""
    status: Literal["success"] = "success"
    data: Optional[list[URLResponse]] = None


class ErrorResponse(APIResponse):
    """Response for errors."""
    status: Literal["failure"] = "failure"
    message: str
