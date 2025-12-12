"""Repository layer for URL operations."""
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.url import URL


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


class URLRepository:
    """Repository for URL database operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def create(self, original_url: str, short_code: str) -> URL:
        """Create a new URL entry.
        
        Args:
            original_url: The original URL
            short_code: The generated short code
            
        Returns:
            URL: Created URL object
        """
        db_url = URL(
            original_url=original_url,
            short_code=short_code,
            created_at=get_current_utc_time()
        )
        self.db.add(db_url)
        self.db.commit()
        self.db.refresh(db_url)
        return db_url
    
    def get_by_short_code(self, short_code: str) -> Optional[URL]:
        """Get URL by short code.
        
        Args:
            short_code: The short code to search for
            
        Returns:
            Optional[URL]: URL object if found, None otherwise
        """
        return self.db.query(URL).filter(URL.short_code == short_code).first()
    
    def get_all(self) -> List[URL]:
        """Get all URLs.
        
        Returns:
            List[URL]: List of all URL objects
        """
        return self.db.query(URL).all()
    
    def delete_by_short_code(self, short_code: str) -> bool:
        """Delete URL by short code.
        
        Args:
            short_code: The short code of the URL to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        url = self.get_by_short_code(short_code)
        if url:
            self.db.delete(url)
            self.db.commit()
            return True
        return False
    
    def short_code_exists(self, short_code: str) -> bool:
        """Check if a short code already exists.
        
        Args:
            short_code: The short code to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return self.db.query(URL).filter(URL.short_code == short_code).count() > 0
    
    def delete_expired(self, ttl_minutes: int) -> int:
        """Delete URLs that have expired based on TTL.
        
        Args:
            ttl_minutes: Time to live in minutes
            
        Returns:
            int: Number of deleted records
        """
        expiration_time = calculate_expiration_time(ttl_minutes)
        expired_urls = self.db.query(URL).filter(URL.created_at < expiration_time).all()
        count = len(expired_urls)
        
        for url in expired_urls:
            self.db.delete(url)
        
        self.db.commit()
        return count
