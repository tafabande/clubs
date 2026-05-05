"""
DRF permission classes for MSU Platform.
"""
from rest_framework.permissions import BasePermission
from .services import PermissionService


class HasPermission(BasePermission):
    """
    Check if user has a specific permission.
    Set permission_codename in view.
    """

    def has_permission(self, request, view):
        """Check permission for the view."""
        if not request.user or not request.user.is_authenticated:
            return False

        permission_codename = getattr(view, 'permission_codename', None)
        if not permission_codename:
            return True

        return PermissionService.check_user_permission(request.user, permission_codename)

    def has_object_permission(self, request, view, obj):
        """Check permission for a specific object."""
        if not request.user or not request.user.is_authenticated:
            return False

        permission_codename = getattr(view, 'permission_codename', None)
        if not permission_codename:
            return True

        return PermissionService.check_user_permission(request.user, permission_codename, obj)


class IsOrganizationAdmin(BasePermission):
    """
    Check if user has admin role for the organization.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is admin of the organization."""
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Check if user is creator
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True

        # Check admin roles
        admin_roles = ['Club President', 'Club Admin', 'Church Leader', 'Team Captain', 'Activity Coordinator']
        user_roles = PermissionService.get_user_roles(request.user, obj)

        for user_role in user_roles:
            if not user_role.is_expired() and user_role.role.name in admin_roles:
                return True

        return False


class IsOrganizationMember(BasePermission):
    """
    Check if user is a member of the organization.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is member of the organization."""
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Check if user is creator
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True

        # Check membership
        # This will be implemented based on organization type
        # For now, check if user has any role in the organization
        user_roles = PermissionService.get_user_roles(request.user, obj)
        return user_roles.exists()
