"""
Tests for user follow functionality.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from apps.users.models import UserFollow
from apps.core.tests.utils import create_test_user, assert_paginated_response

User = get_user_model()


@pytest.mark.django_db
class TestUserFollow:
    """Test user follow endpoints."""

    def test_follow_user(self, authenticated_client, user, user2):
        """Test following another user."""
        url = reverse('users:follow', kwargs={'pk': user2.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert UserFollow.objects.filter(follower=user, following=user2).exists()

    def test_follow_user_already_following(self, authenticated_client, user, user2):
        """Test following user that is already followed."""
        # Create existing follow
        UserFollow.objects.create(follower=user, following=user2)

        url = reverse('users:follow', kwargs={'pk': user2.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_follow_self(self, authenticated_client, user):
        """Test that user cannot follow themselves."""
        url = reverse('users:follow', kwargs={'pk': user.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_follow_nonexistent_user(self, authenticated_client):
        """Test following non-existent user."""
        url = reverse('users:follow', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unfollow_user(self, authenticated_client, user, user2):
        """Test unfollowing a user."""
        # Create follow relationship
        UserFollow.objects.create(follower=user, following=user2)

        url = reverse('users:unfollow', kwargs={'pk': user2.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not UserFollow.objects.filter(follower=user, following=user2).exists()

    def test_unfollow_user_not_following(self, authenticated_client, user, user2):
        """Test unfollowing user that is not followed."""
        url = reverse('users:unfollow', kwargs={'pk': user2.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_check_follow_status(self, authenticated_client, user, user2):
        """Test checking if user is followed."""
        # Create follow relationship
        UserFollow.objects.create(follower=user, following=user2)

        url = reverse('users:follow_status', kwargs={'pk': user2.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_following'] is True

    def test_check_follow_status_not_following(self, authenticated_client, user, user2):
        """Test checking follow status when not following."""
        url = reverse('users:follow_status', kwargs={'pk': user2.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_following'] is False


@pytest.mark.django_db
class TestFollowersList:
    """Test listing followers."""

    def test_get_followers_list(self, authenticated_client, user):
        """Test retrieving list of followers."""
        # Create followers
        for i in range(5):
            follower = create_test_user(email=f'follower{i}@msu.ac.zw')
            UserFollow.objects.create(follower=follower, following=user)

        url = reverse('users:followers', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) == 5

    def test_get_followers_empty_list(self, authenticated_client, user):
        """Test retrieving followers when user has none."""
        url = reverse('users:followers', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) == 0

    def test_get_followers_pagination(self, authenticated_client, user):
        """Test followers list pagination."""
        # Create 25 followers
        for i in range(25):
            follower = create_test_user(email=f'follower{i}@msu.ac.zw')
            UserFollow.objects.create(follower=follower, following=user)

        url = reverse('users:followers', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 25
        assert len(response.data['results']) == 20  # Default page size


@pytest.mark.django_db
class TestFollowingList:
    """Test listing users being followed."""

    def test_get_following_list(self, authenticated_client, user):
        """Test retrieving list of users being followed."""
        # Create following relationships
        for i in range(5):
            following_user = create_test_user(email=f'following{i}@msu.ac.zw')
            UserFollow.objects.create(follower=user, following=following_user)

        url = reverse('users:following', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) == 5

    def test_get_following_empty_list(self, authenticated_client, user):
        """Test retrieving following when user follows no one."""
        url = reverse('users:following', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) == 0

    def test_get_following_with_search(self, authenticated_client, user):
        """Test searching within following list."""
        # Create following relationships
        john = create_test_user(email='john@msu.ac.zw', first_name='John', last_name='Doe')
        jane = create_test_user(email='jane@msu.ac.zw', first_name='Jane', last_name='Smith')

        UserFollow.objects.create(follower=user, following=john)
        UserFollow.objects.create(follower=user, following=jane)

        url = reverse('users:following', kwargs={'pk': user.id})

        response = authenticated_client.get(url, {'search': 'John'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert any(u['first_name'] == 'John' for u in response.data['results'])


@pytest.mark.django_db
class TestFollowCountUpdates:
    """Test that follow counts are updated correctly."""

    def test_follow_updates_count(self, authenticated_client, user, user2):
        """Test that following updates follower/following counts."""
        initial_user_following_count = user.following_count
        initial_user2_followers_count = user2.followers_count

        url = reverse('users:follow', kwargs={'pk': user2.id})
        authenticated_client.post(url)

        # Refresh from database
        user.refresh_from_db()
        user2.refresh_from_db()

        assert user.following_count == initial_user_following_count + 1
        assert user2.followers_count == initial_user2_followers_count + 1

    def test_unfollow_updates_count(self, authenticated_client, user, user2):
        """Test that unfollowing updates follower/following counts."""
        # Create follow relationship
        UserFollow.objects.create(follower=user, following=user2)

        initial_user_following_count = user.following_count
        initial_user2_followers_count = user2.followers_count

        url = reverse('users:unfollow', kwargs={'pk': user2.id})
        authenticated_client.delete(url)

        # Refresh from database
        user.refresh_from_db()
        user2.refresh_from_db()

        assert user.following_count == initial_user_following_count - 1
        assert user2.followers_count == initial_user2_followers_count - 1


@pytest.mark.django_db
class TestMutualFollows:
    """Test mutual follow relationships."""

    def test_mutual_follow(self, authenticated_client, user, user2):
        """Test mutual follow relationship."""
        # User1 follows User2
        UserFollow.objects.create(follower=user, following=user2)

        # User2 follows User1
        client2, _ = create_test_user(user2)
        url = reverse('users:follow', kwargs={'pk': user.id})

        from apps.core.tests.utils import create_authenticated_client
        client2, _ = create_authenticated_client(user2)
        response = client2.post(url)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify mutual follow
        assert UserFollow.objects.filter(follower=user, following=user2).exists()
        assert UserFollow.objects.filter(follower=user2, following=user).exists()

    def test_get_mutual_followers(self, authenticated_client, user, user2, user3):
        """Test getting mutual followers."""
        # User2 and User3 both follow User1
        UserFollow.objects.create(follower=user2, following=user)
        UserFollow.objects.create(follower=user3, following=user)

        # User1 follows User2 (mutual) but not User3
        UserFollow.objects.create(follower=user, following=user2)

        url = reverse('users:mutual_followers', kwargs={'pk': user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Should only include User2 (mutual follow)
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == str(user2.id)
