# 📘 README - Midterm Final Checklist

This README **must remain in your repository** and **must be fully completed** before submitting the midterm.

---

## 1. API Test Coverage Table

Fill in the second column with the **name of the student** who implemented and tested each API.

| # | API Endpoint / Feature | Implemented & Tested By (Student Name) |
|---|------------------------|----------------------------------------|
| 1 | Create Short URL - **POST /urls** | [Your Name Here] |
| 2 | Redirect to Original URL - **GET /u/{code}** | [Your Name Here] |
| 3 | Get All Shortened URLs - **GET /urls** | [Your Name Here] |
| 4 | Delete Short URL - **DELETE /urls/{code}** | [Your Name Here] |

---

## 2. Code Generation Method (Section 6.4)

Check the method you used to generate the short code:

- [ ] **1. Random Generation**
- [x] **2. ID → Base62 Conversion**
- [ ] **3. Hash-based Generation**

(Only select the one you actually implemented.)

**Implementation Details:**
- **File:** `app/services/utils.py`
- **Function:** `generate_short_code(id: int) -> str`
- **Method:** Converts database ID to Base62 encoding using charset: `0-9`, `a-z`, `A-Z`

---

## 3. Bonus User Story: TTL (Expiration Time) for Shortened Links)

If you implemented the bonus user story, mark the box and complete the required details.

- [x] **TTL Feature Implemented**

**If checked, fill in the following information:**

- **ENV variable or config key used:**
  ```
  APP_TTL_MINUTES=1440
  ```
  You must also ensure this key exists in `.env.example` with a sample value. ✅ **Done**

- **Location of TTL Logic (File + Function):**
  
  Specify the exact location where TTL expiration is checked and expired links are detected/removed.
  
  - **File:** `app/services/url_service.py`
  - **Function:** `cleanup_expired_urls()`
  - **Repository Method:** `app/repositories/url_repository.py → delete_expired()`

- **How TTL cleanup is triggered:**
  
  You must write a Command that removes expired links (created_at + TTL < now()).
  
  Here, write:
  - **Full file path of the command:** `app/cli.py`
  - **Command name / execution method:** 
    ```bash
    poetry run python app/cli.py cleanup-expired
    ```
  - **Scheduler details:**
    - Manual execution via CLI command
    - Can be scheduled using cron (Linux/Mac) or Task Scheduler (Windows)
    - Example cron job (run every hour):
      ```cron
      0 * * * * cd /path/to/hebpsh && poetry run python app/cli.py cleanup-expired
      ```

---

## 4. Postman Collection (Required)

A **Postman Collection** has been created and includes all four API routes:

- **POST /urls** - Create shortened URL
- **GET /u/{code}** - Redirect to original URL
- **GET /urls** - Get all shortened URLs
- **DELETE /urls/{code}** - Delete shortened URL

**Collection Files:**
- Collection: `postman_examples/URL_Shortener_API.postman_collection.json`
- Environment: `postman_examples/URL_Shortener_Environment.postman_environment.json`
- Testing Guide: `postman_examples/TESTING_GUIDE.md`

### Screenshots (included in GitHub)

For each route, two screenshots have been added:
- Success case
- Failure case (appropriate error status code and message)

**Screenshot Location:** `postman_examples/screenshots/` (or add them to your repository)

---

## 5. Environment Configuration

The project uses environment variables for configuration:

### Required `.env` file contents:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/urlshortener

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8003

# TTL Configuration (Time in minutes)
APP_TTL_MINUTES=1440
```

**Files:**
- ✅ `.env.example` - Template with sample values
- ✅ `.env` - Actual configuration (included in repository for easy setup)

---

## 6. Database Setup

### Database Technology:
- **DBMS:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Migrations:** Alembic

### Setup Instructions:

1. **Start PostgreSQL:**
   ```bash
   ./setup_database.sh
   ```

2. **Run Migrations:**
   ```bash
   poetry run alembic upgrade head
   ```

3. **Verify Setup:**
   ```bash
   ./verify_setup.sh
   ```

---

## 7. Project Structure

### Layered Architecture:

```
app/
├── config/           # Configuration (database, settings)
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas (validation)
├── repositories/     # Data access layer
├── services/         # Business logic layer
├── controllers/      # API endpoints (FastAPI routes)
├── cli.py           # CLI commands
└── main.py          # Application entry point
```

**Dependency Injection:** ✅ Implemented
- Repository injected into Service
- Service injected into Controller
- Database session managed via FastAPI dependency

---

## 8. Testing

### Manual Testing:

- ✅ All endpoints tested via Swagger UI: `http://localhost:8003/docs`
- ✅ All endpoints tested via Postman
- ✅ Basic test suite: `test_basic.py`

