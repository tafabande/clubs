"""
User models for MSU Platform.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator
import uuid
from datetime import datetime, timedelta


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        # Check if user already exists to make seeding idempotent
        user = self.filter(email=email).first()
        if user:
            # If user exists, ensure they are a superuser
            updated = False
            if not user.is_superuser:
                user.is_superuser = True
                updated = True
            if not user.is_staff:
                user.is_staff = True
                updated = True
            if not user.is_verified:
                user.is_verified = True
                updated = True
            
            if updated:
                user.save(using=self._db)
            return user

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for MSU Platform."""

    FACULTY_CHOICES = [
        ('agriculture', 'Faculty of Agriculture'),
        ('arts', 'Faculty of Arts'),
        ('commerce', 'Faculty of Commerce'),
        ('education', 'Faculty of Education'),
        ('law', 'Faculty of Law'),
        ('science', 'Faculty of Science'),
        ('social_sciences', 'Faculty of Social Sciences'),
    ]

    YEAR_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
        (5, 'Year 5'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text='e.g., MSU000001234')

    # Personal Information
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)

    # MSU-specific fields
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)

    # Social Profile
    bio = models.TextField(max_length=500, blank=True)
    interests = models.CharField(max_length=500, blank=True, help_text='Comma-separated interests (e.g., coding, music, sports)')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # Status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Denormalized counts
    followers_count_val = models.IntegerField(default=0, db_column='followers_count')
    following_count_val = models.IntegerField(default=0, db_column='following_count')
    posts_count = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='users_email_idx'),
            models.Index(fields=['student_id'], name='users_student_id_idx'),
            models.Index(fields=['faculty'], name='users_faculty_idx'),
            models.Index(fields=['department'], name='users_department_idx'),
            models.Index(fields=['is_active', 'is_verified'], name='users_status_idx'),
            models.Index(fields=['faculty', 'department'], name='users_faculty_dept_idx'),
            models.Index(fields=['-created_at'], name='users_created_idx'),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the user's first name."""
        return self.first_name

    @property
    def followers_count(self):
        """Count of users following this user (denormalized)."""
        return self.followers_count_val

    @property
    def following_count(self):
        """Count of users this user is following (denormalized)."""
        return self.following_count_val

    @property
    def organizations_following_count(self):
        """Count of organizations this user follows."""
        return self.following_organizations.count()


class UserFollow(models.Model):
    """
    User-to-user following relationship.

    Allows users to follow each other for social networking.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        help_text='User who is following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        help_text='User being followed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_follows'
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]

    def __str__(self):
        return f"{self.follower.email} follows {self.following.email}"

    def clean(self):
        """Validate that user cannot follow themselves."""
        from django.core.exceptions import ValidationError
        if self.follower == self.following:
            raise ValidationError("Users cannot follow themselves")


class RefreshToken(models.Model):
    """Store refresh tokens for JWT authentication."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = 'refresh_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='refresh_token_user_idx'),
            models.Index(fields=['token'], name='refresh_token_token_idx'),
            models.Index(fields=['revoked', 'expires_at'], name='refresh_token_status_idx'),
        ]

    def __str__(self):
        return f"Token for {self.user.email} (expires: {self.expires_at})"

    def is_valid(self):
        """Check if token is valid (not expired and not revoked)."""
        from django.utils import timezone
        return not self.revoked and self.expires_at > timezone.now()


class UserSession(models.Model):
    """Track user sessions for multi-device authentication."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    device_info = models.CharField(max_length=500, blank=True, help_text='User agent string')
    ip_address = models.GenericIPAddressField()
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'user_sessions'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', '-last_activity'], name='user_session_user_idx'),
            models.Index(fields=['session_key'], name='user_session_key_idx'),
            models.Index(fields=['expires_at'], name='user_session_expires_idx'),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.device_info[:50]}"

    def is_expired(self):
        """Check if session is expired."""
        from django.utils import timezone
        return self.expires_at < timezone.now()


class PasswordResetToken(models.Model):
    """Store password reset tokens."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='pwd_reset_user_idx'),
            models.Index(fields=['token'], name='pwd_reset_token_idx'),
            models.Index(fields=['used', 'expires_at'], name='pwd_reset_status_idx'),
        ]

    def __str__(self):
        return f"Password reset for {self.user.email}"

    def is_valid(self):
        """Check if token is valid (not used and not expired)."""
        from django.utils import timezone
        return not self.used and self.expires_at > timezone.now()


class EmailVerificationToken(models.Model):
    """Store email verification tokens."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'email_verification_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='email_verify_user_idx'),
            models.Index(fields=['token'], name='email_verify_token_idx'),
            models.Index(fields=['verified', 'expires_at'], name='email_verify_status_idx'),
        ]

    def __str__(self):
        return f"Email verification for {self.user.email}"

    def is_valid(self):
        """Check if token is valid (not verified and not expired)."""
        from django.utils import timezone
        return not self.verified and self.expires_at > timezone.now()
