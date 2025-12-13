# URL Shortener Service

A RESTful URL shortening service built with FastAPI, SQLAlchemy, PostgreSQL, and Alembic.

## Project Overview

This is a URL shortener service that allows users to:
- Create short URLs from long URLs
- Redirect from short URLs to original URLs
- List all shortened URLs
- Delete shortened URLs
- Automatically expire URLs based on configurable TTL (Time To Live)

## Technology Stack

- **Programming Language**: Python 3.12+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Migration Tool**: Alembic
- **Dependency Management**: Poetry
- **Version Control**: Git & GitHub

## Architecture

This project follows a **layered architecture** with strict dependency injection:

```
Controller/Router → Service → Repository → Model
```

### Layers:

1. **Controller (Router)**: Handles HTTP requests and responses (`app/controllers/`)
2. **Service**: Contains business logic (`app/services/`)
3. **Repository**: Database operations (`app/repositories/`)
4. **Model**: Data models and database tables (`app/models/`)
5. **Schemas**: Request/response validation with Pydantic (`app/schemas/`)
6. **Config**: Application configuration (`app/config/`)

## Project Structure

```
hebpsh/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── cli.py                     # CLI commands
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Environment configuration
│   │   └── database.py            # Database connection setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── url.py                 # URL database model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── url.py                 # Pydantic schemas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── url_repository.py     # Database operations
│   ├── services/
│   │   ├── __init__.py
│   │   ├── url_service.py        # Business logic
│   │   └── utils.py              # Utility functions
│   └── controllers/
│       ├── __init__.py
│       └── url_controller.py     # API endpoints
├── alembic/
│   ├── versions/
│   │   └── 001_initial.py        # Initial migration
│   ├── env.py                     # Alembic environment
│   └── script.py.mako
├── alembic.ini                    # Alembic configuration
├── pyproject.toml                 # Poetry dependencies
├── .env.example                   # Environment variables template
├── .env                           # Environment variables (not in git)
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- Poetry (Python dependency manager)
- Docker (for PostgreSQL)
- PostgreSQL client (optional, for manual database access)

### 1. Clone the Repository

```bash
git clone https://github.com/HoomanHMP/hebpsh.git
cd hebpsh
```

### 2. Install Dependencies

```bash
# Install Poetry if not already installed
pip install poetry

# Install project dependencies
poetry install
```

### 3. Setup PostgreSQL Database

Start PostgreSQL using Docker:

```bash
docker run --name urlshortener-db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=urlshortener \
  -p 5432:5432 \
  -d postgres:latest
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/urlshortener

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_TTL_MINUTES=1440
```

### 5. Run Database Migrations

```bash
# Run migrations to create the database tables
poetry run alembic upgrade head
```

### 6. Run the Application

```bash
# Start the FastAPI server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Short URL (POST /urls)

**User Story 1**: Create a short URL from a long URL

**Request**:
```bash
POST /urls
Content-Type: application/json

{
  "original_url": "https://www.example.com/very/long/url/path"
}
```

**Response** (201 Created):
```json
{
  "status": "success",
  "message": "Short URL created successfully",
  "data": {
    "id": 1,
    "original_url": "https://www.example.com/very/long/url/path",
    "short_code": "aB3xY9",
    "created_at": "2025-12-12T00:00:00"
  }
}
```

**Error Responses**:
- 400: Invalid input
- 500: Internal server error

### 2. Redirect to Original URL (GET /u/{code})

**User Story 2**: Redirect to the original URL using the short code

**Request**:
```bash
GET /u/aB3xY9
```

**Response** (302 Found):
Redirects to the original URL

**Error Response** (404 Not Found):
```json
{
  "status": "failure",
  "message": "URL not found"
}
```

### 3. Get All URLs (GET /urls)

**User Story 3**: List all shortened URLs

**Request**:
```bash
GET /urls
```

**Response** (200 OK):
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "original_url": "https://www.example.com/very/long/url/path",
      "short_code": "aB3xY9",
      "created_at": "2025-12-12T00:00:00"
    },
    {
      "id": 2,
      "original_url": "https://www.another-example.com/path",
      "short_code": "xY7zW2",
      "created_at": "2025-12-12T01:00:00"
    }
  ]
}
```

### 4. Delete URL (DELETE /urls/{code})

**User Story 4**: Delete a shortened URL

**Request**:
```bash
DELETE /urls/aB3xY9
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "URL deleted successfully"
}
```

**Error Response** (404 Not Found):
```json
{
  "status": "failure",
  "message": "URL not found"
}
```

## TTL (Time To Live) Feature

The application supports automatic expiration of URLs based on a configurable TTL.

### Configuration

Set the TTL in `.env`:
```env
APP_TTL_MINUTES=1440  # 24 hours
```

### Manual Cleanup

Clean up expired URLs manually:

```bash
poetry run python app/cli.py cleanup-expired
```

### Scheduled Cleanup (Optional)

You can setup a cron job to run the cleanup command periodically:

```bash
# Edit crontab
crontab -e

