# Postman Testing Guide

This guide explains how to test the URL Shortener API using Postman.

## Import Collection

1. Open Postman
2. Click "Import" button
3. Select the file: `URL_Shortener_API.postman_collection.json`
4. The collection will appear in your Collections sidebar

## Import Environment

1. In Postman, click the gear icon (Manage Environments)
2. Click "Import"
3. Select the file: `URL_Shortener_Environment.postman_environment.json`
4. Select "URL Shortener Environment" from the environment dropdown

## Prerequisites

Make sure the API server is running:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Testing Workflow

### 1. Health Check

**Endpoint**: GET `/health`

**Purpose**: Verify the API is running

**Expected Response**:
```json
{
  "status": "success",
  "message": "Service is healthy"
}
```

**Status Code**: 200 OK

---

### 2. Create Short URL (User Story 1)

**Endpoint**: POST `/urls`

**Purpose**: Create a short URL from a long URL

**Request Body**:
```json
{
  "original_url": "https://www.example.com/very/long/url/path/to/resource"
}
```

**Expected Response** (201 Created):
```json
{
  "status": "success",
  "message": "Short URL created successfully",
  "data": {
    "id": 1,
    "original_url": "https://www.example.com/very/long/url/path/to/resource",
    "short_code": "aB3xY9",
    "created_at": "2025-12-12T00:00:00"
  }
}
```

**Note**: Save the `short_code` value for use in subsequent tests.

**Test Cases**:
- ✅ Valid URL - Should return 201 Created
- ❌ Empty URL - Should return 400 Bad Request
- ❌ Invalid format - Should return 400 Bad Request

---

### 3. Get All URLs (User Story 3)

**Endpoint**: GET `/urls`

**Purpose**: Retrieve a list of all shortened URLs

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "original_url": "https://www.example.com/very/long/url/path/to/resource",
      "short_code": "aB3xY9",
      "created_at": "2025-12-12T00:00:00"
    }
  ]
}
```

**Test Cases**:
- ✅ Should return all URLs (including expired check)
- ✅ Empty list should return `{"status": "success", "data": []}`

---

### 4. Redirect to Original URL (User Story 2)

**Endpoint**: GET `/u/{code}`

**Purpose**: Redirect to the original URL using the short code

**Example**: GET `/u/aB3xY9`

**Expected Response** (302 Found):
- HTTP Status: 302
- Location Header: Points to original URL
- Browser/Postman will follow redirect automatically

**In Postman**:
1. Disable "Automatically follow redirects" in Settings to see the 302 response
2. Or enable it to see the final destination

**Test Cases**:
- ✅ Valid short code - Should return 302 redirect
- ❌ Invalid short code - Should return 404 Not Found with message "URL not found"
- ❌ Expired URL - Should return 404 Not Found

---

### 5. Delete URL (User Story 4)

**Endpoint**: DELETE `/urls/{code}`

**Purpose**: Delete a shortened URL by its short code

**Example**: DELETE `/urls/aB3xY9`

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "message": "URL deleted successfully"
}
```

**Test Cases**:
- ✅ Valid short code - Should return 200 OK
- ❌ Invalid short code - Should return 404 Not Found
- ❌ Already deleted - Should return 404 Not Found

---

## Complete Test Scenario

Follow these steps to test the complete workflow:

1. **Health Check**: Verify API is running
2. **Create URL 1**: Create first short URL, note the `short_code`
3. **Create URL 2**: Create second short URL, note the `short_code`
4. **Get All URLs**: Should return both URLs
5. **Redirect**: Use one of the short codes to test redirection
6. **Delete URL 1**: Delete the first URL
7. **Get All URLs**: Should return only one URL
8. **Redirect**: Try redirecting to deleted URL (should fail)
9. **Delete URL 2**: Delete the second URL
10. **Get All URLs**: Should return empty array

## Error Responses

All error responses follow this format:

```json
{
  "status": "failure",
  "message": "Error description"
}
```

### Common Errors

| Status Code | Message | Cause |
|-------------|---------|-------|
| 400 | "URL cannot be empty" | Empty or whitespace URL |
| 400 | "Failed to generate unique short code" | System error (rare) |
| 404 | "URL not found" | Invalid or expired short code |
| 500 | "Internal server error" | Server-side error |

## Screenshots

Take screenshots of the following:

1. **Successful POST /urls** - Show request body and 201 response
2. **Successful GET /urls** - Show list of URLs
3. **Successful GET /u/{code}** - Show 302 redirect (with Location header)
4. **Successful DELETE /urls/{code}** - Show 200 response
5. **404 Error** - Show "URL not found" response
6. **400 Error** - Show validation error

Save screenshots in `postman_screenshots/` folder with descriptive names:
- `01_create_url_success.png`
- `02_get_all_urls.png`
- `03_redirect_success.png`
- `04_delete_url_success.png`
- `05_url_not_found_error.png`
- `06_validation_error.png`

## Tips

1. **Use Variables**: The `{{base_url}}` variable is already configured
2. **Copy Short Codes**: After creating a URL, copy the `short_code` for use in other requests
3. **Check Headers**: For redirect endpoint, check the `Location` header
4. **Status Codes**: Verify that each response has the correct HTTP status code
5. **JSON Format**: Ensure all responses follow the standard format with `status` field

## Advanced Testing

### Test TTL Feature

1. Change `APP_TTL_MINUTES` in `.env` to a small value (e.g., 1 minute)
2. Restart the server
3. Create a URL
4. Wait for TTL to expire
5. Try to access the URL - should return 404
6. Run cleanup command: `poetry run python app/cli.py cleanup-expired`

### Test Concurrent Requests

1. Create multiple URLs simultaneously
2. Verify all short codes are unique
3. Test that no duplicate short codes are generated

## Validation Checklist

- [ ] All 4 user stories are working correctly
- [ ] Correct HTTP status codes are returned
- [ ] Error messages are clear and descriptive
- [ ] JSON response format is consistent
- [ ] RESTful naming conventions are followed
- [ ] TTL feature works correctly
- [ ] All screenshots are captured and saved
