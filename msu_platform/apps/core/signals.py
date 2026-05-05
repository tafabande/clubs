"""
Signal handlers for cache invalidation.

Automatically invalidates cache when data changes.
"""
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from apps.core.cache_utils import (
    invalidate_user_cache,
    invalidate_organization_cache,
    invalidate_post_cache,
    invalidate_cache_pattern,
    CacheKey
)


# User-related signals

@receiver(post_save, sender='users.User')
def invalidate_user_cache_on_save(sender, instance, **kwargs):
    """Invalidate user cache when user is updated."""
    invalidate_user_cache(str(instance.id))


@receiver(post_save, sender='users.UserFollow')
def invalidate_follow_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when user follows/unfollows another user."""
    # Invalidate follower's cache
    invalidate_user_cache(str(instance.follower.id))

    # Invalidate following user's cache
    invalidate_user_cache(str(instance.following.id))

    # Invalidate feed cache for follower (they'll see new posts)
    invalidate_cache_pattern(f"feed:user:{instance.follower.id}:*")


@receiver(post_delete, sender='users.UserFollow')
def invalidate_follow_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when user unfollow relationship is deleted."""
    invalidate_user_cache(str(instance.follower.id))
    invalidate_user_cache(str(instance.following.id))
    invalidate_cache_pattern(f"feed:user:{instance.follower.id}:*")


# Post-related signals

@receiver(post_save, sender='organizations.Post')
def invalidate_post_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when post is created or updated."""
    # Invalidate post cache
    invalidate_post_cache(str(instance.id))

    # Invalidate organization feed cache
    if instance.content_type and instance.object_id:
        org_type = instance.content_type.model
        invalidate_cache_pattern(f"feed:org:{org_type}:{instance.object_id}:*")

    # Invalidate discover feed
    invalidate_cache_pattern("feed:discover:*")

    # If post is created, invalidate all follower feeds
    if created:
        # This is handled by Celery task in production
        pass


@receiver(post_delete, sender='organizations.Post')
def invalidate_post_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when post is deleted."""
    invalidate_post_cache(str(instance.id))

    if instance.content_type and instance.object_id:
        org_type = instance.content_type.model
        invalidate_cache_pattern(f"feed:org:{org_type}:{instance.object_id}:*")

    invalidate_cache_pattern("feed:discover:*")


@receiver(post_save, sender='organizations.PostLike')
def invalidate_like_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when post is liked."""
    if created:
        invalidate_post_cache(str(instance.post.id))
        # Update engagement counts in cache
        from django.core.cache import cache
        cache.delete(CacheKey.post_likes_count(str(instance.post.id)))


@receiver(post_delete, sender='organizations.PostLike')
def invalidate_like_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when like is removed."""
    invalidate_post_cache(str(instance.post.id))
    from django.core.cache import cache
    cache.delete(CacheKey.post_likes_count(str(instance.post.id)))


@receiver(post_save, sender='organizations.PostComment')
def invalidate_comment_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when comment is created."""
    if created:
        invalidate_post_cache(str(instance.post.id))
        from django.core.cache import cache
        cache.delete(CacheKey.post_comments_count(str(instance.post.id)))


@receiver(post_delete, sender='organizations.PostComment')
def invalidate_comment_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when comment is deleted."""
    invalidate_post_cache(str(instance.post.id))
    from django.core.cache import cache
    cache.delete(CacheKey.post_comments_count(str(instance.post.id)))


@receiver(post_save, sender='organizations.PostShare')
def invalidate_share_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when post is shared."""
    if created:
        invalidate_post_cache(str(instance.post.id))


# Organization-related signals

@receiver(post_save, sender='organizations.Club')
def invalidate_club_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when club is updated."""
    invalidate_organization_cache('club', str(instance.id))
    invalidate_cache_pattern("org:list:club:*")

    # Invalidate search cache
    invalidate_cache_pattern("search:*")


@receiver(post_delete, sender='organizations.Club')
def invalidate_club_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when club is deleted."""
    invalidate_organization_cache('club', str(instance.id))
    invalidate_cache_pattern("org:list:club:*")
    invalidate_cache_pattern("search:*")


@receiver(post_save, sender='organizations.Church')
def invalidate_church_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when church is updated."""
    invalidate_organization_cache('church', str(instance.id))
    invalidate_cache_pattern("org:list:church:*")
    invalidate_cache_pattern("search:*")


