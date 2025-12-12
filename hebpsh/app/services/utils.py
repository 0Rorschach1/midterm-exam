"""Utility functions for URL shortening."""
import random
import string
from datetime import datetime, timedelta, timezone


# Base62 characters (a-z, A-Z, 0-9)
BASE62_CHARS = string.ascii_letters + string.digits


def generate_short_code(length: int = 6) -> str:
    """Generate a random short code using Base62 characters.
    
    Args:
        length: Length of the short code (default: 6)
        
    Returns:
        str: Generated short code
    """
    return ''.join(random.choices(BASE62_CHARS, k=length))


def get_current_utc_time() -> datetime:
    """Get current UTC time with timezone awareness.
    
    Returns:
        datetime: Current UTC time with timezone info
    """
    return datetime.now(timezone.utc)


def calculate_expiration_time(ttl_minutes: int) -> datetime:
    """Calculate expiration timestamp based on TTL.
    
    Args:
        ttl_minutes: Time to live in minutes
        
    Returns:
        datetime: Expiration timestamp (current time - TTL)
    """
    return get_current_utc_time() - timedelta(minutes=ttl_minutes)


def is_url_expired(created_at: datetime, ttl_minutes: int) -> bool:
    """Check if a URL has expired based on TTL.
    
    Args:
        created_at: URL creation timestamp
        ttl_minutes: Time to live in minutes
        
    Returns:
        bool: True if expired, False otherwise
    """
    # Ensure created_at is timezone-aware
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    
    expiration_time = created_at + timedelta(minutes=ttl_minutes)
    return get_current_utc_time() > expiration_time