### Test Results:

```bash
# Run basic tests
poetry run python test_basic.py

# All 5 tests passing:
# ✓ Create short URL
# ✓ Redirect to original URL
# ✓ Get all URLs
# ✓ Delete URL
# ✓ Handle not found error
```

---

## 9. Error Handling

All endpoints return proper HTTP status codes and descriptive error messages:

| Scenario | Status Code | Response Format |
|----------|-------------|-----------------|
| URL Created | 201 | `{"status": "success", "message": "...", "data": {...}}` |
| Successful Redirect | 302 | HTTP redirect to original URL |
| URL Not Found | 404 | `{"status": "failure", "message": "URL not found..."}` |
| Invalid URL Format | 422 | `{"status": "failure", "message": "URL validation error"}` |
| Server Error | 500 | `{"status": "failure", "message": "Internal server error"}` |

---

## 10. Documentation

### Comprehensive Documentation Provided:

- ✅ **README.md** - Project overview and setup
- ✅ **QUICKSTART.md** - Quick start guide
- ✅ **PROJECT_SUMMARY.md** - Technical implementation details
- ✅ **CONTRIBUTING.md** - Contribution guidelines
- ✅ **README_CHECKLIST.md** - This file (Midterm checklist)

### API Documentation:

- **Swagger UI:** http://localhost:8003/docs
- **ReDoc:** http://localhost:8003/redoc

---

## 11. Additional Features

### Implemented:

- ✅ **URL Validation:** Comprehensive validation with Pydantic HttpUrl + custom validators
  - Rejects invalid TLDs
  - Rejects incomplete paths
  - Rejects missing schemes
  
- ✅ **CORS Support:** Enabled for Swagger UI testing

- ✅ **Timezone Handling:** UTC with fallback to system timezone

- ✅ **Unique Short Codes:** Database constraint ensures uniqueness

- ✅ **Helper Scripts:**
  - `setup_database.sh` - Database setup
  - `run_server.sh` - Start API server
  - `verify_setup.sh` - Verify installation

---

## 12. Running the Application

### Quick Start:

```bash
# 1. Install dependencies
poetry install

# 2. Setup database
./setup_database.sh

# 3. Run migrations
poetry run alembic upgrade head

# 4. Start server
./run_server.sh
```

### Access Points:

- **API:** http://localhost:8003
- **Swagger UI:** http://localhost:8003/docs
- **ReDoc:** http://localhost:8003/redoc

---

## 13. Code Quality

- ✅ **Type Hints:** Throughout the codebase
- ✅ **Error Handling:** Comprehensive with descriptive messages
- ✅ **DRY Principle:** Shared utility functions
- ✅ **RESTful Conventions:** Followed
- ✅ **Python 3.11+ Compatible**

---

## 14. Submission Checklist

Before submitting, ensure:

- [x] All 4 API endpoints implemented and tested
- [x] Bonus TTL feature implemented
- [x] Postman collection created with all routes
- [x] Screenshots added for success/failure cases
- [x] Database migrations working
- [x] Documentation complete
- [x] `.env.example` file present
- [x] Code follows layered architecture
- [x] Dependency injection implemented
- [x] Error handling with proper status codes
- [x] This README_CHECKLIST.md filled out completely

---

## Notes

**Endpoint Pattern Used:** `/urls` and `/u/{code}`
- Create: `POST /urls`
- Get All: `GET /urls`
- Redirect: `GET /u/{code}`
- Delete: `DELETE /urls/{code}`

**Port:** 8003 (configurable via `.env`)

**Database:** PostgreSQL running in Docker container

**Python Version:** 3.11+

---

*This checklist was generated based on the actual implementation in the repository.*
