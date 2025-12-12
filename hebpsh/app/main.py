"""Main application module."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from app.controllers.url_controller import router as url_router

# Create FastAPI application
app = FastAPI(
    title="URL Shortener API",
    description="A RESTful URL shortening service built with FastAPI with TTL support",
    version="1.0.0"
)

# Add CORS middleware to allow Swagger UI redirects
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        
        # Extract custom error message from context if available (for custom validators)
        if error_type == "value_error" and "ctx" in error and "error" in error["ctx"]:
            # Custom validator error - extract the actual message
            custom_error = str(error["ctx"]["error"])
            # Remove "ValueError('" prefix and "')" suffix if present
            if custom_error.startswith("ValueError('") and custom_error.endswith("')"):
                custom_error = custom_error[12:-2]
            elif custom_error.startswith("ValueError(") and custom_error.endswith(")"):
                custom_error = custom_error[11:-1]
            error_messages.append(custom_error)
        elif "url" in error_type or "url_parsing" in error_type:
            error_messages.append("Must be a valid URL with proper format (e.g., https://example.com)")
        elif "missing" in error_type:
            error_messages.append(f"{field}: This field is required")
        else:
            # For other errors, use the message from Pydantic
            # Remove "Value error, " prefix if present
            if msg.startswith("Value error, "):
                msg = msg[13:]
            error_messages.append(msg)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "failure",
            "message": "; ".join(error_messages)
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
