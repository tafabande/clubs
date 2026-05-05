"""
Error logging middleware for comprehensive request/response logging.

Logs all errors with full context including user information, request data,
and performance metrics.
"""
import logging
import time
import uuid
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)
performance_logger = logging.getLogger('performance')


class ErrorLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for logging errors with comprehensive context.

    Logs:
    - All exceptions with full context
    - User information
    - Request data (sanitized)
    - Response status codes
    - Performance metrics
    """

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        super().__init__(get_response)

    def process_request(self, request: HttpRequest) -> None:
        """
        Process incoming request.

        Adds request ID and start time for tracking.
        """
        # Generate unique request ID
        request.request_id = f"req_{uuid.uuid4().hex[:12]}"
        request.start_time = time.time()

        # Log request if in debug mode
        if settings.DEBUG:
            self._log_request(request)

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """
        Process response and log performance metrics.

        Args:
            request: The HTTP request
            response: The HTTP response

        Returns:
            The response object
        """
        # Calculate request duration
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time

            # Log slow requests
            if duration > 1.0:  # More than 1 second
                self._log_slow_request(request, response, duration)

            # Log performance metrics
            self._log_performance(request, response, duration)

        # Add request ID to response headers for tracing
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = request.request_id

        return response

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> None:
        """
        Process exceptions and log with full context.

        Args:
            request: The HTTP request
            exception: The exception that occurred
        """
        self._log_exception(request, exception)

    def _log_request(self, request: HttpRequest) -> None:
        """
        Log incoming request details.

        Args:
            request: The HTTP request
        """
        log_data = {
            'request_id': getattr(request, 'request_id', 'unknown'),
            'method': request.method,
            'path': request.path,
            'user': self._get_user_info(request),
            'ip': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown'),
        }

        logger.debug(f"Incoming request: {log_data}", extra=log_data)

    def _log_performance(
        self, request: HttpRequest, response: HttpResponse, duration: float
    ) -> None:
        """
        Log performance metrics for request/response cycle.

        Args:
            request: The HTTP request
            response: The HTTP response
            duration: Request duration in seconds
        """
        log_data = {
            'request_id': getattr(request, 'request_id', 'unknown'),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2),
            'user': self._get_user_info(request),
        }

        performance_logger.info(
            f"Request completed: {request.method} {request.path} "
            f"[{response.status_code}] in {log_data['duration_ms']}ms",
            extra=log_data
        )

    def _log_slow_request(
        self, request: HttpRequest, response: HttpResponse, duration: float
    ) -> None:
        """
        Log slow requests for performance monitoring.

        Args:
            request: The HTTP request
            response: The HTTP response
            duration: Request duration in seconds
        """
        log_data = {
            'request_id': getattr(request, 'request_id', 'unknown'),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2),
            'user': self._get_user_info(request),
            'query_params': dict(request.GET) if request.GET else {},
        }

        logger.warning(
            f"Slow request detected: {request.method} {request.path} "
            f"took {log_data['duration_ms']}ms",
            extra=log_data
        )

    def _log_exception(self, request: HttpRequest, exception: Exception) -> None:
        """
        Log exception with full request context.

        Args:
            request: The HTTP request
            exception: The exception that occurred
        """
        log_data = {
            'request_id': getattr(request, 'request_id', 'unknown'),
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'method': request.method,
            'path': request.path,
            'user': self._get_user_info(request),
            'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
            'ip': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown'),
        }

        # Add sanitized request data
        if request.method in ['POST', 'PUT', 'PATCH']:
            log_data['request_data'] = self._sanitize_data(request)

        # Add query parameters
        if request.GET:
            log_data['query_params'] = dict(request.GET)

        logger.error(
            f"Exception in request: {type(exception).__name__}: {str(exception)}",
            extra=log_data,
            exc_info=True
        )

    def _get_user_info(self, request: HttpRequest) -> str:
        """
        Get user information from request.

        Args:
            request: The HTTP request

        Returns:
            User identifier string
        """
        if hasattr(request, 'user') and request.user.is_authenticated:
            return f"{request.user.email} (ID: {request.user.id})"
        return 'anonymous'

    def _get_client_ip(self, request: HttpRequest) -> str:
        """
        Get client IP address from request.

        Args:
            request: The HTTP request

        Returns:
            Client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip

    def _sanitize_data(self, request: HttpRequest) -> dict:
        """
        Sanitize request data by removing sensitive fields.

        Args:
            request: The HTTP request

        Returns:
            Sanitized data dictionary
        """
        sensitive_fields = [
            'password', 'token', 'secret', 'api_key', 'authorization',
            'access_token', 'refresh_token', 'csrftoken', 'sessionid'
        ]

        try:
            # Try to get JSON data
            if hasattr(request, 'data'):
                data = dict(request.data)
            else:
                data = dict(request.POST)

            # Remove sensitive fields
            sanitized = {}
            for key, value in data.items():
                if any(field in key.lower() for field in sensitive_fields):
                    sanitized[key] = '***REDACTED***'
                else:
                    sanitized[key] = value

            return sanitized
        except Exception:
            return {}
