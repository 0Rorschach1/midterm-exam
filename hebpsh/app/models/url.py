"""Database models for the application."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Index
from app.config.database import Base


def get_utc_now() -> datetime:
    """Get current UTC time with timezone awareness.
    
    Returns:
        datetime: Current UTC time
    """
    return datetime.now(timezone.utc)


class URL(Base):
    """URL model representing shortened URLs in the database."""
    
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    
    # Create index on short_code for faster lookups
    __table_args__ = (
        Index('idx_short_code', 'short_code'),
    )
