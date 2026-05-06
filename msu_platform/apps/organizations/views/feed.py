"""
ViewSets for social feed functionality.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from apps.organizations.models import (
    Post, PostMedia, PostLike, PostComment, PostShare, Feed,
    Club, Church, SportsTeam, Activity
)
from apps.organizations.serializers.feed import (
    PostSerializer, CreatePostSerializer, PostCommentSerializer, FeedSerializer
)
from apps.core.cache_utils import (
    CacheKey, get_or_set_cache, CACHE_TIMEOUT_5_MIN,
    CACHE_TIMEOUT_1_MIN, CACHE_TIMEOUT_10_MIN
)
from apps.organizations.query_optimizers import PostQueryOptimizer, FeedQueryOptimizer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing organization posts.

    Endpoints:
    - GET /posts/ - List all posts (filtered by permissions)
    - POST /posts/ - Create a new post
    - GET /posts/{id}/ - Retrieve a specific post
    - PUT /posts/{id}/ - Update a post
    - DELETE /posts/{id}/ - Delete a post
    - POST /posts/{id}/like/ - Like/unlike a post
    - POST /posts/{id}/comment/ - Add a comment
    - GET /posts/{id}/comments/ - List comments
    - POST /posts/{id}/share/ - Share a post
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get posts based on user permissions with optimization."""
        user = self.request.user

        print(f"[DEBUG] User: {user}")
        
        # Use optimized queryset from query optimizer
        queryset = PostQueryOptimizer.get_optimized_queryset(
            Post.objects.filter(is_active=True)
        )

        # Filter by visibility
        if user.is_staff:
            # Staff can see all posts
            return queryset

        # Regular users see:
        # 1. Public posts
        # 2. Posts from organizations they're members of (members_only)
        # 3. Posts they authored (private)

        # Get user's organizations
        user_clubs = Club.objects.filter(
            clubmembership__user=user
        ).values_list('id', flat=True)

        user_churches = Church.objects.filter(
            churchmembership__user=user
        ).values_list('id', flat=True)

        user_teams = SportsTeam.objects.filter(
            sportsteammembership__user=user
        ).values_list('id', flat=True)

        user_activities = Activity.objects.filter(
            activityregistration__user=user
        ).values_list('id', flat=True)

        all_org_ids = list(user_clubs) + list(user_churches) + list(user_teams) + list(user_activities)
        print(f"[DEBUG] all_org_ids: {all_org_ids}")

        queryset = queryset.filter(
            Q(visibility='public') |
            Q(visibility='members_only', object_id__in=all_org_ids) |
            Q(author=user)
        )

        return queryset.order_by('-is_pinned', '-created_at')

    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action == 'create':
            return CreatePostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """Set the author when creating a post."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Like or unlike a post.

        Returns:
            - status: 'liked' or 'unliked'
            - likes_count: Updated likes count
        """
        post = self.get_object()

        like, created = PostLike.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            # Unlike - remove the like
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save(update_fields=['likes_count'])

            return Response({
                'status': 'unliked',
                'likes_count': post.likes_count
            })
        else:
            # Like - increment count
            post.likes_count += 1
            post.save(update_fields=['likes_count'])

            return Response({
                'status': 'liked',
                'likes_count': post.likes_count
            })

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """
        Add a comment to a post.

        Body:
            - content: Comment text (required)
            - parent: Parent comment ID for replies (optional)
        """
        post = self.get_object()

        serializer = PostCommentSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            comment = serializer.save(
                post=post,
                user=request.user
            )

            # Increment comments count
            post.comments_count += 1
            post.save(update_fields=['comments_count'])

            return Response(
                PostCommentSerializer(comment, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        List all comments for a post.

        Query params:
            - limit: Number of comments to return (default: 20)
            - offset: Pagination offset (default: 0)
        """
        post = self.get_object()

        # Get top-level comments only
        comments = post.comments.filter(
            is_active=True,
            parent__isnull=True
        ).order_by('-created_at')

        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))

        comments = comments[offset:offset + limit]

        serializer = PostCommentSerializer(
            comments,
            many=True,
            context={'request': request}
        )

        return Response({
            'count': post.comments_count,
            'results': serializer.data
        })

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """
        Share a post.

        Body:
            - comment: Optional comment when sharing (optional)
        """
        post = self.get_object()

        # Check if already shared
        existing_share = PostShare.objects.filter(
            post=post,
            user=request.user
        ).first()

        if existing_share:
            return Response(
                {'detail': 'You have already shared this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create share
        share = PostShare.objects.create(
            post=post,
            user=request.user,
            comment=request.data.get('comment', '')
        )

        # Increment shares count
        post.shares_count += 1
        post.save(update_fields=['shares_count'])

        return Response({
            'status': 'shared',
            'shares_count': post.shares_count,
            'share_id': share.id
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unshare(self, request, pk=None):
        """Remove a share."""
        post = self.get_object()

        try:
            share = PostShare.objects.get(post=post, user=request.user)
            share.delete()

            # Decrement shares count
            post.shares_count = max(0, post.shares_count - 1)
            post.save(update_fields=['shares_count'])

            return Response({
                'status': 'unshared',
                'shares_count': post.shares_count
            })
        except PostShare.DoesNotExist:
            return Response(
                {'detail': 'You have not shared this post.'},
                status=status.HTTP_404_NOT_FOUND
            )


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for personalized user feeds.

    Endpoints:
    - GET /feed/ - Get user's personalized feed
    - POST /feed/generate/ - Generate/refresh feed
    - POST /feed/{id}/mark_read/ - Mark a feed item as read
    """

    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get feed items for current user with optimization."""
        user = self.request.user

        # Use optimized queryset from query optimizer
        return FeedQueryOptimizer.get_user_feed(
            user,
            limit=100,  # Pre-fetch more items for pagination
            offset=0
        )

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Generate personalized feed for user.

        This creates feed entries based on:
        1. User's organization memberships
        2. Recent posts from those organizations
        3. Relevance scoring
        """
        user = request.user

        # Get user's organizations
        user_clubs = Club.objects.filter(clubmembership__user=user)
        user_churches = Church.objects.filter(churchmembership__user=user)
        user_teams = SportsTeam.objects.filter(sportsteammembership__user=user)
        user_activities = Activity.objects.filter(activityregistration__user=user)

        # Get content types
        club_ct = ContentType.objects.get_for_model(Club)
        church_ct = ContentType.objects.get_for_model(Church)
        team_ct = ContentType.objects.get_for_model(SportsTeam)
        activity_ct = ContentType.objects.get_for_model(Activity)

        # Build Q objects for posts from user's organizations
        post_filters = Q()

        for club in user_clubs:
            post_filters |= Q(content_type=club_ct, object_id=club.id)

        for church in user_churches:
            post_filters |= Q(content_type=church_ct, object_id=church.id)

        for team in user_teams:
            post_filters |= Q(content_type=team_ct, object_id=team.id)

        for activity in user_activities:
            post_filters |= Q(content_type=activity_ct, object_id=activity.id)

        # Get recent posts (last 30 days)
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)

        recent_posts = Post.objects.filter(
            post_filters,
            is_active=True,
            created_at__gte=thirty_days_ago
        ).exclude(
            # Exclude posts already in user's feed
            id__in=Feed.objects.filter(user=user).values_list('post_id', flat=True)
        )

        # Create feed entries with relevance scoring
        feed_entries = []
        for post in recent_posts:
            # Simple relevance scoring
            relevance = 0.0

            # Boost pinned posts
            if post.is_pinned:
                relevance += 10.0

            # Boost posts with high engagement
            relevance += (post.likes_count * 0.1)
            relevance += (post.comments_count * 0.2)
            relevance += (post.shares_count * 0.3)

            # Boost recent posts
            days_old = (timezone.now() - post.created_at).days
            relevance += max(0, 5.0 - days_old * 0.5)

            feed_entries.append(
                Feed(
                    user=user,
                    post=post,
                    relevance_score=relevance
                )
            )

        # Bulk create feed entries
        created_count = len(feed_entries)
        if feed_entries:
            Feed.objects.bulk_create(feed_entries, ignore_conflicts=True)

        return Response({
            'status': 'generated',
            'new_items': created_count
        })

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a feed item as read."""
        feed_item = self.get_object()

        if not feed_item.is_read:
            feed_item.is_read = True
            feed_item.read_at = timezone.now()
            feed_item.save(update_fields=['is_read', 'read_at'])

        return Response({
            'status': 'marked_read',
            'read_at': feed_item.read_at
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread feed items with caching."""
        user = request.user
        cache_key = CacheKey.feed_unread_count(str(user.id))

        # Try to get from cache
        count = cache.get(cache_key)

        if count is None:
            # Cache miss - calculate count
            count = Feed.objects.filter(
                user=user,
                is_read=False
            ).count()

            # Cache for 1 minute
            cache.set(cache_key, count, CACHE_TIMEOUT_1_MIN)

        return Response({
            'unread_count': count
        })
