"""
Custom exception classes for MSU Platform.

Provides a hierarchy of exceptions with error codes for standardized error handling.
"""
from typing import Any, Dict, Optional


class MSUPlatformException(Exception):
    """
    Base exception class for all MSU Platform exceptions.

    All custom exceptions should inherit from this class.
    """
    default_message = "An error occurred"
    error_code = "MSU_ERROR"
    status_code = 500

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message or self.default_message
        self.details = details or {}
        if error_code:
            self.error_code = error_code
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary format for API responses."""
        return {
            'error': {
                'code': self.error_code,
                'message': self.message,
                'details': self.details,
                'status': self.status_code
            }
        }


class ValidationException(MSUPlatformException):
    """
    Exception raised for validation errors.

    Use when input data fails validation checks.
    """
    default_message = "Invalid input data"
    error_code = "VALIDATION_ERROR"
    status_code = 400


class PermissionDeniedException(MSUPlatformException):
    """
    Exception raised when user lacks required permissions.

    Use for authorization failures.
    """
    default_message = "You do not have permission to perform this action"
    error_code = "PERMISSION_DENIED"
    status_code = 403


class NotFoundException(MSUPlatformException):
    """
    Exception raised when a resource is not found.

    Use for 404 errors.
    """
    default_message = "The requested resource was not found"
    error_code = "NOT_FOUND"
    status_code = 404


class RateLimitException(MSUPlatformException):
    """
    Exception raised when rate limit is exceeded.

    Use for throttling violations.
    """
    default_message = "Rate limit exceeded. Please try again later"
    error_code = "RATE_LIMIT_EXCEEDED"
    status_code = 429

    def __init__(self, message=None, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
        if retry_after:
            self.details['retry_after'] = retry_after


class StorageException(MSUPlatformException):
    """
    Exception raised for storage/S3 related errors.

    Use when file upload, download, or storage operations fail.
    """
    default_message = "Storage operation failed"
    error_code = "STORAGE_ERROR"
    status_code = 500


class TranscodingException(MSUPlatformException):
    """
    Exception raised for video/media transcoding errors.

    Use when media processing fails.
    """
    default_message = "Media transcoding failed"
    error_code = "TRANSCODING_ERROR"
    status_code = 500


class CacheException(MSUPlatformException):
    """
    Exception raised for cache operation errors.

    Use when Redis/cache operations fail.
    """
    default_message = "Cache operation failed"
    error_code = "CACHE_ERROR"
    status_code = 500


class AuthenticationException(MSUPlatformException):
    """
    Exception raised for authentication errors.

    Use when user authentication fails.
    """
    default_message = "Authentication failed"
    error_code = "AUTHENTICATION_ERROR"
    status_code = 401


class TokenExpiredException(AuthenticationException):
    """
    Exception raised when JWT token has expired.
    """
    default_message = "Token has expired"
    error_code = "TOKEN_EXPIRED"
    status_code = 401


class TokenInvalidException(AuthenticationException):
    """
    Exception raised when JWT token is invalid.
    """
    default_message = "Invalid token"
    error_code = "TOKEN_INVALID"
    status_code = 401


class DuplicateResourceException(MSUPlatformException):
    """
    Exception raised when attempting to create a duplicate resource.

    Use for unique constraint violations.
    """
    default_message = "Resource already exists"
    error_code = "DUPLICATE_RESOURCE"
    status_code = 409


class ConfigurationException(MSUPlatformException):
    """
    Exception raised for configuration errors.

    Use when system configuration is invalid or missing.
    """
    default_message = "System configuration error"
    error_code = "CONFIGURATION_ERROR"
    status_code = 500


class DatabaseException(MSUPlatformException):
    """
    Exception raised for database operation errors.

    Use when database operations fail.
    """
    default_message = "Database operation failed"
    error_code = "DATABASE_ERROR"
    status_code = 500


class ExternalServiceException(MSUPlatformException):
    """
    Exception raised when external service calls fail.

    Use for third-party API failures.
    """
    default_message = "External service unavailable"
    error_code = "EXTERNAL_SERVICE_ERROR"
    status_code = 503


class TaskException(MSUPlatformException):
    """
    Exception raised for Celery task errors.

    Use when background task processing fails.
    """
    default_message = "Task processing failed"
    error_code = "TASK_ERROR"
    status_code = 500
