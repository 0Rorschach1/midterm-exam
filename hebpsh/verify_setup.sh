#!/bin/bash
# Verification script to check if the project is set up correctly

echo "=========================================="
echo "URL Shortener - Setup Verification"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
if [ $? -eq 0 ]; then
    echo "✅ Python installed: $PYTHON_VERSION"
else
    echo "❌ Python not found"
    exit 1
fi

# Check Poetry
echo ""
echo "Checking Poetry installation..."
if command -v poetry &> /dev/null; then
    POETRY_VERSION=$(poetry --version 2>&1)
    echo "✅ Poetry installed: $POETRY_VERSION"
else
    echo "❌ Poetry not found. Install with: pip install poetry"
    exit 1
fi

# Check if dependencies are installed
echo ""
echo "Checking project dependencies..."
if poetry show &> /dev/null; then
    echo "✅ Dependencies installed"
    PACKAGE_COUNT=$(poetry show | wc -l)
    echo "   Installed packages: $PACKAGE_COUNT"
else
    echo "⚠️  Dependencies not installed. Run: poetry install"
fi

# Check Docker
echo ""
echo "Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1)
    echo "✅ Docker installed: $DOCKER_VERSION"
else
    echo "❌ Docker not found. Required for PostgreSQL database."
    exit 1
fi

# Check if database container is running
echo ""
echo "Checking database container..."
if docker ps | grep -q urlshortener-db; then
    echo "✅ Database container is running"
else
    echo "⚠️  Database container not running. Run: ./setup_database.sh"
fi

# Check environment file
echo ""
echo "Checking environment configuration..."
if [ -f .env ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found. Copy from: .env.example"
fi

# Check if migrations exist
echo ""
echo "Checking database migrations..."
if [ -d alembic/versions ] && [ "$(ls -A alembic/versions)" ]; then
    MIGRATION_COUNT=$(ls -1 alembic/versions/*.py 2>/dev/null | wc -l)
    echo "✅ Migration files found: $MIGRATION_COUNT"
else
    echo "⚠️  No migration files found"
fi

# Run basic tests
echo ""
echo "Running basic tests..."
if poetry run python test_basic.py > /tmp/test_output.txt 2>&1; then
    echo "✅ All basic tests passed"
else
    echo "❌ Some tests failed. Check output:"
    cat /tmp/test_output.txt
fi

# Check project structure
echo ""
echo "Verifying project structure..."
REQUIRED_DIRS=(
    "app/config"
    "app/models"
    "app/schemas"
    "app/repositories"
    "app/services"
    "app/controllers"
    "alembic/versions"
    "postman_examples"
)

ALL_DIRS_OK=true
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir"
    else
        echo "❌ $dir not found"
        ALL_DIRS_OK=false
    fi
done

# Check required files
echo ""
echo "Verifying required files..."
REQUIRED_FILES=(
    "app/main.py"
    "app/cli.py"
    "pyproject.toml"
    "alembic.ini"
    "README.md"
    ".env.example"
    ".gitignore"
)

ALL_FILES_OK=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file not found"
        ALL_FILES_OK=false
    fi
done

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="

if $ALL_DIRS_OK && $ALL_FILES_OK; then
    echo "✅ Project structure is complete"
else
    echo "⚠️  Some files or directories are missing"
fi

echo ""
echo "Next steps:"
echo "1. If database is not running: ./setup_database.sh"
echo "2. Run migrations: poetry run alembic upgrade head"
echo "3. Start the server: ./run_server.sh"
echo "4. Test with Postman or visit: http://localhost:8000/docs"
echo ""
