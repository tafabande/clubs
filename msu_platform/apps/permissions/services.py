"""
Permission service for checking user permissions.
"""
from django.contrib.contenttypes.models import ContentType
from .models import Permission, Role, RolePermission, UserRole


class PermissionService:
    """Service for managing permissions."""

    @staticmethod
    def check_user_permission(user, codename, organization=None):
        """
        Check if user has a specific permission.

        Args:
            user: User object
            codename: Permission codename (e.g., 'can_create_club')
            organization: Optional organization object to check role-based permissions

        Returns:
            bool: True if user has permission
        """
        # Superusers have all permissions
        if user.is_superuser:
            return True

        # Get permission
        try:
            permission = Permission.objects.get(codename=codename, is_active=True)
        except Permission.DoesNotExist:
            return False

        # If checking organization-specific permission
        if organization:
            content_type = ContentType.objects.get_for_model(organization)
            user_roles = UserRole.objects.filter(
                user=user,
                content_type=content_type,
                object_id=organization.id
            ).select_related('role')

            for user_role in user_roles:
                if not user_role.is_expired():
                    if RolePermission.objects.filter(
                        role=user_role.role,
                        permission=permission
                    ).exists():
                        return True

        # Check system-wide roles
        system_roles = UserRole.objects.filter(
            user=user,
            content_type__isnull=True,
            object_id__isnull=True
        ).select_related('role')

        for user_role in system_roles:
            if not user_role.is_expired():
                if RolePermission.objects.filter(
                    role=user_role.role,
                    permission=permission
                ).exists():
                    return True

        return False

    @staticmethod
    def assign_role(user, role, organization=None, granted_by=None, expires_at=None):
        """
        Assign a role to a user.

        Args:
            user: User object
            role: Role object or role name
            organization: Optional organization object
            granted_by: User who granted the role
            expires_at: Optional expiration datetime

        Returns:
            UserRole object
        """
        if isinstance(role, str):
            role = Role.objects.get(name=role)

        content_type = None
        object_id = None

        if organization:
            content_type = ContentType.objects.get_for_model(organization)
            object_id = organization.id

        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            content_type=content_type,
            object_id=object_id,
            defaults={
                'granted_by': granted_by,
                'expires_at': expires_at
            }
        )

        return user_role

    @staticmethod
    def get_user_permissions(user, organization=None):
        """
        Get all permissions for a user.

        Args:
            user: User object
            organization: Optional organization object

        Returns:
            QuerySet of Permission objects
        """
        if user.is_superuser:
            return Permission.objects.filter(is_active=True)

        permission_ids = set()

        # Get organization-specific permissions
        if organization:
            content_type = ContentType.objects.get_for_model(organization)
            user_roles = UserRole.objects.filter(
                user=user,
                content_type=content_type,
                object_id=organization.id
            ).select_related('role')

            for user_role in user_roles:
                if not user_role.is_expired():
                    role_perms = RolePermission.objects.filter(
                        role=user_role.role
                    ).values_list('permission_id', flat=True)
                    permission_ids.update(role_perms)

        # Get system-wide permissions
        system_roles = UserRole.objects.filter(
            user=user,
            content_type__isnull=True,
            object_id__isnull=True
        ).select_related('role')

        for user_role in system_roles:
            if not user_role.is_expired():
                role_perms = RolePermission.objects.filter(
                    role=user_role.role
                ).values_list('permission_id', flat=True)
                permission_ids.update(role_perms)

        return Permission.objects.filter(id__in=permission_ids, is_active=True)

    @staticmethod
    def get_user_roles(user, organization=None):
        """
        Get all roles for a user.

        Args:
            user: User object
            organization: Optional organization object

        Returns:
            QuerySet of Role objects
        """
        query = UserRole.objects.filter(user=user)

        if organization:
            content_type = ContentType.objects.get_for_model(organization)
            query = query.filter(content_type=content_type, object_id=organization.id)

        return query.select_related('role')
