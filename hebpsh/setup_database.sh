#!/bin/bash
# Script to setup PostgreSQL database using Docker

echo "Setting up PostgreSQL database for URL Shortener..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=urlshortener-db)" ]; then
    echo "Removing existing database container..."
    docker stop urlshortener-db 2>/dev/null
    docker rm urlshortener-db 2>/dev/null
fi

# Start PostgreSQL container
echo "Starting PostgreSQL container..."
docker run --name urlshortener-db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=urlshortener \
  -p 5432:5432 \
  -d postgres:latest

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Check if container is running
if [ "$(docker ps -q -f name=urlshortener-db)" ]; then
    echo "✅ PostgreSQL database is running!"
    echo ""
    echo "Connection details:"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo "  Database: urlshortener"
    echo "  User: user"
    echo "  Password: password"
    echo ""
    echo "Connection URL: postgresql://user:password@localhost:5432/urlshortener"
    echo ""
    echo "To connect to the database:"
    echo "  docker exec -it urlshortener-db psql -U user -d urlshortener"
    echo ""
    echo "Next steps:"
    echo "  1. Run migrations: poetry run alembic upgrade head"
    echo "  2. Start the API: ./run_server.sh"
else
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi
