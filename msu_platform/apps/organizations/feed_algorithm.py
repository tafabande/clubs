"""
Feed ranking algorithm for MSU Platform.

Implements priority scoring based on:
- Engagement (likes, comments, shares)
- Recency (post age)
- Relationship (following, membership, interest)
- Post type and visibility
"""
from django.utils import timezone
from datetime import timedelta
import math
import logging

logger = logging.getLogger(__name__)


def calculate_engagement_score(post) -> float:
    """
    Calculate engagement score based on post interactions.

    Formula: (likes * 1) + (comments * 3) + (shares * 5)
    Normalized to 0-100 scale.

    Args:
        post: Post instance

    Returns:
        float: Engagement score (0-100)
    """
    likes_weight = 1.0
    comments_weight = 3.0
    shares_weight = 5.0

    raw_score = (
        (post.likes_count * likes_weight) +
        (post.comments_count * comments_weight) +
        (post.shares_count * shares_weight)
    )

    # Normalize using logarithmic scale for better distribution
    if raw_score > 0:
        normalized = min(math.log10(raw_score + 1) * 20, 100)
    else:
        normalized = 0

    return round(normalized, 2)


def calculate_recency_score(post) -> float:
    """
    Calculate recency score based on post age.

    Newer posts get higher scores with exponential decay.

    Args:
        post: Post instance

    Returns:
        float: Recency score (0-100)
    """
    now = timezone.now()
    age = (now - post.created_at).total_seconds()

    # Time decay parameters
    half_life_hours = 24  # Score halves every 24 hours
    half_life_seconds = half_life_hours * 3600

    # Exponential decay formula
    decay_factor = math.exp(-age / half_life_seconds)
    score = decay_factor * 100

    # Bonus for very recent posts (< 1 hour)
    if age < 3600:
        score = min(score * 1.2, 100)

    return round(score, 2)


def calculate_relationship_score(user, post) -> float:
    """
    Calculate relationship score based on user's connection to organization.

    Scoring:
    - Member: 100 points
    - Following: 80 points
    - Interested: 60 points
    - Author connection: +20 points
    - None: 20 points (discovery)

    Args:
        user: User instance
        post: Post instance

    Returns:
        float: Relationship score (0-100)
    """
    from django.contrib.contenttypes.models import ContentType
    from apps.organizations.models import (
        UserFollowOrganization,
        UserInterestOrganization,
        ClubMembership,
        ChurchMembership,
        SportsTeamMembership,
        ActivityRegistration
    )

    score = 20.0  # Base score for discovery

    # Get organization
    organization = post.organization
    if not organization:
        return score

    content_type = post.content_type
    org_id = post.object_id

    # Check membership (highest priority)
    is_member = False
    if content_type.model == 'club':
        is_member = ClubMembership.objects.filter(user=user, club_id=org_id, status='active').exists()
    elif content_type.model == 'church':
        is_member = ChurchMembership.objects.filter(user=user, church_id=org_id, status='active').exists()
    elif content_type.model == 'sportsteam':
        is_member = SportsTeamMembership.objects.filter(user=user, team_id=org_id, status='active').exists()
    elif content_type.model == 'activity':
        is_member = ActivityRegistration.objects.filter(user=user, activity_id=org_id, status='registered').exists()

    if is_member:
        score = 100.0
    else:
        # Check following
        is_following = UserFollowOrganization.objects.filter(
            user=user,
            content_type=content_type,
            object_id=org_id
        ).exists()

        if is_following:
            score = 80.0
        else:
            # Check interest
            has_interest = UserInterestOrganization.objects.filter(
                user=user,
                content_type=content_type,
                object_id=org_id
            ).exists()

            if has_interest:
                score = 60.0

    # Bonus if user follows the post author
    from apps.users.models import UserFollow
    if UserFollow.objects.filter(follower=user, following=post.author).exists():
        score = min(score + 15, 100)

    # Interest matching (Tag-based)
    if user.interests and organization.categories:
        user_tags = set(tag.strip().lower() for tag in user.interests.split(',') if tag.strip())
        org_tags = set(tag.strip().lower() for tag in organization.categories.split(',') if tag.strip())
        
        matches = user_tags.intersection(org_tags)
        if matches:
            # Bonus of 5 points per match, up to 20
            interest_bonus = min(len(matches) * 5, 20)
            score = min(score + interest_bonus, 100)

    return round(score, 2)


def calculate_post_type_bonus(post) -> float:
    """
    Calculate bonus based on post type.

    Important post types get higher priority.

    Args:
        post: Post instance

    Returns:
        float: Type bonus (0-20)
    """
    type_bonuses = {
        'announcement': 20,
        'event': 18,
        'recruitment': 15,
        'achievement': 10,
        'general': 5,
        'media': 3,
    }

    bonus = type_bonuses.get(post.post_type, 5)

    # Extra bonus for pinned posts
    if post.is_pinned:
        bonus += 10

    return round(bonus, 2)


def calculate_relevance_score(user, post) -> dict:
    """
    Calculate comprehensive relevance score for a post.

    Combines multiple factors:
    - Engagement (30% weight)
    - Recency (25% weight)
    - Relationship (35% weight)
    - Type bonus (10% weight)

    Args:
        user: User instance
        post: Post instance

    Returns:
        dict: Score breakdown and total
    """
    engagement_score = calculate_engagement_score(post)
    recency_score = calculate_recency_score(post)
    relationship_score = calculate_relationship_score(user, post)
    type_bonus = calculate_post_type_bonus(post)

    # Weighted combination
    total_score = (
        (engagement_score * 0.30) +
        (recency_score * 0.25) +
        (relationship_score * 0.35) +
        (type_bonus * 0.10)
    )

    # Cap at 100
    total_score = min(total_score, 100)

    return {
        'total': round(total_score, 2),
        'engagement': engagement_score,
        'recency': recency_score,
        'relationship': relationship_score,
        'type_bonus': type_bonus,
    }


def should_include_in_feed(user, post) -> tuple:
    """
    Determine if a post should be included in user's feed.

    Checks:
    - Visibility rules
    - User permissions
    - Organization membership/following

    Args:
        user: User instance
        post: Post instance

    Returns:
        tuple: (should_include: bool, reason: str)
    """
    # Check if post is active
    if not post.is_active:
        return False, 'Post is not active'

    # Check visibility
    if post.visibility == 'admin_only':
        # Only admins can see
        # Add admin check here
        return False, 'Admin only visibility'

    elif post.visibility == 'members_only':
        # Only members can see
        relationship_score = calculate_relationship_score(user, post)
        if relationship_score < 80:  # Not a member or follower
            return False, 'Members only visibility'

    elif post.visibility == 'followers_only':
        # Only followers can see
        relationship_score = calculate_relationship_score(user, post)
        if relationship_score < 60:  # Not following or interested
            return False, 'Followers only visibility'

    # Public posts are visible to everyone
    return True, 'Visible'


def get_source_type(user, post) -> str:
    """
    Determine how this post reached the user.

    Args:
        user: User instance
        post: Post instance

    Returns:
        str: Source type (following, member, interest, recommended, trending)
    """
    relationship_score = calculate_relationship_score(user, post)

    if relationship_score >= 90:
        return 'member'
    elif relationship_score >= 70:
        return 'following'
    elif relationship_score >= 50:
        return 'interest'
    elif calculate_engagement_score(post) > 70:
        return 'trending'
    else:
        return 'recommended'