@receiver(post_delete, sender='organizations.Church')
def invalidate_church_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when church is deleted."""
    invalidate_organization_cache('church', str(instance.id))
    invalidate_cache_pattern("org:list:church:*")
    invalidate_cache_pattern("search:*")


@receiver(post_save, sender='organizations.SportsTeam')
def invalidate_sports_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when sports team is updated."""
    invalidate_organization_cache('sports_team', str(instance.id))
    invalidate_cache_pattern("org:list:sports_team:*")
    invalidate_cache_pattern("search:*")


@receiver(post_delete, sender='organizations.SportsTeam')
def invalidate_sports_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when sports team is deleted."""
    invalidate_organization_cache('sports_team', str(instance.id))
    invalidate_cache_pattern("org:list:sports_team:*")
    invalidate_cache_pattern("search:*")


@receiver(post_save, sender='organizations.Activity')
def invalidate_activity_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when activity is updated."""
    invalidate_organization_cache('activity', str(instance.id))
    invalidate_cache_pattern("org:list:activity:*")
    invalidate_cache_pattern("search:*")


@receiver(post_delete, sender='organizations.Activity')
def invalidate_activity_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when activity is deleted."""
    invalidate_organization_cache('activity', str(instance.id))
    invalidate_cache_pattern("org:list:activity:*")
    invalidate_cache_pattern("search:*")


# Membership-related signals

@receiver(post_save, sender='organizations.ClubMembership')
def invalidate_club_membership_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when club membership changes."""
    invalidate_organization_cache('club', str(instance.club.id))
    invalidate_user_cache(str(instance.user.id))


@receiver(post_delete, sender='organizations.ClubMembership')
def invalidate_club_membership_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when club membership is deleted."""
    invalidate_organization_cache('club', str(instance.club.id))
    invalidate_user_cache(str(instance.user.id))


@receiver(post_save, sender='organizations.ChurchMembership')
def invalidate_church_membership_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when church membership changes."""
    invalidate_organization_cache('church', str(instance.church.id))
    invalidate_user_cache(str(instance.user.id))


@receiver(post_delete, sender='organizations.ChurchMembership')
def invalidate_church_membership_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when church membership is deleted."""
    invalidate_organization_cache('church', str(instance.church.id))
    invalidate_user_cache(str(instance.user.id))


@receiver(post_save, sender='organizations.SportsTeamMembership')
def invalidate_sports_membership_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when sports team membership changes."""
    invalidate_organization_cache('sports_team', str(instance.sports_team.id))
    invalidate_user_cache(str(instance.user.id))


@receiver(post_delete, sender='organizations.SportsTeamMembership')
def invalidate_sports_membership_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when sports team membership is deleted."""
    invalidate_organization_cache('sports_team', str(instance.sports_team.id))
    invalidate_user_cache(str(instance.user.id))


# Follow organization signals

@receiver(post_save, sender='organizations.UserFollowOrganization')
def invalidate_follow_org_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when user follows an organization."""
    if instance.content_type and instance.object_id:
        org_type = instance.content_type.model
        invalidate_organization_cache(org_type, str(instance.object_id))

    invalidate_user_cache(str(instance.user.id))

    # Invalidate user's feed since they'll see new posts
    if created:
        invalidate_cache_pattern(f"feed:user:{instance.user.id}:*")


@receiver(post_delete, sender='organizations.UserFollowOrganization')
def invalidate_follow_org_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when user unfollows an organization."""
    if instance.content_type and instance.object_id:
        org_type = instance.content_type.model
        invalidate_organization_cache(org_type, str(instance.object_id))

    invalidate_user_cache(str(instance.user.id))
    invalidate_cache_pattern(f"feed:user:{instance.user.id}:*")


# Search index signals

@receiver(post_save, sender='organizations.SearchIndex')
def invalidate_search_cache_on_save(sender, instance, **kwargs):
    """Invalidate search cache when search index is updated."""
    invalidate_cache_pattern("search:*")


@receiver(post_delete, sender='organizations.SearchIndex')
def invalidate_search_cache_on_delete(sender, instance, **kwargs):
    """Invalidate search cache when search index entry is deleted."""
    invalidate_cache_pattern("search:*")
