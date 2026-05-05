"""
Tests for Feed views and API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.organizations.models import Post, Comment, OrganizationFollow
from apps.core.tests.utils import (
    create_test_user,
    create_test_club,
    create_test_post,
    create_test_comment,
    assert_paginated_response,
)


@pytest.mark.django_db
@pytest.mark.feed
class TestPostCRUD:
    """Test Post CRUD operations."""

    def test_create_post(self, authenticated_client, user, club):
        """Test creating a post."""
        url = reverse('organizations:posts-list')
        data = {
            'organization': str(club.id),
            'post_type': 'text',
            'content': 'This is a test post',
            'visibility': 'public',
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'This is a test post'
        assert response.data['author']['id'] == str(user.id)

    def test_create_post_different_types(self, authenticated_client, club):
        """Test creating posts of different types."""
        url = reverse('organizations:posts-list')
        post_types = ['text', 'image', 'video', 'announcement', 'event', 'poll']

        for post_type in post_types:
            data = {
                'organization': str(club.id),
                'post_type': post_type,
                'content': f'Test {post_type} post',
                'visibility': 'public',
            }

            response = authenticated_client.post(url, data, format='json')

            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['post_type'] == post_type

    def test_create_post_unauthenticated(self, api_client, club):
        """Test creating post without authentication."""
        url = reverse('organizations:posts-list')
        data = {
            'organization': str(club.id),
            'content': 'Test post',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_posts(self, authenticated_client):
        """Test listing posts."""
        club = create_test_club()

        # Create posts
        for i in range(5):
            create_test_post(organization=club)

        url = reverse('organizations:posts-list')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) >= 5

    def test_get_post_detail(self, authenticated_client):
        """Test retrieving post detail."""
        post = create_test_post()

        url = reverse('organizations:posts-detail', kwargs={'pk': post.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == post.content

    def test_update_post_author(self, authenticated_client, user):
        """Test updating post as author."""
        post = create_test_post(author=user)

        url = reverse('organizations:posts-detail', kwargs={'pk': post.id})
        data = {'content': 'Updated content'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == 'Updated content'

    def test_update_post_non_author(self, authenticated_client):
        """Test updating post as non-author."""
        other_user = create_test_user()
        post = create_test_post(author=other_user)

        url = reverse('organizations:posts-detail', kwargs={'pk': post.id})
        data = {'content': 'Hacked content'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_post_author(self, authenticated_client, user):
        """Test deleting post as author."""
        post = create_test_post(author=user)

        url = reverse('organizations:posts-detail', kwargs={'pk': post.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(id=post.id).exists()

    def test_delete_post_non_author(self, authenticated_client):
        """Test deleting post as non-author."""
        other_user = create_test_user()
        post = create_test_post(author=other_user)

        url = reverse('organizations:posts-detail', kwargs={'pk': post.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.feed
class TestPostLikes:
    """Test post like functionality."""

    def test_like_post(self, authenticated_client, user):
        """Test liking a post."""
        post = create_test_post()

        url = reverse('organizations:posts-like', kwargs={'pk': post.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert user in post.likes.all()

    def test_unlike_post(self, authenticated_client, user):
        """Test unliking a post."""
        post = create_test_post()
        post.likes.add(user)

        url = reverse('organizations:posts-unlike', kwargs={'pk': post.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert user not in post.likes.all()

    def test_like_post_twice(self, authenticated_client, user):
        """Test liking same post twice."""
        post = create_test_post()

        url = reverse('organizations:posts-like', kwargs={'pk': post.id})

        # First like
        response1 = authenticated_client.post(url)
        assert response1.status_code == status.HTTP_200_OK

        # Second like (should be idempotent or return error)
        response2 = authenticated_client.post(url)
        assert response2.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_get_post_likes_count(self, authenticated_client):
        """Test getting post likes count."""
        post = create_test_post()

        # Add likes
        for i in range(5):
            user = create_test_user()
            post.likes.add(user)

        url = reverse('organizations:posts-detail', kwargs={'pk': post.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['likes_count'] == 5


@pytest.mark.django_db
@pytest.mark.feed
class TestComments:
    """Test comment functionality."""

    def test_create_comment(self, authenticated_client, user):
        """Test creating a comment."""
        post = create_test_post()

        url = reverse('organizations:comments-list', kwargs={'post_pk': post.id})
        data = {'content': 'Great post!'}

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'Great post!'
        assert response.data['author']['id'] == str(user.id)

    def test_create_nested_comment(self, authenticated_client, user):
        """Test creating a nested comment (reply)."""
        post = create_test_post()
        parent_comment = create_test_comment(post=post)

        url = reverse('organizations:comments-list', kwargs={'post_pk': post.id})
        data = {
            'content': 'Reply to comment',
            'parent': str(parent_comment.id),
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['parent'] == str(parent_comment.id)

    def test_list_comments(self, authenticated_client):
        """Test listing comments for a post."""
        post = create_test_post()

        # Create comments
        for i in range(5):
            create_test_comment(post=post, content=f'Comment {i}')

        url = reverse('organizations:comments-list', kwargs={'post_pk': post.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) == 5

    def test_update_comment_author(self, authenticated_client, user):
        """Test updating comment as author."""
        post = create_test_post()
        comment = create_test_comment(post=post, author=user)

        url = reverse('organizations:comments-detail', kwargs={
            'post_pk': post.id,
            'pk': comment.id
        })
        data = {'content': 'Updated comment'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == 'Updated comment'

    def test_delete_comment_author(self, authenticated_client, user):
        """Test deleting comment as author."""
        post = create_test_post()
        comment = create_test_comment(post=post, author=user)

        url = reverse('organizations:comments-detail', kwargs={
            'post_pk': post.id,
            'pk': comment.id
        })

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
@pytest.mark.feed
class TestFeedEndpoints:
    """Test feed generation endpoints."""

    def test_get_user_feed(self, authenticated_client, user):
        """Test getting user's personalized feed."""
        # User follows a club
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        # Create posts
        for i in range(10):
            create_test_post(organization=club)

        url = reverse('organizations:feed-user')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) > 0

    def test_get_discover_feed(self, authenticated_client):
        """Test getting discover feed."""
        # Create posts from various clubs
        for i in range(5):
            club = create_test_club()
            create_test_post(organization=club)

        url = reverse('organizations:feed-discover')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) > 0

    def test_get_organization_feed(self, authenticated_client):
        """Test getting posts for specific organization."""
        club = create_test_club()

        # Create posts
        for i in range(10):
            create_test_post(organization=club)

        url = reverse('organizations:feed-organization', kwargs={'org_id': club.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert all(p['organization']['id'] == str(club.id) for p in response.data['results'])

    def test_feed_pagination(self, authenticated_client, user):
        """Test feed pagination."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        # Create many posts
        for i in range(30):
            create_test_post(organization=club)

        url = reverse('organizations:feed-user')

        # First page
        response1 = authenticated_client.get(url, {'page': 1, 'page_size': 10})
        assert response1.status_code == status.HTTP_200_OK
        assert len(response1.data['results']) == 10

        # Second page
        response2 = authenticated_client.get(url, {'page': 2, 'page_size': 10})
        assert response2.status_code == status.HTTP_200_OK
        assert len(response2.data['results']) == 10

    def test_feed_visibility_filtering(self, authenticated_client, user):
        """Test that feed respects post visibility."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        # Create public and private posts
        public_post = create_test_post(organization=club, visibility='public')
        private_post = create_test_post(organization=club, visibility='private')

        url = reverse('organizations:feed-user')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        post_ids = [p['id'] for p in response.data['results']]

        # Public post should appear
        assert str(public_post.id) in post_ids
        # Private post should not appear (unless user is author)
        if user.id != private_post.author.id:
            assert str(private_post.id) not in post_ids


@pytest.mark.django_db
@pytest.mark.feed
class TestPostSharing:
    """Test post sharing functionality."""

    def test_share_post(self, authenticated_client, user):
        """Test sharing a post."""
        post = create_test_post()

        url = reverse('organizations:posts-share', kwargs={'pk': post.id})
        data = {'message': 'Check out this post!'}

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_unshare_post(self, authenticated_client, user):
        """Test unsharing a post."""
        post = create_test_post()

        # First share the post
        url_share = reverse('organizations:posts-share', kwargs={'pk': post.id})
        authenticated_client.post(url_share, {'message': 'Test'})

        # Then unshare
        url_unshare = reverse('organizations:posts-unshare', kwargs={'pk': post.id})

        response = authenticated_client.delete(url_unshare)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@pytest.mark.feed
class TestFeedItemTracking:
    """Test feed item read/unread tracking."""

    def test_mark_feed_item_as_read(self, authenticated_client, user):
        """Test marking feed item as read."""
        post = create_test_post()

        url = reverse('organizations:feed-mark-read', kwargs={'post_id': post.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_unread_count(self, authenticated_client, user):
        """Test getting unread feed items count."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        # Create posts
        for i in range(10):
            create_test_post(organization=club)

        url = reverse('organizations:feed-unread-count')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'unread_count' in response.data
        assert response.data['unread_count'] >= 0
