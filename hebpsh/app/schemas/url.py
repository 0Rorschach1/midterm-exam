"""Pydantic schemas for request and response validation."""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, HttpUrl, Field, field_validator
import re


class URLCreate(BaseModel):
    """Schema for creating a new short URL."""
    original_url: HttpUrl = Field(..., description="The original URL to shorten (must be a valid URL starting with http:// or https://)")
    
    @field_validator('original_url')
    @classmethod
    def validate_url_format(cls, v):
        """Additional validation for URL format.
        
        Ensures:
        - URL has a valid scheme (http/https)
        - URL has a valid domain with proper TLD
        - URL doesn't end with just a slash after domain
        - URL path is complete if present
        """
        url_str = str(v)
        
        # Extract domain from URL (between scheme and first slash or end)
        domain_match = re.match(r'https?://([^/]+)', url_str)
        if not domain_match:
            raise ValueError("URL must have a valid domain")
        
        domain = domain_match.group(1)
        
        # Check if domain has at least one dot for TLD (e.g., example.com)
        # Allow localhost and IP addresses as special cases
        if domain not in ['localhost', '127.0.0.1'] and not re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
            if '.' not in domain:
                raise ValueError("URL must have a valid top-level domain (e.g., .com, .org, .net)")
            
            # Check if TLD is at least 2 characters
            tld = domain.split('.')[-1]
            if len(tld) < 2:
                raise ValueError("URL must have a valid top-level domain")
        
        # Check for incomplete URLs like "https://github./" or "https://example.com/"
        # Allow root URLs but prevent obvious incomplete paths
        if url_str.endswith('/.') or url_str.endswith('//'):
            raise ValueError("URL path appears incomplete or malformed")
        
        # Check for suspicious patterns that indicate incomplete URLs
        path_after_domain = url_str[len(f"{domain_match.group(0)}"):]
        if path_after_domain == '/.':
            raise ValueError("URL path is incomplete")
        
        return v


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
