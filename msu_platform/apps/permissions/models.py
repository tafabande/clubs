"""
RBAC models for MSU Platform.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.users.models import User
import uuid


class Permission(models.Model):
    """Represent a permission that can be granted to roles."""

    RESOURCE_TYPES = [
        ('club', 'Club'),
        ('church', 'Church'),
        ('sports_team', 'Sports Team'),
        ('activity', 'Activity'),
        ('system', 'System'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codename = models.CharField(max_length=100, unique=True, help_text='e.g., can_create_club')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permissions'
        ordering = ['resource_type', 'codename']

    def __str__(self):
        return f"{self.name} ({self.codename})"


class Role(models.Model):
    """Represent a role that can be assigned to users."""

    ORGANIZATION_TYPES = [
        ('club', 'Club'),
        ('church', 'Church'),
        ('sports_team', 'Sports Team'),
        ('activity', 'Activity'),
        ('system', 'System'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text='e.g., Club President')
    description = models.TextField(blank=True)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES)
    is_system_role = models.BooleanField(default=False, help_text='System roles are platform-wide')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        ordering = ['organization_type', 'name']

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """Many-to-many relationship between roles and permissions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserRole(models.Model):
    """Assign roles to users for specific organizations."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    # Generic foreign key to organization (Club, Church, SportsTeam, Activity)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)
    organization = GenericForeignKey('content_type', 'object_id')

    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_roles')
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Leave blank for no expiration')

    class Meta:
        db_table = 'user_roles'
        ordering = ['-granted_at']
        indexes = [
            models.Index(fields=['user', 'role']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        org_str = f" for {self.organization}" if self.organization else ""
        return f"{self.user.get_full_name()} - {self.role.name}{org_str}"

    def is_expired(self):
        """Check if role assignment is expired."""
        if not self.expires_at:
            return False
        from django.utils import timezone
        return self.expires_at < timezone.now()
