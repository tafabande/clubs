"""
Query optimization utilities for organizations app.

Provides optimized querysets with proper select_related and prefetch_related.
"""
from django.db.models import Prefetch, Count, Q, F
from django.contrib.contenttypes.models import ContentType


class PostQueryOptimizer:
    """Optimize Post queries."""

    @staticmethod
    def get_optimized_queryset(queryset=None):
        """
        Get optimized queryset for posts with related data.

        Includes:
        - Author information
        - Engagement counts
        - Media files
        """
        from apps.organizations.models import Post, PostMedia

        if queryset is None:
            from apps.organizations.models import Post
            queryset = Post.objects.all()

        return queryset.select_related(
            'author',
            'content_type'
        ).prefetch_related(
            Prefetch(
                'media',
                queryset=PostMedia.objects.order_by('order')
            ),
            'likes',
            'comments'
        ).annotate(
            total_likes=Count('likes', distinct=True),
            total_comments=Count('comments', distinct=True),
            total_shares=Count('shares', distinct=True)
        )

    @staticmethod
    def get_feed_posts(user, limit=20):
        """
        Get optimized feed posts for a user.

        Args:
            user: User object
            limit: Number of posts to return

        Returns:
            Optimized queryset of posts
        """
        from apps.organizations.models import Post

        queryset = Post.objects.filter(
            is_active=True,
            visibility='public'
        ).select_related(
            'author',
            'content_type'
        ).prefetch_related(
            'media',
            'likes',
        ).annotate(
            user_liked=Count(
                'likes',
                filter=Q(likes__user=user),
                distinct=True
            )
        ).order_by('-is_pinned', '-created_at')[:limit]

        return queryset

    @staticmethod
    def get_organization_posts(content_type, object_id, limit=20):
        """
        Get optimized posts for an organization.

        Args:
            content_type: ContentType of organization
            object_id: ID of organization
            limit: Number of posts to return

        Returns:
            Optimized queryset of posts
        """
        from apps.organizations.models import Post

        return Post.objects.filter(
            content_type=content_type,
            object_id=object_id,
            is_active=True
        ).select_related(
            'author'
        ).prefetch_related(
            'media'
        ).annotate(
            total_likes=Count('likes', distinct=True),
            total_comments=Count('comments', distinct=True)
        ).order_by('-is_pinned', '-created_at')[:limit]


class FeedQueryOptimizer:
    """Optimize Feed queries."""

    @staticmethod
    def get_user_feed(user, limit=20, offset=0):
        """
        Get optimized user feed.

        Args:
            user: User object
            limit: Number of feed items
            offset: Pagination offset

        Returns:
            Optimized queryset of feed items with posts
        """
        from apps.organizations.models import Feed

        return Feed.objects.filter(
            user=user
        ).select_related(
            'post__author',
            'post__content_type'
        ).prefetch_related(
            'post__media',
            'post__likes',
            'post__comments'
        ).annotate(
            user_liked=Count(
                'post__likes',
                filter=Q(post__likes__user=user),
                distinct=True
            )
        ).order_by('-relevance_score', '-created_at')[offset:offset + limit]


class OrganizationQueryOptimizer:
    """Optimize Organization queries."""

    @staticmethod
    def get_clubs_with_counts():
        """Get clubs with member and follower counts."""
        from apps.organizations.models import Club

        return Club.objects.filter(
            is_active=True,
            is_approved=True
        ).select_related(
            'created_by'
        ).annotate(
            member_count=Count('memberships', filter=Q(memberships__status='active'), distinct=True),
            post_count=Count('posts', filter=Q(posts__is_active=True), distinct=True)
        ).order_by('-member_count', 'name')

    @staticmethod
    def get_churches_with_counts():
        """Get churches with member counts."""
        from apps.organizations.models import Church

        return Church.objects.filter(
            is_active=True,
            is_approved=True
        ).select_related(
            'created_by'
        ).annotate(
            member_count=Count('memberships', filter=Q(memberships__status='active'), distinct=True),
            post_count=Count('posts', filter=Q(posts__is_active=True), distinct=True)
        ).order_by('-member_count', 'name')

    @staticmethod
    def get_sports_teams_with_counts():
        """Get sports teams with member counts."""
        from apps.organizations.models import SportsTeam

        return SportsTeam.objects.filter(
            is_active=True,
            is_approved=True
        ).select_related(
            'created_by'
        ).annotate(
            member_count=Count('memberships', filter=Q(memberships__status='active'), distinct=True),
            post_count=Count('posts', filter=Q(posts__is_active=True), distinct=True)
        ).order_by('-member_count', 'name')

    @staticmethod
    def get_activities_with_counts():
        """Get activities with registration counts."""
        from apps.organizations.models import Activity

        return Activity.objects.filter(
            is_active=True,
            is_approved=True
        ).select_related(
            'created_by'
        ).annotate(
            registration_count=Count(
                'registrations',
                filter=Q(registrations__status='registered'),
                distinct=True
            ),
            post_count=Count('posts', filter=Q(posts__is_active=True), distinct=True)
        ).order_by('start_date', 'name')

    @staticmethod
    def get_club_with_members(club_id):
        """Get club with optimized member data."""
        from apps.organizations.models import Club

        return Club.objects.filter(
            id=club_id
        ).select_related(
            'created_by',
            'faculty_advisor'
        ).prefetch_related(
            Prefetch(
                'memberships',
                queryset=Club.objects.none().__class__.objects.filter(
                    status='active'
                ).select_related('user').order_by('-joined_at')
            )
        ).first()


