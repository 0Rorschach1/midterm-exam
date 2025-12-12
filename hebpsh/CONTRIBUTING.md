# Contributing to URL Shortener

This document provides guidelines for team members working on the URL Shortener project.

## Team Structure

This is a two-person team project. Each member is responsible for implementing specific features end-to-end.

### Member 1 Responsibilities
- Poetry setup and dependency management
- Database setup and configuration
- Model design (URL model)
- **API Endpoints:**
  - POST /urls (Create short URL)
  - GET /urls (Get all URLs)

### Member 2 Responsibilities
- Poetry setup verification
- **API Endpoints:**
  - GET /u/{code} (Redirect to original URL)
  - DELETE /urls/{code} (Delete URL)
- Postman documentation and testing

**Important**: Both members must understand the entire codebase and may be asked to present any part of it.

## Development Workflow

### 1. Initial Setup

```bash
# Clone the repository
git clone https://github.com/HoomanHMP/hebpsh.git
cd hebpsh

# Install dependencies
poetry install

# Setup database
./setup_database.sh

# Run migrations
poetry run alembic upgrade head
```

### 2. Branch Strategy

**Main Branch**: Production-ready code only

**Feature Branches**: Each member works on their own branch

```bash
# Member 1
git checkout -b feature/member1-endpoints

# Member 2
git checkout -b feature/member2-endpoints
```

### 3. Development Process

1. **Understand the Requirements**: Read the user stories carefully
2. **Follow the Architecture**: Implement changes in the correct layer
3. **Test Your Work**: Use Postman to verify endpoints
4. **Document Changes**: Update README if needed
5. **Code Review**: Review each other's code

### 4. Commit Guidelines

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add POST /urls endpoint with validation"
git commit -m "Implement redirect functionality for GET /u/{code}"
git commit -m "Fix: Handle expired URLs in repository layer"

# Bad examples
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### 5. Pull Request Process

1. Push your branch to GitHub:
   ```bash
   git push origin feature/your-branch-name
   ```

2. Open a Pull Request with:
   - Clear title describing the feature
   - List of completed tasks
   - Screenshots of Postman tests (if applicable)
   - Any issues or concerns

3. Request review from your team member

4. Address review comments

5. Merge to main after approval

## Code Standards

### Python Style (PEP 8)

- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter standard)
- Use snake_case for functions and variables
- Use PascalCase for classes
- Add docstrings to all functions and classes

### Type Hints

**Required** for all function parameters and return types:

```python
def create_short_url(self, original_url: str) -> URL:
    """Create a short URL."""
    pass
```

### Dependency Injection

**Never** instantiate dependencies directly:

```python
# ❌ Bad - Direct instantiation
class URLService:
    def __init__(self):
        self.repository = URLRepository()  # Wrong!

# ✅ Good - Constructor injection
class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository
```

### RESTful Conventions

- Use plural nouns: `/urls` not `/url`
- Use HTTP methods for actions
- No verbs in URLs: ❌ `/createUrl` ✅ `POST /urls`
- Consistent naming

### Response Format

All responses must include `status` field:

```python
{
    "status": "success" | "failure",
    "message": "Optional message",
    "data": { /* optional data */ }
}
```

### Error Handling

Always handle errors appropriately:

```python
try:
    url = service.create_short_url(url_data.original_url)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"status": "success", "data": {...}}
    )
except ValueError as e:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "failure", "message": str(e)}
    )
except Exception as e:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "failure", "message": "Internal server error"}
    )
```

## Testing Requirements

### 1. Manual Testing

Test all your endpoints using:
- Postman
- cURL
- Browser (for redirect endpoint)

### 2. Test Cases

For each endpoint, test:
- ✅ Success case
- ❌ Invalid input
- ❌ Not found (where applicable)
- ❌ Server error handling

### 3. Postman Documentation

Member 2 is responsible for:
1. Creating comprehensive Postman collection
2. Adding example responses
3. Taking screenshots of all endpoints
4. Organizing screenshots in `postman_screenshots/` folder

Screenshot naming convention:
- `01_create_url_success.png`
- `02_create_url_error.png`
- `03_get_all_urls.png`
- etc.

## Database Management

### Running Migrations

```bash
# Create a new migration (after model changes)
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head

# Rollback last migration
poetry run alembic downgrade -1
```

### Database Access

```bash
# Connect to PostgreSQL
docker exec -it urlshortener-db psql -U user -d urlshortener

# View all tables
\dt

# View table structure
\d urls

# Query data
SELECT * FROM urls;
```

## Common Issues and Solutions

### Issue: Import Errors

**Solution**: Make sure you're in the project root and using Poetry:
```bash
poetry shell
poetry run python app/main.py
```

### Issue: Database Connection Failed

**Solution**: Ensure PostgreSQL is running:
```bash
docker ps | grep urlshortener-db
# If not running:
./setup_database.sh
```

### Issue: Port Already in Use

**Solution**: Change the port in `.env` or kill the process:
```bash
# Find process
lsof -ti:8000

# Kill process
lsof -ti:8000 | xargs kill
```

### Issue: Alembic Migration Errors

**Solution**: Check that:
1. Database is running
2. DATABASE_URL in `.env` is correct
3. Models are imported in `alembic/env.py`

## Project Structure Rules

### Where to Add Code

| Layer | Location | Purpose | Example |
|-------|----------|---------|---------|
| Model | `app/models/` | Database tables | `url.py` |
| Schema | `app/schemas/` | Request/response validation | `url.py` |
| Repository | `app/repositories/` | Database operations | `url_repository.py` |
| Service | `app/services/` | Business logic | `url_service.py` |
| Controller | `app/controllers/` | HTTP endpoints | `url_controller.py` |
| Config | `app/config/` | Settings, DB setup | `settings.py` |

### What NOT to Do

❌ Don't add business logic in controllers
❌ Don't add database queries in services
❌ Don't bypass the layered architecture
❌ Don't commit `.env` file
❌ Don't commit `poetry.lock` (for this project)
❌ Don't use Docker Compose (requirement says Docker run only)

## Presentation Preparation

Both members may be asked to present any part of the project. Be prepared to explain:

1. **Architecture**: Why we use layered architecture
2. **Dependency Injection**: How and why it's implemented
3. **Database**: Table structure, migrations, indexes
4. **Endpoints**: How each endpoint works end-to-end
5. **Short Code Generation**: The algorithm used
6. **TTL Feature**: How expiration works
7. **Error Handling**: How errors are managed
8. **RESTful Design**: Why endpoints are designed this way

## Review Checklist

Before submitting your PR:

- [ ] All endpoints work correctly
- [ ] Type hints are present
- [ ] Docstrings are added
- [ ] Error handling is comprehensive
- [ ] Response format is consistent
- [ ] HTTP status codes are correct
- [ ] Code follows PEP 8
- [ ] No hardcoded dependencies
- [ ] Tests pass (Postman)
- [ ] Screenshots captured (if applicable)
- [ ] README updated (if needed)

## Communication

- Discuss architectural decisions together
- Agree on naming conventions before starting
- Review each other's code
- Test each other's endpoints
- Help debug issues

## Questions?

If you're unsure about:
- Architecture decisions → Discuss with team member
- Technical implementation → Check the project requirements
- Code quality → Review this guide
- Testing → Check Postman guide

Remember: Both team members must fully understand the entire project!
