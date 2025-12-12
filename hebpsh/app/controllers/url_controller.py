"""URL controllers/routers for handling HTTP requests."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.repositories.url_repository import URLRepository
from app.services.url_service import URLService
from app.schemas.url import (
    URLCreate,
    URLResponse,
    URLCreateResponse,
    URLListResponse,
    ErrorResponse
)

router = APIRouter()


def get_url_service(db: Session = Depends(get_db)) -> URLService:
    """Dependency injection for URL service.
    
    Args:
        db: Database session
        
    Returns:
        URLService: URL service instance
    """
    repository = URLRepository(db)
    return URLService(repository)


@router.post(
    "/urls",
    response_model=URLCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Short URL created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_short_url(
    url_data: URLCreate,
    service: URLService = Depends(get_url_service)
):
    """Create a short URL.
    
    User Story 1: As a system user, I want to send a long URL to the service 
    and receive a short link.
    
    Args:
        url_data: URL creation data
        service: URL service instance
        
    Returns:
        URLCreateResponse: Created URL information
        
    Raises:
        HTTPException: If URL creation fails
    """
    try:
        url = service.create_short_url(url_data.original_url)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": "success",
                "message": "Short URL created successfully",
                "data": {
                    "id": url.id,
                    "original_url": url.original_url,
                    "short_code": url.short_code,
                    "created_at": url.created_at.isoformat()
                }
            }
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "failure",
                "message": str(e)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "failure",
                "message": "Internal server error"
            }
        )


@router.get(
    "/u/{code}",
    responses={
        302: {"description": "Redirect to original URL"},
        404: {"model": ErrorResponse, "description": "URL not found"}
    }
)
async def redirect_to_url(
    code: str,
    service: URLService = Depends(get_url_service)
):
    """Redirect to original URL using short code.
    
    User Story 2: As a user, I want to enter the short link and be 
    redirected to the original URL.
    
    Args:
        code: Short code
        service: URL service instance
        
    Returns:
        RedirectResponse: Redirect to original URL
        
    Raises:
        HTTPException: If URL not found
    """
    url = service.get_url_by_code(code)
    
    if not url:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "failure",
                "message": "URL not found"
            }
        )
    
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_302_FOUND)


@router.get(
    "/urls",
    response_model=URLListResponse,
    responses={
        200: {"description": "List of all URLs"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_all_urls(
    service: URLService = Depends(get_url_service)
):
    """Get all shortened URLs.
    
    User Story 3: As a user/admin, I want to see a list of all shortened URLs.
    
    Args:
        service: URL service instance
        
    Returns:
        URLListResponse: List of all URLs
    """
    try:
        urls = service.get_all_urls()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "data": [
                    {
                        "id": url.id,
                        "original_url": url.original_url,
                        "short_code": url.short_code,
                        "created_at": url.created_at.isoformat()
                    }
                    for url in urls
                ]
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "failure",
                "message": "Internal server error"
            }
        )


@router.delete(
    "/urls/{code}",
    responses={
        200: {"description": "URL deleted successfully"},
        404: {"model": ErrorResponse, "description": "URL not found"}
    }
)
async def delete_url(
    code: str,
    service: URLService = Depends(get_url_service)
):
    """Delete a shortened URL.
    
    User Story 4: As a user/admin, I want to delete a short link.
    
    Args:
        code: Short code of URL to delete
        service: URL service instance
        
    Returns:
        JSON response with deletion status
    """
    deleted = service.delete_url(code)
    
    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "failure",
                "message": "URL not found"
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "URL deleted successfully"
        }
    )
