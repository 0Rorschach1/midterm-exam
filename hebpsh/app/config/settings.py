"""Configuration settings for the application."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/urlshortener")
    
    # Application
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    
    # TTL (Time To Live) Configuration
    # URLs older than this value (in minutes) will be considered expired
    # Expired URLs are automatically filtered out when accessed and can be deleted with cleanup command
    # Set to 0 to disable expiration (URLs never expire)
    # Default: 1440 minutes = 24 hours
    APP_TTL_MINUTES: int = int(os.getenv("APP_TTL_MINUTES", "1440"))


settings = Settings()