# Add this line to run cleanup every hour
0 * * * * cd /path/to/hebpsh && /path/to/poetry run python app/cli.py cleanup-expired
```

## Short Code Generation

The service generates unique short codes using:
- **Base62 encoding** (a-z, A-Z, 0-9)
- **6 characters** by default
- **Uniqueness check** against the database
- **Indexed column** for fast lookups

## Response Format

All API responses follow a unified structure:

**Success**:
```json
{
  "status": "success",
  "message": "Optional success message",
  "data": { /* response data */ }
}
```

**Failure**:
```json
{
  "status": "failure",
  "message": "Error description"
}
```

## HTTP Status Codes

The API uses standard HTTP status codes:

- **200 OK**: Successful GET, DELETE
- **201 Created**: Successful POST
- **302 Found**: Redirect
- **400 Bad Request**: Invalid input
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Testing

### Manual Testing with cURL

**Create a short URL**:
```bash
curl -X POST http://localhost:8000/urls \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com/long/url"}'
```

**Get all URLs**:
```bash
curl http://localhost:8000/urls
```

**Redirect (follow redirects)**:
```bash
curl -L http://localhost:8000/u/aB3xY9
```

**Delete a URL**:
```bash
curl -X DELETE http://localhost:8000/urls/aB3xY9
```

### Testing with Postman

1. Import the API endpoints into Postman
2. Set the base URL to `http://localhost:8000`
3. Test each endpoint with sample data
4. Save screenshots of successful requests in a `postman_screenshots/` folder

## Database Schema

### URLs Table

| Column        | Type         | Constraints                    |
|---------------|--------------|--------------------------------|
| id            | INTEGER      | PRIMARY KEY, AUTO_INCREMENT    |
| original_url  | VARCHAR      | NOT NULL                       |
| short_code    | VARCHAR(10)  | NOT NULL, UNIQUE, INDEXED      |
| created_at    | DATETIME     | NOT NULL                       |

**Indexes**:
- Primary key on `id`
- Unique index on `short_code`
- Regular index on `short_code` for fast lookups

## Development Guidelines

### Code Style

- Follow **PEP 8** Python style guide
- Use **type hints** for all function parameters and return values
- Add **docstrings** to all classes and functions
- Use **meaningful variable names**

### RESTful Conventions

- Use **plural nouns** for endpoints (e.g., `/urls`)
- Use **HTTP methods** for actions (POST, GET, DELETE)
- No **verbs** in URL paths
- Return appropriate **HTTP status codes**

### Dependency Injection

- All dependencies injected via **constructor injection**
- No layer instantiates the layer below it
- Services receive repositories via constructor
- Controllers receive services via FastAPI Depends

## Team Collaboration

This project was designed as a team assignment with two members:

**Member 1 Responsibilities**:
- Poetry setup
- Database setup
- Model design
- POST /urls endpoint (Create)
- GET /urls endpoint (List All)
- GET /u/{code} endpoint (Redirect)
- DELETE /urls/{code} endpoint (Delete)


**Member 2 Responsibilities**:
- Poetry setup
- Postman documentation

Both members implemented the entire layered architecture for their endpoints.

## Git Workflow

1. Create feature branch from `main`
2. Implement features
3. Test thoroughly
4. Open Pull Request
5. Review and merge to `main`

## Environment Variables

| Variable          | Description                    | Default                                    |
|-------------------|--------------------------------|--------------------------------------------|
| DATABASE_URL      | PostgreSQL connection string   | postgresql://user:password@localhost:5432/urlshortener |
| APP_HOST          | Application host               | 0.0.0.0                                    |
| APP_PORT          | Application port               | 8000                                       |
| APP_TTL_MINUTES   | URL expiration time (minutes)  | 1440 (24 hours)                            |

## Troubleshooting

### Database Connection Issues

#### Password Authentication Failed Error

If you get `password authentication failed for user "user"`:

1. **Make sure PostgreSQL database is running**:
   ```bash
   docker ps | grep urlshortener-db
   ```
   
2. **If not running, start it with the setup script**:
   ```bash
   ./setup_database.sh
   ```
   
3. **Verify `.env` file exists and has correct credentials**:
   ```bash
   cat .env
   # Should show: DATABASE_URL=postgresql://user:password@localhost:5432/urlshortener
   ```
   
4. **If .env doesn't exist, create it**:
   ```bash
   cp .env.example .env
   ```

5. **Remove any existing conflicting database container**:
   ```bash
   docker stop urlshortener-db
   docker rm urlshortener-db
   ./setup_database.sh
   ```

6. **Verify the database is accessible**:
   ```bash
   docker exec -it urlshortener-db psql -U user -d urlshortener
   # Should connect successfully. Type \q to exit
   ```

#### Other Database Issues

If you get connection errors:
1. Ensure PostgreSQL is running: `docker ps`
2. Check connection details in `.env`
3. Verify database exists: `docker exec -it urlshortener-db psql -U user -d urlshortener`

### Migration Issues

If migrations fail:
1. Check database connection (see above)
2. Verify alembic.ini configuration
3. Run: `poetry run alembic current` to check current version
4. Run: `poetry run alembic upgrade head` to apply migrations

### Port Already in Use

If port 8000 is busy:
1. Change `APP_PORT` in `.env` to another port
2. Update `run_server.sh` to match the new port
3. Or kill the process using port 8000: `lsof -ti:8000 | xargs kill`

## Postman Collection & Screenshots 

A complete **Postman Collection** has been created with all four API endpoints, including examples for success and error cases.

### Postman Screenshots
For each route, two screenshots are provided.

All screenshots are located in the `/postman-examples` folder:



**Project completed as part of Backend Development Course - Midterm Assignment**
