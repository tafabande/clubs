"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RefreshToken, UserSession, EmailVerificationToken, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for User model."""

    list_display = ['email', 'first_name', 'last_name', 'student_id', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_verified', 'faculty', 'year_of_study']
    search_fields = ['email', 'first_name', 'last_name', 'student_id']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'student_id')}),
        ('Academic info', {'fields': ('faculty', 'department', 'year_of_study')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    """Admin for RefreshToken model."""

    list_display = ['user', 'created_at', 'expires_at', 'revoked']
    list_filter = ['revoked', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin for UserSession model."""

    list_display = ['user', 'device_info', 'ip_address', 'last_activity', 'expires_at']
    list_filter = ['last_activity']
    search_fields = ['user__email', 'ip_address']
    readonly_fields = ['session_key', 'last_activity']


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """Admin for EmailVerificationToken model."""

    list_display = ['user', 'created_at', 'expires_at', 'verified']
    list_filter = ['verified', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin for PasswordResetToken model."""

    list_display = ['user', 'created_at', 'expires_at', 'used']
    list_filter = ['used', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at']
