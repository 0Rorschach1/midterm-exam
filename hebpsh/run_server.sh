#!/bin/bash
# Script to start the URL Shortener API

echo "Starting URL Shortener API..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

# Run the application
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
