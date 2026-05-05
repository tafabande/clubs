"""
Tests for User models.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from apps.users.models import (
    UserFollow,
    RefreshToken,
    UserSession,
    PasswordResetToken,
    EmailVerificationToken,
)
from apps.core.tests.utils import (
    create_test_user,
    create_refresh_token,
    create_password_reset_token,
    create_email_verification_token,
)

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = create_test_user(
            email="test@msu.ac.zw",
            first_name="John",
            last_name="Doe",
        )

        assert user.email == "test@msu.ac.zw"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.is_verified is True

    def test_create_user_without_email(self):
        """Test creating user without email raises error."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@msu.ac.zw",
            password="testpass123",
            first_name="Admin",
            last_name="User",
        )

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_verified is True

    def test_user_str_representation(self):
        """Test user string representation."""
        user = create_test_user(
            email="test@msu.ac.zw",
            first_name="John",
            last_name="Doe",
        )

        assert str(user) == "John Doe (test@msu.ac.zw)"

    def test_get_full_name(self):
        """Test get_full_name method."""
        user = create_test_user(first_name="John", last_name="Doe")
        assert user.get_full_name() == "John Doe"

    def test_get_short_name(self):
        """Test get_short_name method."""
        user = create_test_user(first_name="John", last_name="Doe")
        assert user.get_short_name() == "John"

    def test_email_uniqueness(self):
        """Test that email must be unique."""
        create_test_user(email="test@msu.ac.zw")

        with pytest.raises(Exception):  # IntegrityError
            create_test_user(email="test@msu.ac.zw")

    def test_student_id_uniqueness(self):
        """Test that student_id must be unique."""
        create_test_user(student_id="MSU000001234")

        with pytest.raises(Exception):  # IntegrityError
            create_test_user(student_id="MSU000001234")

    def test_faculty_choices(self):
        """Test faculty field choices."""
        user = create_test_user(faculty="science")
        assert user.faculty == "science"

    def test_year_of_study_choices(self):
        """Test year_of_study field choices."""
        user = create_test_user(year_of_study=3)
        assert user.year_of_study == 3

    def test_followers_count_property(self):
        """Test followers_count property."""
        user1 = create_test_user()
        user2 = create_test_user()
        user3 = create_test_user()

        # Create follows
        UserFollow.objects.create(follower=user2, following=user1)
        UserFollow.objects.create(follower=user3, following=user1)

        assert user1.followers_count == 2

    def test_following_count_property(self):
        """Test following_count property."""
        user1 = create_test_user()
        user2 = create_test_user()
        user3 = create_test_user()

        # User1 follows user2 and user3
        UserFollow.objects.create(follower=user1, following=user2)
        UserFollow.objects.create(follower=user1, following=user3)

        assert user1.following_count == 2


@pytest.mark.django_db
class TestUserFollowModel:
    """Test UserFollow model."""

    def test_create_follow(self):
        """Test creating a follow relationship."""
        user1 = create_test_user()
        user2 = create_test_user()

        follow = UserFollow.objects.create(follower=user1, following=user2)

        assert follow.follower == user1
        assert follow.following == user2
        assert follow.created_at is not None

    def test_follow_str_representation(self):
        """Test follow string representation."""
        user1 = create_test_user(email="user1@msu.ac.zw")
        user2 = create_test_user(email="user2@msu.ac.zw")

        follow = UserFollow.objects.create(follower=user1, following=user2)

        assert str(follow) == "user1@msu.ac.zw follows user2@msu.ac.zw"

    def test_cannot_follow_self(self):
        """Test that user cannot follow themselves."""
        user = create_test_user()

        follow = UserFollow(follower=user, following=user)

        with pytest.raises(ValidationError, match="Users cannot follow themselves"):
            follow.clean()

    def test_unique_follow_constraint(self):
        """Test that follow relationship must be unique."""
        user1 = create_test_user()
        user2 = create_test_user()

        UserFollow.objects.create(follower=user1, following=user2)

        with pytest.raises(Exception):  # IntegrityError
            UserFollow.objects.create(follower=user1, following=user2)


