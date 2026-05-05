"""
Audit logging services for MSU Platform.

Provides utilities for logging user actions, security events, and activity.
"""
from .models import AuditLog, SecurityEvent, UserActivityLog
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class AuditService:
    """Service for creating audit log entries."""

    @staticmethod
    def log_action(user, action, resource=None, changes=None, request=None,
                   ip_address=None, user_agent=None, session_id=None):
        """
        Log a user action.

        Args:
            user: User instance who performed the action
            action: Action type (CREATE, UPDATE, DELETE, etc.)
            resource: Resource object that was affected
            changes: Dictionary of changes made
            request: Django request object (to extract IP, user agent)
            ip_address: IP address (if request not provided)
            user_agent: User agent string (if request not provided)
            session_id: Session ID (if request not provided)

        Returns:
            AuditLog instance
        """
        # Extract request information if provided
        if request:
            ip_address = AuditService._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            session_id = request.session.session_key if hasattr(request, 'session') else ''

        # Get content type for resource
        resource_type = None
        resource_id = None
        if resource:
            resource_type = ContentType.objects.get_for_model(resource)
            resource_id = resource.id if hasattr(resource, 'id') else None

        try:
            audit_log = AuditLog.objects.create(
                user=user,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                changes=changes or {},
                ip_address=ip_address or '0.0.0.0',
                user_agent=user_agent or '',
                session_id=session_id or '',
            )
            return audit_log
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
            return None

    @staticmethod
    def log_login(user, request, success=True):
        """Log user login attempt."""
        action = 'LOGIN' if success else 'FAILED_LOGIN'
        return AuditService.log_action(
            user=user if success else None,
            action=action,
            request=request
        )

    @staticmethod
    def log_logout(user, request):
        """Log user logout."""
        return AuditService.log_action(
            user=user,
            action='LOGOUT',
            request=request
        )

    @staticmethod
    def log_create(user, resource, request=None):
        """Log resource creation."""
        changes = {'action': 'created', 'resource': str(resource)}
        return AuditService.log_action(
            user=user,
            action='CREATE',
            resource=resource,
            changes=changes,
            request=request
        )

    @staticmethod
    def log_update(user, resource, old_data, new_data, request=None):
        """Log resource update with changes."""
        changes = {
            'old': old_data,
            'new': new_data,
            'modified_fields': list(set(old_data.keys()) & set(new_data.keys()))
        }
        return AuditService.log_action(
            user=user,
            action='UPDATE',
            resource=resource,
            changes=changes,
            request=request
        )

    @staticmethod
    def log_delete(user, resource, request=None):
        """Log resource deletion."""
        changes = {'action': 'deleted', 'resource': str(resource)}
        return AuditService.log_action(
            user=user,
            action='DELETE',
            resource=resource,
            changes=changes,
            request=request
        )

    @staticmethod
    def log_approve(user, resource, request=None):
        """Log approval action."""
        changes = {'action': 'approved', 'resource': str(resource)}
        return AuditService.log_action(
            user=user,
            action='APPROVE',
            resource=resource,
            changes=changes,
            request=request
        )

    @staticmethod
    def _get_client_ip(request):
        """Extract client IP from request, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip


class SecurityService:
    """Service for logging security events."""

    @staticmethod
    def log_security_event(event_type, severity, description, user=None,
                          request=None, ip_address=None, details=None):
        """
        Log a security event.

        Args:
            event_type: Type of security event
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
            description: Description of the event
            user: User instance (if applicable)
            request: Django request object
            ip_address: IP address (if request not provided)
            details: Additional details dictionary

        Returns:
            SecurityEvent instance
        """
        # Extract request information
        if request:
            ip_address = AuditService._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        else:
            user_agent = ''

        try:
            event = SecurityEvent.objects.create(
                event_type=event_type,
                severity=severity,
                description=description,
                user=user,
                ip_address=ip_address or '0.0.0.0',
                user_agent=user_agent,
                details=details or {},
            )

            # Log critical events
            if severity in ['HIGH', 'CRITICAL']:
                logger.warning(
                    f"Security Event: {event_type} | Severity: {severity} | "
                    f"IP: {ip_address} | User: {user.email if user else 'Anonymous'}"
                )

            return event
        except Exception as e:
            logger.error(f"Failed to create security event: {str(e)}")
            return None

    @staticmethod
    def log_failed_login(username, request, reason='Invalid credentials'):
        """Log failed login attempt."""
        details = {'username': username, 'reason': reason}
        return SecurityService.log_security_event(
            event_type='FAILED_LOGIN',
            severity='MEDIUM',
            description=f'Failed login attempt for user: {username}',
            request=request,
            details=details
        )

    @staticmethod
    def log_permission_violation(user, resource, action, request):
        """Log permission violation."""
        details = {
            'resource': str(resource),
            'action': action,
            'user': user.email if user else 'Anonymous'
        }
        return SecurityService.log_security_event(
            event_type='PERMISSION_VIOLATION',
            severity='HIGH',
            description=f'Permission violation: User tried to {action} {resource}',
            user=user,
            request=request,
            details=details
        )

    @staticmethod
    def log_rate_limit_exceeded(user, request, limit_type):
        """Log rate limit exceeded."""
        details = {'limit_type': limit_type}
        return SecurityService.log_security_event(
            event_type='RATE_LIMIT_EXCEEDED',
            severity='MEDIUM',
            description=f'Rate limit exceeded for {limit_type}',
            user=user,
            request=request,
            details=details
        )

    @staticmethod
    def log_suspicious_activity(user, request, description, details=None):
        """Log suspicious activity."""
        return SecurityService.log_security_event(
            event_type='SUSPICIOUS_ACTIVITY',
            severity='HIGH',
            description=description,
            user=user,
            request=request,
            details=details
        )

    @staticmethod
    def resolve_event(event_id, resolved_by, resolution_notes=''):
        """
        Mark a security event as resolved.

        Args:
            event_id: SecurityEvent ID
            resolved_by: User who resolved the event
            resolution_notes: Notes about the resolution
        """
        try:
            event = SecurityEvent.objects.get(id=event_id)
            event.resolved = True
            event.resolved_at = timezone.now()
            event.resolved_by = resolved_by
            event.resolution_notes = resolution_notes
            event.save()
            return event
        except SecurityEvent.DoesNotExist:
            logger.error(f"Security event {event_id} not found")
            return None


class ActivityService:
    """Service for logging user activity."""

    @staticmethod
    def log_activity(user, action, resource=None, metadata=None, request=None):
        """
        Log user activity.

        Args:
            user: User instance
            action: Activity type (VIEW, SEARCH, DOWNLOAD, SHARE)
            resource: Resource object being accessed
            metadata: Additional metadata dictionary
            request: Django request object

        Returns:
            UserActivityLog instance
        """
        # Get IP address
        ip_address = '0.0.0.0'
        if request:
            ip_address = AuditService._get_client_ip(request)

        # Get content type for resource
        resource_type = None
        resource_id = None
        if resource:
            resource_type = ContentType.objects.get_for_model(resource)
            resource_id = resource.id if hasattr(resource, 'id') else None

        try:
            activity = UserActivityLog.objects.create(
                user=user,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                metadata=metadata or {},
                ip_address=ip_address,
            )
            return activity
        except Exception as e:
            logger.error(f"Failed to create activity log: {str(e)}")
            return None

    @staticmethod
    def log_view(user, resource, request=None):
        """Log resource view."""
        return ActivityService.log_activity(
            user=user,
            action='VIEW',
            resource=resource,
            request=request
        )

    @staticmethod
    def log_search(user, query, results_count, request=None):
        """Log search activity."""
        metadata = {'query': query, 'results_count': results_count}
        return ActivityService.log_activity(
            user=user,
            action='SEARCH',
            metadata=metadata,
            request=request
        )

    @staticmethod
    def log_download(user, resource, request=None):
        """Log file download."""
        return ActivityService.log_activity(
            user=user,
            action='DOWNLOAD',
            resource=resource,
            request=request
        )

    @staticmethod
    def log_share(user, resource, share_method, request=None):
        """Log content sharing."""
        metadata = {'share_method': share_method}
        return ActivityService.log_activity(
            user=user,
            action='SHARE',
            resource=resource,
            metadata=metadata,
            request=request
        )
