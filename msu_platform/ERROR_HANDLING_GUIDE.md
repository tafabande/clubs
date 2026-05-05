# Error Handling Guide - MSU Platform

This guide covers the comprehensive error handling system implemented in the MSU Platform.

## Table of Contents

- [Overview](#overview)
- [Exception Hierarchy](#exception-hierarchy)
- [Error Response Format](#error-response-format)
- [Custom Exceptions](#custom-exceptions)
- [Exception Handler](#exception-handler)
- [Logging System](#logging-system)
- [Error Codes](#error-codes)
- [Best Practices](#best-practices)
- [Debugging Production Errors](#debugging-production-errors)
- [Sentry Integration](#sentry-integration)

## Overview

The MSU Platform implements a comprehensive error handling system that provides:

- **Standardized Error Responses**: Consistent error format across all endpoints
- **Detailed Logging**: Comprehensive logging with context and tracing
- **Error Codes**: Unique codes for each error type
- **Request Tracing**: Request IDs for debugging
- **Environment-aware**: Detailed errors in development, sanitized in production
- **Security**: Sensitive data never exposed in error responses

### Key Components

1. **Custom Exceptions** (`apps/core/exceptions.py`)
2. **Exception Handler** (`apps/core/exception_handlers.py`)
3. **Error Logging Middleware** (`apps/core/middleware/error_logging.py`)
4. **Logging Configuration** (`config/settings/base.py`)

## Exception Hierarchy

```
MSUPlatformException (base)
├── ValidationException
├── PermissionDeniedException
├── NotFoundException
├── RateLimitException
├── StorageException
├── TranscodingException
├── CacheException
├── AuthenticationException
│   ├── TokenExpiredException
│   └── TokenInvalidException
├── DuplicateResourceException
├── ConfigurationException
├── DatabaseException
├── ExternalServiceException
└── TaskException
```

### Base Exception

All custom exceptions inherit from `MSUPlatformException`:

```python
from apps.core.exceptions import MSUPlatformException

class MSUPlatformException(Exception):
    default_message = "An error occurred"
    error_code = "MSU_ERROR"
    status_code = 500
```

## Error Response Format

All errors return a standardized JSON response:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["This field is required."],
      "password": ["Password must be at least 8 characters."]
    },
    "timestamp": "2026-05-05T14:30:00Z",
    "request_id": "req_abc123def456",
    "status": 400
  }
}
```

### Response Fields

- **code**: Unique error code (e.g., `VALIDATION_ERROR`)
- **message**: Human-readable error message
- **details**: Additional error information (optional)
- **timestamp**: ISO 8601 timestamp
- **request_id**: Unique request identifier for tracing
- **status**: HTTP status code

## Custom Exceptions

### ValidationException

Use for input validation errors:

```python
from apps.core.exceptions import ValidationException

def create_user(data):
    if not data.get('email'):
        raise ValidationException(
            message="Email is required",
            details={'email': ['This field is required.']}
        )
```

**HTTP Status**: 400 Bad Request
**Error Code**: `VALIDATION_ERROR`

### PermissionDeniedException

Use for authorization failures:

```python
from apps.core.exceptions import PermissionDeniedException

def delete_club(request, club_id):
    club = Club.objects.get(id=club_id)
    if not request.user.has_perm('delete_club', club):
        raise PermissionDeniedException(
            message="You don't have permission to delete this club"
        )
```

**HTTP Status**: 403 Forbidden
**Error Code**: `PERMISSION_DENIED`

### NotFoundException

Use when a resource is not found:

```python
from apps.core.exceptions import NotFoundException

def get_club(club_id):
    try:
        return Club.objects.get(id=club_id)
    except Club.DoesNotExist:
        raise NotFoundException(
            message=f"Club with id {club_id} not found"
        )
```

**HTTP Status**: 404 Not Found
**Error Code**: `NOT_FOUND`

### RateLimitException

Use when rate limit is exceeded:

```python
from apps.core.exceptions import RateLimitException

def check_rate_limit(user):
    if user.exceeded_rate_limit():
        raise RateLimitException(
            message="Too many requests",
            retry_after=3600  # Retry after 1 hour
        )
```

**HTTP Status**: 429 Too Many Requests
**Error Code**: `RATE_LIMIT_EXCEEDED`

### StorageException

Use for file storage errors:

```python
from apps.core.exceptions import StorageException

def upload_file(file):
    try:
        storage.save(file.name, file)
    except Exception as e:
        raise StorageException(
            message="Failed to upload file",
            details={'original_error': str(e)}
        )
```

**HTTP Status**: 500 Internal Server Error
**Error Code**: `STORAGE_ERROR`

### TranscodingException

Use for media processing errors:

```python
from apps.core.exceptions import TranscodingException

def transcode_video(video_path):
    try:
        transcode(video_path)
    except Exception as e:
        raise TranscodingException(
            message="Video transcoding failed",
            details={'video': video_path, 'error': str(e)}
        )
```

**HTTP Status**: 500 Internal Server Error
**Error Code**: `TRANSCODING_ERROR`

### CacheException

Use for cache operation errors:

```python
from apps.core.exceptions import CacheException

def get_cached_data(key):
    try:
        return cache.get(key)
    except Exception as e:
        raise CacheException(
            message="Cache operation failed",
            details={'key': key}
        )
```

**HTTP Status**: 500 Internal Server Error
**Error Code**: `CACHE_ERROR`

### AuthenticationException

Use for authentication failures:

```python
from apps.core.exceptions import TokenExpiredException

def validate_token(token):
    if token.is_expired():
        raise TokenExpiredException(
            message="Your session has expired"
        )
```

**HTTP Status**: 401 Unauthorized
**Error Code**: `TOKEN_EXPIRED`

### DuplicateResourceException

Use for unique constraint violations:

```python
from apps.core.exceptions import DuplicateResourceException

def create_club(name):
    if Club.objects.filter(name=name).exists():
        raise DuplicateResourceException(
            message=f"Club '{name}' already exists"
        )
```

**HTTP Status**: 409 Conflict
**Error Code**: `DUPLICATE_RESOURCE`

## Exception Handler

The custom exception handler (`custom_exception_handler`) processes all exceptions and returns standardized responses.

### Features

1. **Automatic Request ID Generation**
   - Unique ID for each request
   - Added to response headers (`X-Request-ID`)
   - Used for log correlation

2. **Comprehensive Logging**
   - All exceptions logged with context
   - User information included
   - Request data sanitized

3. **Environment-aware**
   - Development: Detailed errors with stack traces
   - Production: Sanitized errors, no sensitive data

4. **DRF Integration**
   - Handles all DRF exceptions
   - Converts to standard format
   - Preserves error details

### Usage

The exception handler is automatically applied to all DRF views. No manual configuration needed.

## Logging System

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages (non-critical)
- **ERROR**: Error messages (critical)

### Log Files

```
logs/
├── general.log       # All application logs (INFO+)
├── errors.log        # Error logs only (ERROR+)
├── security.log      # Security-related logs (WARNING+)
└── performance.log   # Performance metrics (INFO+)
```

### Logging in Code

```python
import logging

logger = logging.getLogger(__name__)

# Info logging
logger.info("User logged in", extra={
    'user_id': user.id,
    'email': user.email
})

# Warning logging
logger.warning("Rate limit approaching", extra={
    'user_id': user.id,
    'requests': 450,
    'limit': 500
})

# Error logging
try:
    process_data()
except Exception as e:
    logger.error("Data processing failed", extra={
        'error': str(e),
        'user_id': user.id
    }, exc_info=True)
```

### Log Format

```
[ERROR] 2026-05-05 14:30:00 apps.core views process_data 12345 67890 - Data processing failed
```

Fields:
1. Log level
2. Timestamp
3. Logger name
4. Module
5. Function
6. Process ID
7. Thread ID
8. Message

### Structured Logging

For JSON logging (production):

```python
LOGGING = {
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    }
}
```

## Error Codes

### Complete Error Code Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `PARSE_ERROR` | 400 | Request parsing failed |
| `AUTHENTICATION_FAILED` | 401 | Authentication credentials invalid |
| `NOT_AUTHENTICATED` | 401 | Authentication required |
| `TOKEN_EXPIRED` | 401 | JWT token expired |
| `TOKEN_INVALID` | 401 | JWT token invalid |
| `PERMISSION_DENIED` | 403 | User lacks permission |
| `NOT_FOUND` | 404 | Resource not found |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not allowed |
| `NOT_ACCEPTABLE` | 406 | Content type not acceptable |
| `DUPLICATE_RESOURCE` | 409 | Resource already exists |
| `UNSUPPORTED_MEDIA_TYPE` | 415 | Media type not supported |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected server error |
| `STORAGE_ERROR` | 500 | File storage operation failed |
| `TRANSCODING_ERROR` | 500 | Media transcoding failed |
| `CACHE_ERROR` | 500 | Cache operation failed |
| `DATABASE_ERROR` | 500 | Database operation failed |
| `CONFIGURATION_ERROR` | 500 | System configuration error |
| `TASK_ERROR` | 500 | Background task failed |
| `EXTERNAL_SERVICE_ERROR` | 503 | External service unavailable |

## Best Practices

### 1. Always Use Custom Exceptions

❌ **Don't:**
```python
def get_user(user_id):
    user = User.objects.get(id=user_id)  # Raises DoesNotExist
    return user
```

✅ **Do:**
```python
from apps.core.exceptions import NotFoundException

def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFoundException(f"User {user_id} not found")
```

### 2. Provide Helpful Error Messages

❌ **Don't:**
```python
raise ValidationException("Invalid")
```

✅ **Do:**
```python
raise ValidationException(
    message="Invalid email format",
    details={
        'email': ['Must be a valid email address'],
        'example': 'user@msu.ac.zw'
    }
)
```

### 3. Include Context in Logs

❌ **Don't:**
```python
logger.error("Failed")
```

✅ **Do:**
```python
logger.error("User registration failed", extra={
    'email': email,
    'student_id': student_id,
    'error_type': type(e).__name__
})
```

### 4. Sanitize Sensitive Data

❌ **Don't:**
```python
logger.info(f"User login: {password}")
```

✅ **Do:**
```python
logger.info(f"User login", extra={
    'user_id': user.id,
    'email': user.email
    # Never log passwords, tokens, or secrets
})
```

### 5. Use Appropriate Status Codes

```python
# 400 - Client errors (validation)
raise ValidationException()

# 401 - Authentication required
raise AuthenticationException()

# 403 - Permission denied
raise PermissionDeniedException()

# 404 - Not found
raise NotFoundException()

# 409 - Conflict (duplicate)
raise DuplicateResourceException()

# 429 - Rate limit
raise RateLimitException()

# 500 - Server errors
raise StorageException()
```

### 6. Handle Exceptions at the Right Level

```python
# View level - handle and return user-friendly errors
@api_view(['POST'])
def create_club(request):
    try:
        serializer = ClubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = serializer.save()
        return Response(ClubSerializer(club).data)
    except ValidationException as e:
        # Let exception handler process it
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error("Unexpected error", exc_info=True)
        raise

# Service level - raise specific exceptions
def create_club_service(data):
    if Club.objects.filter(name=data['name']).exists():
        raise DuplicateResourceException(
            f"Club '{data['name']}' already exists"
        )
```

## Debugging Production Errors

### 1. Find Error in Logs

```bash
# Search by request ID
grep "req_abc123" logs/errors.log

# Search by error code
grep "VALIDATION_ERROR" logs/errors.log

# Search by user
grep "user@msu.ac.zw" logs/errors.log

# Tail errors in real-time
tail -f logs/errors.log
```

### 2. Check Sentry

1. Go to [sentry.io](https://sentry.io)
2. Find error by request ID
3. View full stack trace
4. Check user context
5. See error frequency

### 3. Reproduce Locally

```bash
# Use same settings
export DJANGO_SETTINGS_MODULE=config.settings.production

# Add request ID to logs
export REQUEST_ID=req_abc123

# Run command
python manage.py shell
```

### 4. Check Health Endpoints

```bash
# Overall health
curl http://api.msu.ac.zw/health/detailed/

# Specific services
curl http://api.msu.ac.zw/health/db/
curl http://api.msu.ac.zw/health/redis/
curl http://api.msu.ac.zw/health/celery/
```

## Sentry Integration

### Setup

1. **Install Sentry SDK** (already in requirements.txt)

2. **Configure in .env**
   ```bash
   SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
   ENVIRONMENT=production
   RELEASE_VERSION=1.0.0
   ```

3. **Automatic Configuration**
   - Configured in `config/settings/base.py`
   - Integrates with Django, Celery, Redis
   - Only active in production

### Features

- **Automatic Error Tracking**: All unhandled exceptions sent to Sentry
- **Performance Monitoring**: Transaction tracing (10% sample rate)
- **Release Tracking**: Errors grouped by release version
- **User Context**: User information attached to errors
- **Breadcrumbs**: Request history before error
- **Source Maps**: Link errors to source code

### Usage

```python
import sentry_sdk

# Add custom context
sentry_sdk.set_context("club", {
    "id": club.id,
    "name": club.name
})

# Add user context
sentry_sdk.set_user({
    "id": user.id,
    "email": user.email
})

# Capture custom error
sentry_sdk.capture_message("Something went wrong", level="error")

# Add breadcrumb
sentry_sdk.add_breadcrumb(
    category="action",
    message="User clicked button",
    level="info"
)
```

## Common Error Scenarios

### Scenario 1: Invalid API Input

```python
# Client sends invalid data
POST /api/clubs/
{
  "name": "",  # Empty name
  "email": "invalid"  # Invalid email
}

# Response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "name": ["This field may not be blank."],
      "email": ["Enter a valid email address."]
    },
    "status": 400,
    "request_id": "req_abc123"
  }
}
```

### Scenario 2: Unauthorized Access

```python
# User tries to delete club without permission
DELETE /api/clubs/123/

# Response
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "You don't have permission to delete this club",
    "status": 403,
    "request_id": "req_def456"
  }
}
```

### Scenario 3: Resource Not Found

```python
# Client requests non-existent resource
GET /api/clubs/999/

# Response
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Club with id 999 not found",
    "status": 404,
    "request_id": "req_ghi789"
  }
}
```

### Scenario 4: Rate Limit Exceeded

```python
# Client exceeds rate limit
POST /api/auth/login/

# Response
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later",
    "details": {
      "retry_after": 3600
    },
    "status": 429,
    "request_id": "req_jkl012"
  }
}
```

## Testing Error Handling

### Unit Tests

```python
from apps.core.exceptions import ValidationException

def test_validation_error():
    with pytest.raises(ValidationException) as exc_info:
        validate_email("invalid")

    assert exc_info.value.error_code == "VALIDATION_ERROR"
    assert exc_info.value.status_code == 400
```

### Integration Tests

```python
def test_api_validation_error(client):
    response = client.post('/api/clubs/', {
        'name': '',  # Invalid
    })

    assert response.status_code == 400
    assert response.json()['error']['code'] == 'VALIDATION_ERROR'
    assert 'request_id' in response.json()['error']
```

---

**Last Updated**: May 5, 2026
**Version**: 1.0
