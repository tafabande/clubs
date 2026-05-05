"""
Custom exception handler for Django REST Framework.

Provides standardized error responses with detailed logging and error codes.
"""
import logging
import traceback
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from .exceptions import MSUPlatformException

logger = logging.getLogger(__name__)


def generate_request_id() -> str:
    """Generate unique request ID for tracing."""
    return f"req_{uuid.uuid4().hex[:12]}"


def get_error_details(exc: Exception) -> Dict[str, Any]:
    """
    Extract detailed error information from exception.

    Args:
        exc: The exception to process

    Returns:
        Dictionary containing error details
    """
    details = {}

    # Handle DRF validation errors
    if isinstance(exc, exceptions.ValidationError):
        if isinstance(exc.detail, dict):
            details = exc.detail
        elif isinstance(exc.detail, list):
            details = {'errors': exc.detail}
        else:
            details = {'message': str(exc.detail)}

    # Handle custom exception details
    elif isinstance(exc, MSUPlatformException):
        details = exc.details

    # Handle other exceptions
    elif hasattr(exc, 'detail'):
        details = {'message': str(exc.detail)}
    else:
        details = {'message': str(exc)}

    return details


def log_exception(exc: Exception, context: Dict[str, Any]) -> None:
    """
    Log exception with full context.

    Args:
        exc: The exception to log
        context: Additional context (request, user, etc.)
    """
    request = context.get('request')
    request_id = context.get('request_id', 'unknown')

    log_data = {
        'request_id': request_id,
        'exception_type': type(exc).__name__,
        'exception_message': str(exc),
        'path': getattr(request, 'path', 'unknown') if request else 'unknown',
        'method': getattr(request, 'method', 'unknown') if request else 'unknown',
        'user': getattr(request.user, 'email', 'anonymous') if request and hasattr(request, 'user') else 'anonymous',
        'user_id': getattr(request.user, 'id', None) if request and hasattr(request, 'user') else None,
    }

    # Add request data (sanitized)
    if request:
        if hasattr(request, 'data'):
            sanitized_data = _sanitize_data(dict(request.data))
            log_data['request_data'] = sanitized_data

        # Add query params
        if hasattr(request, 'query_params'):
            log_data['query_params'] = dict(request.query_params)

    # Log at appropriate level
    if isinstance(exc, (Http404, exceptions.NotFound, exceptions.PermissionDenied)):
        logger.warning(f"Client error: {log_data}", extra=log_data)
    elif isinstance(exc, (exceptions.ValidationError, exceptions.ParseError)):
        logger.info(f"Validation error: {log_data}", extra=log_data)
    else:
        # Server errors - log with full traceback
        log_data['traceback'] = traceback.format_exc()
        logger.error(f"Server error: {log_data}", extra=log_data, exc_info=True)


def _sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove sensitive information from data before logging.

    Args:
        data: Dictionary to sanitize

    Returns:
        Sanitized dictionary
    """
    sensitive_fields = [
        'password', 'token', 'secret', 'api_key', 'authorization',
        'access_token', 'refresh_token', 'csrftoken', 'sessionid'
    ]

    sanitized = {}
    for key, value in data.items():
        if any(field in key.lower() for field in sensitive_fields):
            sanitized[key] = '***REDACTED***'
        elif isinstance(value, dict):
            sanitized[key] = _sanitize_data(value)
        else:
            sanitized[key] = value

    return sanitized


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """
    Custom exception handler for Django REST Framework.

    Provides standardized error responses with:
    - Error codes
    - Detailed messages
    - Request IDs for tracing
    - Timestamps
    - Environment-specific detail levels

    Args:
        exc: The exception that was raised
        context: Context dictionary containing request and view

    Returns:
        Response object with standardized error format
    """
    # Generate request ID for tracing
    request_id = generate_request_id()
    context['request_id'] = request_id

    # Try DRF's default handler first
    response = drf_exception_handler(exc, context)

    # Log the exception with full context
    log_exception(exc, context)

    # Handle custom MSU Platform exceptions
    if isinstance(exc, MSUPlatformException):
        error_code = exc.error_code
        status_code = exc.status_code
        message = exc.message
        details = exc.details

    # Handle DRF exceptions
    elif isinstance(exc, exceptions.APIException):
        error_code = _get_error_code_from_exception(exc)
        status_code = exc.status_code if hasattr(exc, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR
        message = exc.detail if hasattr(exc, 'detail') else str(exc)
        details = get_error_details(exc)

    # Handle Django exceptions
    elif isinstance(exc, Http404):
        error_code = 'NOT_FOUND'
        status_code = status.HTTP_404_NOT_FOUND
        message = 'Resource not found'
        details = {}

    elif isinstance(exc, PermissionDenied):
        error_code = 'PERMISSION_DENIED'
        status_code = status.HTTP_403_FORBIDDEN
        message = 'Permission denied'
        details = {}

    elif isinstance(exc, DjangoValidationError):
        error_code = 'VALIDATION_ERROR'
        status_code = status.HTTP_400_BAD_REQUEST
        message = 'Validation error'
        details = {'errors': exc.messages if hasattr(exc, 'messages') else [str(exc)]}

    # Handle unexpected exceptions
    else:
        error_code = 'INTERNAL_SERVER_ERROR'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'An unexpected error occurred'
        details = {}

        # In development, include exception details
        if settings.DEBUG:
            details = {
                'exception_type': type(exc).__name__,
                'exception_message': str(exc),
                'traceback': traceback.format_exc().split('\n')
            }

    # Build error response
    error_response = {
        'error': {
            'code': error_code,
            'message': str(message),
            'status': status_code,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'request_id': request_id,
        }
    }

    # Add details if present
    if details:
        error_response['error']['details'] = details

    # In production, sanitize error messages
    if not settings.DEBUG and status_code >= 500:
        error_response['error']['message'] = 'An internal server error occurred'
        error_response['error'].pop('details', None)

    return Response(error_response, status=status_code)


def _get_error_code_from_exception(exc: exceptions.APIException) -> str:
    """
    Get error code from DRF exception.

    Args:
        exc: DRF exception

    Returns:
        Error code string
    """
    error_code_map = {
        exceptions.ValidationError: 'VALIDATION_ERROR',
        exceptions.ParseError: 'PARSE_ERROR',
        exceptions.AuthenticationFailed: 'AUTHENTICATION_FAILED',
        exceptions.NotAuthenticated: 'NOT_AUTHENTICATED',
        exceptions.PermissionDenied: 'PERMISSION_DENIED',
        exceptions.NotFound: 'NOT_FOUND',
        exceptions.MethodNotAllowed: 'METHOD_NOT_ALLOWED',
        exceptions.NotAcceptable: 'NOT_ACCEPTABLE',
        exceptions.UnsupportedMediaType: 'UNSUPPORTED_MEDIA_TYPE',
        exceptions.Throttled: 'RATE_LIMIT_EXCEEDED',
    }

    for exception_class, code in error_code_map.items():
        if isinstance(exc, exception_class):
            return code

    return 'API_ERROR'
