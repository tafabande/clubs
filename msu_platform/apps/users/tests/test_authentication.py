"""
Tests for authentication endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from apps.core.tests.utils import (
    create_test_user,
    create_password_reset_token,
    create_email_verification_token,
)

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.authentication
class TestUserRegistration:
    """Test user registration endpoint."""

    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        url = reverse('users:register')
        data = {
            'email': 'newuser@msu.ac.zw',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'student_id': 'MSU000012345',
            'faculty': 'science',
            'year_of_study': 2,
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
        assert response.data['user']['email'] == 'newuser@msu.ac.zw'

        # Verify user was created
        user = User.objects.get(email='newuser@msu.ac.zw')
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        assert user.is_verified is False  # Email not verified initially

    def test_register_user_invalid_email(self, api_client):
        """Test registration with invalid email."""
        url = reverse('users:register')
        data = {
            'email': 'invalid-email',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_user_password_mismatch(self, api_client):
        """Test registration with mismatched passwords."""
        url = reverse('users:register')
        data = {
            'email': 'test@msu.ac.zw',
            'password': 'StrongPass123!',
            'password_confirm': 'DifferentPass123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_weak_password(self, api_client):
        """Test registration with weak password."""
        url = reverse('users:register')
        data = {
            'email': 'test@msu.ac.zw',
            'password': '12345',
            'password_confirm': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_duplicate_email(self, api_client, user):
        """Test registration with existing email."""
        url = reverse('users:register')
        data = {
            'email': user.email,
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_user_missing_required_fields(self, api_client):
        """Test registration with missing required fields."""
        url = reverse('users:register')
        data = {
            'email': 'test@msu.ac.zw',
            'password': 'StrongPass123!',
            # Missing first_name and last_name
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.authentication
class TestUserLogin:
    """Test user login endpoint."""

    def test_login_success(self, api_client):
        """Test successful login."""
        user = create_test_user(email='test@msu.ac.zw', password='testpass123')

        url = reverse('users:login')
        data = {
            'email': 'test@msu.ac.zw',
            'password': 'testpass123',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data

    def test_login_invalid_credentials(self, api_client, user):
        """Test login with invalid credentials."""
        url = reverse('users:login')
        data = {
            'email': user.email,
            'password': 'wrongpassword',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent email."""
        url = reverse('users:login')
        data = {
            'email': 'nonexistent@msu.ac.zw',
            'password': 'testpass123',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user(self, api_client):
        """Test login with inactive user."""
        user = create_test_user(is_active=False)

        url = reverse('users:login')
        data = {
            'email': user.email,
            'password': 'testpass123',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.authentication
class TestTokenRefresh:
    """Test token refresh endpoint."""

    def test_refresh_token_success(self, api_client, user):
        """Test successful token refresh."""
        # Get initial tokens
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)

        url = reverse('users:token_refresh')
        data = {'refresh': refresh_token}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_refresh_token_invalid(self, api_client):
        """Test refresh with invalid token."""
        url = reverse('users:token_refresh')
        data = {'refresh': 'invalid_token'}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.authentication
class TestLogout:
    """Test logout endpoints."""

    def test_logout_success(self, authenticated_client, user):
        """Test successful logout."""
        url = reverse('users:logout')

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK

    def test_logout_unauthenticated(self, api_client):
        """Test logout without authentication."""
        url = reverse('users:logout')

        response = api_client.post(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_all_devices(self, authenticated_client, user):
        """Test logout from all devices."""
        url = reverse('users:logout_all')

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.authentication
class TestEmailVerification:
    """Test email verification endpoints."""

    def test_send_verification_email(self, api_client, user):
        """Test sending verification email."""
        url = reverse('users:send_verification_email')
        data = {'email': user.email}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

    def test_verify_email_success(self, api_client):
        """Test successful email verification."""
        user = create_test_user(is_verified=False)
        token = create_email_verification_token(user)

        url = reverse('users:verify_email')
        data = {'token': token.token}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

        # Verify user is now verified
        user.refresh_from_db()
        assert user.is_verified is True

    def test_verify_email_invalid_token(self, api_client):
        """Test email verification with invalid token."""
        url = reverse('users:verify_email')
        data = {'token': 'invalid_token'}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_email_expired_token(self, api_client):
        """Test email verification with expired token."""
        user = create_test_user(is_verified=False)
        token = create_email_verification_token(user)

        # Expire the token
        token.expires_at = timezone.now() - timedelta(days=1)
        token.save()

        url = reverse('users:verify_email')
        data = {'token': token.token}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.authentication
class TestPasswordReset:
    """Test password reset endpoints."""

    def test_request_password_reset(self, api_client, user):
        """Test requesting password reset."""
        url = reverse('users:password_reset_request')
        data = {'email': user.email}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

    def test_request_password_reset_nonexistent_email(self, api_client):
        """Test password reset with non-existent email."""
        url = reverse('users:password_reset_request')
        data = {'email': 'nonexistent@msu.ac.zw'}

        response = api_client.post(url, data, format='json')

        # Should still return 200 for security
        assert response.status_code == status.HTTP_200_OK

    def test_password_reset_confirm_success(self, api_client, user):
        """Test successful password reset confirmation."""
        token = create_password_reset_token(user)

        url = reverse('users:password_reset_confirm')
        data = {
            'token': token.token,
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'NewStrongPass123!',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

        # Verify password was changed
        user.refresh_from_db()
        assert user.check_password('NewStrongPass123!')

    def test_password_reset_confirm_invalid_token(self, api_client):
        """Test password reset with invalid token."""
        url = reverse('users:password_reset_confirm')
        data = {
            'token': 'invalid_token',
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'NewStrongPass123!',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_confirm_password_mismatch(self, api_client, user):
        """Test password reset with mismatched passwords."""
        token = create_password_reset_token(user)

        url = reverse('users:password_reset_confirm')
        data = {
            'token': token.token,
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'DifferentPass123!',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_confirm_expired_token(self, api_client, user):
        """Test password reset with expired token."""
        token = create_password_reset_token(user)

        # Expire the token
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()

        url = reverse('users:password_reset_confirm')
        data = {
            'token': token.token,
            'new_password': 'NewStrongPass123!',
            'new_password_confirm': 'NewStrongPass123!',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
