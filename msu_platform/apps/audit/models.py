"""Audit and logging models."""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from apps.users.models import User
import uuid


class AuditLog(models.Model):
    """Audit log for tracking user actions."""

    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('VIEW', 'View'),
        ('APPROVE', 'Approve'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    # Generic foreign key to resource
    resource_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    resource_id = models.UUIDField(null=True, blank=True)

    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]


class UserActivityLog(models.Model):
    """Track user activity for analytics."""

    ACTION_CHOICES = [
        ('VIEW', 'View'),
        ('SEARCH', 'Search'),
        ('DOWNLOAD', 'Download'),
        ('SHARE', 'Share'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    resource_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    resource_id = models.UUIDField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activity_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]


class SecurityEvent(models.Model):
    """
    Track security-related events for monitoring and alerts.

    Specialized model for security events that may require immediate attention.
    """

    EVENT_TYPES = [
        ('FAILED_LOGIN', 'Failed Login'),
        ('ACCOUNT_LOCKED', 'Account Locked'),
        ('SUSPICIOUS_ACTIVITY', 'Suspicious Activity'),
        ('PERMISSION_VIOLATION', 'Permission Violation'),
        ('RATE_LIMIT_EXCEEDED', 'Rate Limit Exceeded'),
        ('SQL_INJECTION_ATTEMPT', 'SQL Injection Attempt'),
        ('XSS_ATTEMPT', 'XSS Attempt'),
        ('CSRF_FAILURE', 'CSRF Failure'),
        ('UNAUTHORIZED_ACCESS', 'Unauthorized Access'),
        ('DATA_BREACH_ATTEMPT', 'Data Breach Attempt'),
    ]

    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    # Event details
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM', db_index=True)

    # User/IP information
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='security_events'
    )
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # Event details
    description = models.TextField()
    details = models.JSONField(default=dict, blank=True)

    # Response
    resolved = models.BooleanField(default=False, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_security_events'
    )
    resolution_notes = models.TextField(blank=True)

    class Meta:
        db_table = 'security_events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp', 'severity']),
            models.Index(fields=['event_type', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
            models.Index(fields=['resolved', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.get_event_type_display()} from {self.ip_address} at {self.timestamp}"
