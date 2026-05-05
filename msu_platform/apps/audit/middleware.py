"""
Audit logging middleware for MSU Platform.

Automatically logs certain actions and security events.
"""
from .services import AuditService, SecurityService
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class AuditLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log certain requests and actions.

    Logs:
    - Failed authentication attempts
    - Permission denied responses
    - 404 errors (potential unauthorized access attempts)
    - 500 errors (potential attacks or bugs)
    """

    def process_response(self, request, response):
        """Process response to log security events."""

        # Log failed authentication (401)
        if response.status_code == 401 and hasattr(request, 'user'):
            SecurityService.log_security_event(
                event_type='UNAUTHORIZED_ACCESS',
                severity='MEDIUM',
                description=f'Unauthorized access attempt to {request.path}',
                user=request.user if request.user.is_authenticated else None,
                request=request,
                details={'path': request.path, 'method': request.method}
            )

        # Log permission denied (403)
        elif response.status_code == 403 and hasattr(request, 'user'):
            SecurityService.log_permission_violation(
                user=request.user if request.user.is_authenticated else None,
                resource=request.path,
                action=request.method,
                request=request
            )

        # Log not found (404) - potential probing
        elif response.status_code == 404 and request.method in ['POST', 'PUT', 'DELETE']:
            SecurityService.log_security_event(
                event_type='SUSPICIOUS_ACTIVITY',
                severity='LOW',
                description=f'Attempted {request.method} to non-existent endpoint: {request.path}',
                user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                request=request,
                details={'path': request.path, 'method': request.method}
            )

        # Log server errors (500) - potential attacks
        elif response.status_code >= 500:
            SecurityService.log_security_event(
                event_type='SUSPICIOUS_ACTIVITY',
                severity='HIGH',
                description=f'Server error on {request.path}',
                user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                request=request,
                details={
                    'path': request.path,
                    'method': request.method,
                    'status_code': response.status_code
                }
            )

        return response

    def process_exception(self, request, exception):
        """Log exceptions as potential security events."""

        # Log exceptions that might indicate attacks
        exception_name = type(exception).__name__

        if 'SQL' in exception_name or 'Query' in exception_name:
            # Potential SQL injection
            SecurityService.log_security_event(
                event_type='SQL_INJECTION_ATTEMPT',
                severity='CRITICAL',
                description=f'Potential SQL injection attempt: {exception_name}',
                user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                request=request,
                details={
                    'exception': exception_name,
                    'path': request.path,
                    'method': request.method
                }
            )

        elif 'XSS' in exception_name or 'Script' in exception_name:
            # Potential XSS attempt
            SecurityService.log_security_event(
                event_type='XSS_ATTEMPT',
                severity='CRITICAL',
                description=f'Potential XSS attempt: {exception_name}',
                user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                request=request,
                details={
                    'exception': exception_name,
                    'path': request.path,
                    'method': request.method
                }
            )

        # Don't interfere with normal exception handling
        return None
