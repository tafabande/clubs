"""
Tests for User views and API endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from apps.core.tests.utils import (
    create_test_user,
    create_authenticated_client,
    assert_paginated_response,
)

User = get_user_model()


@pytest.mark.django_db
class TestUserProfileViews:
    """Test user profile related views."""

    def test_get_current_user(self, authenticated_client, user):
        """Test retrieving current user profile."""
        url = reverse('users:me')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name

    def test_get_current_user_unauthenticated(self, api_client):
        """Test retrieving current user without authentication."""
        url = reverse('users:me')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_current_user(self, authenticated_client, user):
        """Test updating current user profile."""
        url = reverse('users:me')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '+263712345678',
            'department': 'Computer Science',
        }

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
        assert response.data['phone'] == '+263712345678'

        # Verify database was updated
        user.refresh_from_db()
        assert user.first_name == 'Updated'

    def test_update_email_not_allowed(self, authenticated_client, user):
        """Test that email cannot be updated."""
        url = reverse('users:me')
        original_email = user.email
        data = {'email': 'newemail@msu.ac.zw'}

        response = authenticated_client.patch(url, data, format='json')

        # Email should not change
        user.refresh_from_db()
        assert user.email == original_email

    def test_get_user_by_id(self, authenticated_client, user2):
        """Test retrieving user by ID."""
        url = reverse('users:detail', kwargs={'pk': user2.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user2.email

    def test_get_user_by_id_not_found(self, authenticated_client):
        """Test retrieving non-existent user."""
        url = reverse('users:detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUserListViews:
    """Test user listing and search views."""

    def test_list_users(self, authenticated_client):
        """Test listing users."""
        # Create multiple users
        for i in range(5):
            create_test_user(email=f'user{i}@msu.ac.zw')

        url = reverse('users:list')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) >= 5

    def test_list_users_pagination(self, authenticated_client):
        """Test user list pagination."""
        # Create 25 users
        for i in range(25):
            create_test_user(email=f'user{i}@msu.ac.zw')

        url = reverse('users:list')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert response.data['count'] >= 25
        assert len(response.data['results']) == 20  # Default page size

        # Test second page
        response = authenticated_client.get(url, {'page': 2})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 5

    def test_search_users_by_name(self, authenticated_client):
        """Test searching users by name."""
        create_test_user(email='john@msu.ac.zw', first_name='John', last_name='Doe')
        create_test_user(email='jane@msu.ac.zw', first_name='Jane', last_name='Smith')

        url = reverse('users:list')

        response = authenticated_client.get(url, {'search': 'John'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert any(u['first_name'] == 'John' for u in response.data['results'])

    def test_search_users_by_email(self, authenticated_client):
        """Test searching users by email."""
        create_test_user(email='john.doe@msu.ac.zw')

        url = reverse('users:list')

        response = authenticated_client.get(url, {'search': 'john.doe'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_filter_users_by_faculty(self, authenticated_client):
        """Test filtering users by faculty."""
        create_test_user(faculty='science')
        create_test_user(faculty='arts')
        create_test_user(faculty='science')

        url = reverse('users:list')

        response = authenticated_client.get(url, {'faculty': 'science'})

        assert response.status_code == status.HTTP_200_OK
        assert all(u['faculty'] == 'science' for u in response.data['results'])

    def test_filter_users_by_year(self, authenticated_client):
        """Test filtering users by year of study."""
        create_test_user(year_of_study=2)
        create_test_user(year_of_study=3)
        create_test_user(year_of_study=2)

        url = reverse('users:list')

        response = authenticated_client.get(url, {'year_of_study': 2})

        assert response.status_code == status.HTTP_200_OK
        assert all(u['year_of_study'] == 2 for u in response.data['results'])

    def test_list_users_unauthenticated(self, api_client):
        """Test listing users without authentication."""
        url = reverse('users:list')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfileUpdate:
    """Test user profile update functionality."""

    def test_update_profile_picture(self, authenticated_client, user, mock_s3):
        """Test updating profile picture."""
        from django.core.files.uploadedfile import SimpleUploadedFile

        url = reverse('users:me')
        image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        data = {'profile_picture': image}

        response = authenticated_client.patch(url, data, format='multipart')

        assert response.status_code == status.HTTP_200_OK

    def test_update_valid_fields(self, authenticated_client, user):
        """Test updating valid user fields."""
        url = reverse('users:me')
        data = {
            'phone': '+263771234567',
            'department': 'Computer Science',
            'year_of_study': 3,
        }

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['phone'] == '+263771234567'
        assert response.data['department'] == 'Computer Science'
        assert response.data['year_of_study'] == 3

    def test_partial_update(self, authenticated_client, user):
        """Test partial profile update."""
        url = reverse('users:me')
        data = {'phone': '+263771234567'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['phone'] == '+263771234567'
        # Other fields should remain unchanged
        assert response.data['first_name'] == user.first_name

    def test_update_invalid_faculty(self, authenticated_client, user):
        """Test updating with invalid faculty choice."""
        url = reverse('users:me')
        data = {'faculty': 'invalid_faculty'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_invalid_year(self, authenticated_client, user):
        """Test updating with invalid year of study."""
        url = reverse('users:me')
        data = {'year_of_study': 10}  # Invalid year

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserStatistics:
    """Test user statistics endpoints."""

    def test_get_user_statistics(self, authenticated_client, user):
        """Test retrieving user statistics."""
        from apps.users.models import UserFollow

        # Create some follows
        user2 = create_test_user()
        user3 = create_test_user()
        UserFollow.objects.create(follower=user2, following=user)
        UserFollow.objects.create(follower=user, following=user3)

        url = reverse('users:statistics', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'followers_count' in response.data
        assert 'following_count' in response.data
        assert response.data['followers_count'] == 1
        assert response.data['following_count'] == 1
