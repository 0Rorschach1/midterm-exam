"""Service layer for URL operations."""
from typing import List, Optional
from app.models.url import URL
from app.repositories.url_repository import URLRepository
from app.services.utils import generate_short_code, is_url_expired
from app.config.settings import settings


class URLService:
    """Service for URL business logic."""
    
    def __init__(self, repository: URLRepository):
        """Initialize service with repository.
        
        Args:
            repository: URL repository instance
        """
        self.repository = repository
    
    def create_short_url(self, original_url: str) -> URL:
        """Create a short URL.
        
        Args:
            original_url: The original URL to shorten
            
        Returns:
            URL: Created URL object
            
        Raises:
            ValueError: If URL is invalid or short code generation fails
        """
        # Validate URL
        if not original_url or len(original_url.strip()) == 0:
            raise ValueError("URL cannot be empty")
        
        # Generate unique short code
        max_attempts = 10
        for _ in range(max_attempts):
            short_code = generate_short_code()
            if not self.repository.short_code_exists(short_code):
                return self.repository.create(original_url, short_code)
        
        raise ValueError("Failed to generate unique short code")
    
    def get_url_by_code(self, short_code: str) -> Optional[URL]:
        """Get URL by short code, checking for expiration.
        
        Args:
            short_code: The short code to search for
            
        Returns:
            Optional[URL]: URL object if found and not expired, None otherwise
        """
        url = self.repository.get_by_short_code(short_code)
        
        if url and is_url_expired(url.created_at, settings.APP_TTL_MINUTES):
            # URL has expired, delete it
            self.repository.delete_by_short_code(short_code)
            return None
        
        return url
    
    def get_all_urls(self) -> List[URL]:
        """Get all URLs, excluding expired ones.
        
        Returns:
            List[URL]: List of all valid URL objects
        """
        all_urls = self.repository.get_all()
        valid_urls = []
        
        for url in all_urls:
            if not is_url_expired(url.created_at, settings.APP_TTL_MINUTES):
                valid_urls.append(url)
            else:
                # Delete expired URL
                self.repository.delete_by_short_code(url.short_code)
        
        return valid_urls
    
    def delete_url(self, short_code: str) -> bool:
        """Delete URL by short code.
        
        Args:
            short_code: The short code of the URL to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        return self.repository.delete_by_short_code(short_code)
    
    def cleanup_expired_urls(self) -> int:
        """Delete all expired URLs.
        
        Returns:
            int: Number of deleted URLs
        """
        return self.repository.delete_expired(settings.APP_TTL_MINUTES)