@pytest.mark.django_db
class TestRefreshTokenModel:
    """Test RefreshToken model."""

    def test_create_refresh_token(self):
        """Test creating a refresh token."""
        user = create_test_user()
        token = create_refresh_token(user)

        assert token.user == user
        assert token.token is not None
        assert token.revoked is False
        assert token.expires_at > timezone.now()

    def test_token_str_representation(self):
        """Test token string representation."""
        user = create_test_user(email="test@msu.ac.zw")
        token = create_refresh_token(user)

        assert "test@msu.ac.zw" in str(token)
        assert "expires" in str(token)

    def test_is_valid_method(self):
        """Test is_valid method."""
        user = create_test_user()
        token = create_refresh_token(user)

        assert token.is_valid() is True

    def test_is_valid_revoked_token(self):
        """Test is_valid returns False for revoked token."""
        user = create_test_user()
        token = create_refresh_token(user, revoked=True)

        assert token.is_valid() is False

    def test_is_valid_expired_token(self):
        """Test is_valid returns False for expired token."""
        user = create_test_user()
        token = create_refresh_token(user)

        # Manually set expiration to past
        token.expires_at = timezone.now() - timedelta(days=1)
        token.save()

        assert token.is_valid() is False


@pytest.mark.django_db
class TestUserSessionModel:
    """Test UserSession model."""

    def test_create_session(self):
        """Test creating a user session."""
        user = create_test_user()

        session = UserSession.objects.create(
            user=user,
            session_key="test_session_key",
            device_info="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            ip_address="192.168.1.1",
            expires_at=timezone.now() + timedelta(days=7),
        )

        assert session.user == user
        assert session.session_key == "test_session_key"
        assert session.ip_address == "192.168.1.1"

    def test_is_expired_method(self):
        """Test is_expired method."""
        user = create_test_user()

        session = UserSession.objects.create(
            user=user,
            session_key="test_key",
            ip_address="192.168.1.1",
            expires_at=timezone.now() + timedelta(days=7),
        )

        assert session.is_expired() is False

    def test_is_expired_past_expiration(self):
        """Test is_expired returns True for expired session."""
        user = create_test_user()

        session = UserSession.objects.create(
            user=user,
            session_key="test_key",
            ip_address="192.168.1.1",
            expires_at=timezone.now() - timedelta(days=1),
        )

        assert session.is_expired() is True


@pytest.mark.django_db
class TestPasswordResetTokenModel:
    """Test PasswordResetToken model."""

    def test_create_password_reset_token(self):
        """Test creating a password reset token."""
        user = create_test_user()
        token = create_password_reset_token(user)

        assert token.user == user
        assert token.token is not None
        assert token.used is False
        assert token.expires_at > timezone.now()

    def test_is_valid_method(self):
        """Test is_valid method."""
        user = create_test_user()
        token = create_password_reset_token(user)

        assert token.is_valid() is True

    def test_is_valid_used_token(self):
        """Test is_valid returns False for used token."""
        user = create_test_user()
        token = create_password_reset_token(user, used=True)

        assert token.is_valid() is False

    def test_is_valid_expired_token(self):
        """Test is_valid returns False for expired token."""
        user = create_test_user()
        token = create_password_reset_token(user)

        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()

        assert token.is_valid() is False


@pytest.mark.django_db
class TestEmailVerificationTokenModel:
    """Test EmailVerificationToken model."""

    def test_create_email_verification_token(self):
        """Test creating an email verification token."""
        user = create_test_user(is_verified=False)
        token = create_email_verification_token(user)

        assert token.user == user
        assert token.token is not None
        assert token.verified is False
        assert token.expires_at > timezone.now()

    def test_is_valid_method(self):
        """Test is_valid method."""
        user = create_test_user(is_verified=False)
        token = create_email_verification_token(user)

        assert token.is_valid() is True

    def test_is_valid_verified_token(self):
        """Test is_valid returns False for verified token."""
        user = create_test_user()
        token = create_email_verification_token(user, verified=True)

        assert token.is_valid() is False

    def test_is_valid_expired_token(self):
        """Test is_valid returns False for expired token."""
        user = create_test_user(is_verified=False)
        token = create_email_verification_token(user)

        token.expires_at = timezone.now() - timedelta(days=1)
        token.save()

        assert token.is_valid() is False
