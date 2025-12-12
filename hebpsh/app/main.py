"""Main application module."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.controllers.url_controller import router as url_router

# Create FastAPI application
app = FastAPI(
    title="URL Shortener API",
    description="A RESTful URL shortening service built with FastAPI with TTL support",
    version="1.0.0"
)


# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with custom format.
    
    Returns a user-friendly error message for invalid URL format or missing fields.
    """
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        field = error.get("loc", [])[-1] if error.get("loc") else "field"
        msg = error.get("msg", "Invalid input")
        error_type = error.get("type", "")
        
        if "url" in error_type:
            error_messages.append(f"{field}: Must be a valid URL starting with http:// or https://")
        elif "missing" in error_type:
            error_messages.append(f"{field}: This field is required")
        else:
            error_messages.append(f"{field}: {msg}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "failure",
            "message": "Validation error: " + "; ".join(error_messages),
            "details": errors
        }
    )


# Include routers
app.include_router(url_router, tags=["URLs"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "status": "success",
        "message": "Welcome to URL Shortener API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "success",
        "message": "Service is healthy"
    }
