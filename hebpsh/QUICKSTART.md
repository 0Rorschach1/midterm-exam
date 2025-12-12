# Quick Start Guide

Get the URL Shortener API up and running in 5 minutes!

## Prerequisites

- Python 3.12+
- Poetry (will be installed if needed)
- Docker (for PostgreSQL)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/HoomanHMP/hebpsh.git
cd hebpsh
```

### 2. Install Poetry (if not installed)

```bash
pip install poetry
```

### 3. Install Dependencies

```bash
poetry install
```

### 4. Setup Database

```bash
./setup_database.sh
```

This will:
- Start PostgreSQL in Docker
- Create the database
- Show connection details

### 5. Run Migrations

```bash
poetry run alembic upgrade head
```

This creates the `urls` table in the database.

### 6. Start the Server

```bash
./run_server.sh
```

Or manually:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Verify Installation

```bash
./verify_setup.sh
```

## Access the API

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Quick Test with cURL

### Create a Short URL

```bash
curl -X POST http://localhost:8000/urls \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com/very/long/url"}'
```

### Get All URLs

```bash
curl http://localhost:8000/urls
```

### Test Redirect (replace with actual code)

```bash
curl -L http://localhost:8000/u/aB3xY9
```

### Delete a URL (replace with actual code)

```bash
curl -X DELETE http://localhost:8000/urls/aB3xY9
```

## Test with Postman

1. Open Postman
2. Import `postman_examples/URL_Shortener_API.postman_collection.json`
3. Import `postman_examples/URL_Shortener_Environment.postman_environment.json`
4. Select "URL Shortener Environment"
5. Run requests

See `postman_examples/TESTING_GUIDE.md` for detailed testing instructions.

## TTL Feature

Clean up expired URLs:

```bash
poetry run python app/cli.py cleanup-expired
```

Configure TTL in `.env`:

```env
APP_TTL_MINUTES=1440  # 24 hours
```

## Troubleshooting

### Database Connection Error

```bash
# Check if database is running
docker ps | grep urlshortener-db

# Restart database
docker restart urlshortener-db
```

### Port Already in Use

```bash
# Change port in .env
APP_PORT=8001

# Or kill process using port 8000
lsof -ti:8000 | xargs kill
```

### Import Errors

```bash
# Ensure you're using Poetry
poetry shell
poetry run python app/main.py
```

## Project Structure

```
hebpsh/
├── app/              # Application code
│   ├── config/      # Settings and database
│   ├── models/      # SQLAlchemy models
│   ├── schemas/     # Pydantic validation
│   ├── repositories/# Database operations
│   ├── services/    # Business logic
│   └── controllers/ # API endpoints
├── alembic/         # Database migrations
└── postman_examples/# API testing
```

## Documentation

- **README.md**: Complete documentation
- **CONTRIBUTING.md**: Team guidelines
- **PROJECT_SUMMARY.md**: Implementation overview
- **postman_examples/TESTING_GUIDE.md**: Testing instructions

## Common Commands

```bash
# Start database
./setup_database.sh

# Run migrations
poetry run alembic upgrade head

# Start server
./run_server.sh

# Run tests
poetry run python test_basic.py

# Clean expired URLs
poetry run python app/cli.py cleanup-expired

# Verify setup
./verify_setup.sh
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /urls | Create short URL |
| GET | /urls | Get all URLs |
| GET | /u/{code} | Redirect to original |
| DELETE | /urls/{code} | Delete URL |
| GET | /health | Health check |

## Next Steps

1. ✅ Test all endpoints with Postman
2. ✅ Review the code structure
3. ✅ Read CONTRIBUTING.md for team workflow
4. ✅ Understand the layered architecture
5. ✅ Test TTL feature
6. ✅ Prepare for presentation

## Support

For issues or questions:
1. Check README.md
2. Review CONTRIBUTING.md
3. Check PROJECT_SUMMARY.md
4. Run `./verify_setup.sh`

---

**Happy coding! 🚀**