class SearchQueryOptimizer:
    """Optimize search queries."""

    @staticmethod
    def search_organizations(query, org_type=None, limit=20):
        """
        Optimized organization search.

        Args:
            query: Search query string
            org_type: Filter by organization type
            limit: Maximum results

        Returns:
            Optimized search results
        """
        from apps.organizations.models import SearchIndex

        queryset = SearchIndex.objects.filter(
            is_active=True,
            is_approved=True
        )

        if org_type:
            queryset = queryset.filter(organization_type=org_type)

        # Use full-text search
        results = SearchIndex.search(query, org_type, limit=limit)

        return results


class MembershipQueryOptimizer:
    """Optimize membership queries."""

    @staticmethod
    def get_user_memberships(user):
        """
        Get all memberships for a user across all organization types.

        Args:
            user: User object

        Returns:
            Dictionary with membership data by type
        """
        from apps.organizations.models import (
            ClubMembership, ChurchMembership,
            SportsTeamMembership, ActivityRegistration
        )

        return {
            'clubs': ClubMembership.objects.filter(
                user=user,
                status='active'
            ).select_related(
                'club'
            ).annotate(
                member_count=Count('club__memberships', filter=Q(club__memberships__status='active'))
            ),
            'churches': ChurchMembership.objects.filter(
                user=user,
                status='active'
            ).select_related(
                'church'
            ).annotate(
                member_count=Count('church__memberships', filter=Q(church__memberships__status='active'))
            ),
            'sports_teams': SportsTeamMembership.objects.filter(
                user=user,
                status='active'
            ).select_related(
                'sports_team'
            ).annotate(
                member_count=Count('sports_team__memberships', filter=Q(sports_team__memberships__status='active'))
            ),
            'activities': ActivityRegistration.objects.filter(
                user=user,
                status='registered'
            ).select_related(
                'activity'
            ).annotate(
                registration_count=Count('activity__registrations', filter=Q(activity__registrations__status='registered'))
            )
        }

    @staticmethod
    def get_organization_members(content_type_id, object_id, status='active'):
        """
        Get members for any organization type.

        Args:
            content_type_id: ContentType ID
            object_id: Organization ID
            status: Membership status filter

        Returns:
            Optimized queryset of memberships
        """
        from apps.organizations.models import Club, Church, SportsTeam

        content_type = ContentType.objects.get_for_id(content_type_id)
        model_class = content_type.model_class()

        if model_class == Club:
            from apps.organizations.models import ClubMembership
            return ClubMembership.objects.filter(
                club_id=object_id,
                status=status
            ).select_related('user').order_by('-joined_at')
        elif model_class == Church:
            from apps.organizations.models import ChurchMembership
            return ChurchMembership.objects.filter(
                church_id=object_id,
                status=status
            ).select_related('user').order_by('-joined_at')
        elif model_class == SportsTeam:
            from apps.organizations.models import SportsTeamMembership
            return SportsTeamMembership.objects.filter(
                sports_team_id=object_id,
                status=status
            ).select_related('user').order_by('-joined_at')

        return None


class CommentQueryOptimizer:
    """Optimize comment queries."""

    @staticmethod
    def get_post_comments(post_id, limit=50):
        """
        Get optimized comments for a post with nested replies.

        Args:
            post_id: Post ID
            limit: Maximum comments to return

        Returns:
            Optimized queryset of comments
        """
        from apps.organizations.models import PostComment

        # Get top-level comments with replies prefetched
        return PostComment.objects.filter(
            post_id=post_id,
            parent__isnull=True,
            is_active=True
        ).select_related(
            'user'
        ).prefetch_related(
            Prefetch(
                'replies',
                queryset=PostComment.objects.filter(
                    is_active=True
                ).select_related('user').order_by('created_at')
            )
        ).order_by('-created_at')[:limit]


# Utility functions for common query patterns

def get_user_following_organizations(user):
    """
    Get all organizations a user is following.

    Args:
        user: User object

    Returns:
        Queryset of UserFollowOrganization with organization data
    """
    from apps.organizations.models import UserFollowOrganization

    return UserFollowOrganization.objects.filter(
        user=user
    ).select_related(
        'content_type'
    ).order_by('-created_at')


def get_organization_followers_count(content_type, object_id):
    """
    Get follower count for an organization.

    Args:
        content_type: ContentType of organization
        object_id: Organization ID

    Returns:
        Integer count of followers
    """
    from apps.organizations.models import UserFollowOrganization

    return UserFollowOrganization.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).count()


def check_user_follows_organization(user, content_type, object_id):
    """
    Check if user follows an organization.

    Args:
        user: User object
        content_type: ContentType of organization
        object_id: Organization ID

    Returns:
        Boolean
    """
    from apps.organizations.models import UserFollowOrganization

    return UserFollowOrganization.objects.filter(
        user=user,
        content_type=content_type,
        object_id=object_id
    ).exists()
