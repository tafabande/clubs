"""
Add performance indexes to User and related models.

This migration adds database indexes to improve query performance for:
- User lookups
- Session management
- Token validation
- Follow relationships
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # Adjust this based on your previous migrations
    ]

    operations = [
        # User model indexes
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='users_email_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['student_id'], name='users_student_id_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['faculty'], name='users_faculty_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['department'], name='users_department_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['is_active', 'is_verified'], name='users_status_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['faculty', 'department'], name='users_faculty_dept_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['-created_at'], name='users_created_idx'),
        ),

        # RefreshToken indexes
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['user', '-created_at'], name='refresh_token_user_idx'),
        ),
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['token'], name='refresh_token_token_idx'),
        ),
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['revoked', 'expires_at'], name='refresh_token_status_idx'),
        ),

        # UserSession indexes
        migrations.AddIndex(
            model_name='usersession',
            index=models.Index(fields=['user', '-last_activity'], name='user_session_user_idx'),
        ),
        migrations.AddIndex(
            model_name='usersession',
            index=models.Index(fields=['session_key'], name='user_session_key_idx'),
        ),
        migrations.AddIndex(
            model_name='usersession',
            index=models.Index(fields=['expires_at'], name='user_session_expires_idx'),
        ),

        # PasswordResetToken indexes
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['user', '-created_at'], name='pwd_reset_user_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['token'], name='pwd_reset_token_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['used', 'expires_at'], name='pwd_reset_status_idx'),
        ),

        # EmailVerificationToken indexes
        migrations.AddIndex(
            model_name='emailverificationtoken',
            index=models.Index(fields=['user', '-created_at'], name='email_verify_user_idx'),
        ),
        migrations.AddIndex(
            model_name='emailverificationtoken',
            index=models.Index(fields=['token'], name='email_verify_token_idx'),
        ),
        migrations.AddIndex(
            model_name='emailverificationtoken',
            index=models.Index(fields=['verified', 'expires_at'], name='email_verify_status_idx'),
        ),
    ]
