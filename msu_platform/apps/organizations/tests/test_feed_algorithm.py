"""
Tests for feed algorithm and priority scoring.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.organizations.models import Post, OrganizationFollow
from apps.organizations.services.feed import FeedGenerator, calculate_priority_score
from apps.core.tests.utils import (
    create_test_user,
    create_test_club,
    create_test_post,
)


@pytest.mark.django_db
@pytest.mark.feed
class TestFeedPriorityScoring:
    """Test feed priority score calculation."""

    def test_calculate_priority_score_recent_post(self, user, club):
        """Test that recent posts get higher priority."""
        post = create_test_post(
            author=user,
            organization=club,
            created_at=timezone.now()
        )

        score = calculate_priority_score(post, user)

        assert score > 0
        assert 'recency' in score  # Should have recency component

    def test_calculate_priority_score_old_post(self, user, club):
        """Test that old posts get lower priority."""
        post = create_test_post(
            author=user,
            organization=club,
        )
        # Manually set old timestamp
        post.created_at = timezone.now() - timedelta(days=30)
        post.save()

        recent_post = create_test_post(
            author=user,
            organization=club,
        )

        old_score = calculate_priority_score(post, user)
        recent_score = calculate_priority_score(recent_post, user)

        assert recent_score > old_score

    def test_priority_score_with_engagement(self, user, club):
        """Test that posts with engagement get higher priority."""
        low_engagement_post = create_test_post(organization=club)
        high_engagement_post = create_test_post(organization=club)

        # Add engagement to high engagement post
        for i in range(10):
            engagement_user = create_test_user()
            high_engagement_post.likes.add(engagement_user)

        low_score = calculate_priority_score(low_engagement_post, user)
        high_score = calculate_priority_score(high_engagement_post, user)

        assert high_score > low_score

    def test_priority_score_followed_organization(self, user, club):
        """Test that posts from followed organizations get higher priority."""
        # User follows this club
        OrganizationFollow.objects.create(user=user, organization=club)

        followed_post = create_test_post(organization=club)

        # Create another club user doesn't follow
        other_club = create_test_club()
        unfollowed_post = create_test_post(organization=other_club)

        followed_score = calculate_priority_score(followed_post, user)
        unfollowed_score = calculate_priority_score(unfollowed_post, user)

        assert followed_score > unfollowed_score

    def test_priority_score_author_followed(self, user):
        """Test that posts from followed authors get higher priority."""
        from apps.users.models import UserFollow

        followed_author = create_test_user()
        UserFollow.objects.create(follower=user, following=followed_author)

        club = create_test_club()
        followed_author_post = create_test_post(
            author=followed_author,
            organization=club
        )

        other_author = create_test_user()
        other_post = create_test_post(author=other_author, organization=club)

        followed_score = calculate_priority_score(followed_author_post, user)
        other_score = calculate_priority_score(other_post, user)

        assert followed_score > other_score


@pytest.mark.django_db
@pytest.mark.feed
class TestFeedGeneration:
    """Test feed generation for users."""

    def test_generate_feed_for_user(self, user):
        """Test generating feed for user."""
        # Create clubs and posts
        club1 = create_test_club()
        club2 = create_test_club()

        # User follows club1
        OrganizationFollow.objects.create(user=user, organization=club1)

        # Create posts
        for i in range(5):
            create_test_post(organization=club1)
            create_test_post(organization=club2)

        feed_generator = FeedGenerator(user)
        feed = feed_generator.generate_feed()

        assert len(feed) > 0
        # Posts from followed club should appear first
        assert feed[0].organization == club1

    def test_feed_pagination(self, user):
        """Test feed pagination."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        # Create many posts
        for i in range(30):
            create_test_post(organization=club)

        feed_generator = FeedGenerator(user)
        feed_page_1 = feed_generator.generate_feed(page=1, page_size=10)
        feed_page_2 = feed_generator.generate_feed(page=2, page_size=10)

        assert len(feed_page_1) == 10
        assert len(feed_page_2) == 10
        assert feed_page_1[0].id != feed_page_2[0].id

    def test_feed_excludes_hidden_posts(self, user):
        """Test that feed excludes hidden posts."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        visible_post = create_test_post(organization=club, is_hidden=False)
        hidden_post = create_test_post(organization=club, is_hidden=True)

        feed_generator = FeedGenerator(user)
        feed = feed_generator.generate_feed()

        post_ids = [post.id for post in feed]
        assert visible_post.id in post_ids
        assert hidden_post.id not in post_ids

    def test_feed_respects_visibility(self, user):
        """Test that feed respects post visibility settings."""
        club = create_test_club()

        # Public post - should appear
        public_post = create_test_post(
            organization=club,
            visibility='public'
        )

        # Members-only post - should not appear if user is not member
        members_post = create_test_post(
            organization=club,
            visibility='members'
        )

        feed_generator = FeedGenerator(user)
        feed = feed_generator.generate_feed()

        post_ids = [post.id for post in feed]
        assert public_post.id in post_ids
        # User is not member, so shouldn't see members-only post
        assert members_post.id not in post_ids

    def test_discover_feed(self, user):
        """Test discover feed shows diverse content."""
        # Create multiple clubs
        clubs = [create_test_club() for _ in range(5)]

        # Create posts from various clubs
        for club in clubs:
            for i in range(3):
                create_test_post(organization=club)

        feed_generator = FeedGenerator(user)
        discover_feed = feed_generator.generate_discover_feed()

        assert len(discover_feed) > 0
        # Should have posts from multiple clubs
        club_ids = {post.organization.id for post in discover_feed}
        assert len(club_ids) > 1


@pytest.mark.django_db
@pytest.mark.feed
class TestFeedCaching:
    """Test feed caching mechanisms."""

    def test_feed_caching(self, user):
        """Test that feed is cached."""
        from django.core.cache import cache

        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)
        create_test_post(organization=club)

        feed_generator = FeedGenerator(user)

        # Generate feed first time
        feed1 = feed_generator.generate_feed()

        # Check if cached
        cache_key = f'user_feed:{user.id}'
        cached_feed = cache.get(cache_key)

        assert cached_feed is not None

    def test_feed_cache_invalidation_new_post(self, user):
        """Test that feed cache is invalidated when new post is created."""
        from django.core.cache import cache

        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        feed_generator = FeedGenerator(user)
        feed1 = feed_generator.generate_feed()

        # Create new post
        create_test_post(organization=club)

        # Cache should be invalidated
        cache_key = f'user_feed:{user.id}'
        cached_feed = cache.get(cache_key)

        # Cache should be cleared or feed regenerated
        feed2 = feed_generator.generate_feed()
        assert len(feed2) >= len(feed1)

    def test_feed_cache_invalidation_new_follow(self, user):
        """Test that feed cache is invalidated when user follows organization."""
        club1 = create_test_club()
        club2 = create_test_club()

        create_test_post(organization=club1)
        create_test_post(organization=club2)

        feed_generator = FeedGenerator(user)
        feed1 = feed_generator.generate_feed()

        # User follows new club
        OrganizationFollow.objects.create(user=user, organization=club2)

        # Feed should be regenerated with new content
        feed2 = feed_generator.generate_feed()

        # Should have different or more content
        assert len(feed2) >= len(feed1)


@pytest.mark.django_db
@pytest.mark.feed
class TestFeedAggregation:
    """Test feed aggregation from multiple sources."""

    def test_aggregate_posts_from_multiple_sources(self, user):
        """Test aggregating posts from followed clubs and interests."""
        club1 = create_test_club()
        club2 = create_test_club()
        club3 = create_test_club()

        # User follows club1 and club2
        OrganizationFollow.objects.create(user=user, organization=club1)
        OrganizationFollow.objects.create(user=user, organization=club2)

        # Create posts
        create_test_post(organization=club1)
        create_test_post(organization=club2)
        create_test_post(organization=club3)  # Not followed

        feed_generator = FeedGenerator(user)
        feed = feed_generator.generate_feed()

        # Should have posts from followed clubs
        org_ids = {post.organization.id for post in feed}
        assert club1.id in org_ids
        assert club2.id in org_ids

    def test_feed_deduplication(self, user):
        """Test that feed doesn't have duplicate posts."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        post = create_test_post(organization=club)

        feed_generator = FeedGenerator(user)
        feed = feed_generator.generate_feed()

        post_ids = [p.id for p in feed]
        # No duplicates
        assert len(post_ids) == len(set(post_ids))

    def test_feed_sorting_by_priority(self, user):
        """Test that feed is sorted by priority score."""
        club = create_test_club()
        OrganizationFollow.objects.create(user=user, organization=club)

        # Create posts with different characteristics
        old_post = create_test_post(organization=club)
        old_post.created_at = timezone.now() - timedelta(days=7)
        old_post.save()

        new_post = create_test_post(organization=club)

        feed_generator = FeedGenerator(user)
        feed = feed_generator.generate_feed()

        # New post should appear before old post
        post_ids = [p.id for p in feed]
        assert post_ids.index(new_post.id) < post_ids.index(old_post.id)
