"""Main application module."""
from fastapi import FastAPI
from app.controllers.url_controller import router as url_router

# Create FastAPI application
app = FastAPI(
    title="URL Shortener API",
    description="A RESTful URL shortening service built with FastAPI",
    version="1.0.0"
)

# Include routers
app.include_router(url_router, tags=["URLs"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "status": "success",
        "message": "Welcome to URL Shortener API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "success",
        "message": "Service is healthy"
    }
