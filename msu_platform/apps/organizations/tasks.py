"""
Celery tasks for feed generation and management.
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from apps.organizations.models import Post, Feed, UserFollowOrganization
from apps.organizations.models.club import ClubMembership
from apps.organizations.models.church import ChurchMembership
from apps.organizations.models.sports import SportsTeamMembership
from apps.organizations.models.activity import ActivityMembership
from django.db.models import F
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


@shared_task
def update_organization_counts(content_type_id: int, object_id: str):
    """
    Update counts for an organization.
    """
    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
        model_class = content_type.model_class()
        org = model_class.objects.get(id=object_id)
        
        # Calculate counts
        org.followers_count = UserFollowOrganization.objects.filter(
            content_type=content_type, 
            object_id=object_id
        ).count()
        
        # This is a bit tricky since memberships are in different models
        # We'll need a way to sum them or check the specific model
        if hasattr(org, 'memberships'):
            org.members_count = org.memberships.filter(status='active').count()
            
        org.posts_count = Post.objects.filter(
            content_type=content_type, 
            object_id=object_id,
            is_active=True
        ).count()
        
        org.save(update_fields=['followers_count', 'members_count', 'posts_count'])
        logger.info(f"Updated counts for {org.name}")
        
    except Exception as e:
        logger.error(f"Error updating counts for org {object_id}: {e}")


@shared_task
def fan_out_post_to_followers(post_id: str):
    """
    Push a new post to all followers' feeds.
    """
    try:
        post = Post.objects.get(id=post_id)
        org = post.organization
        
        # Get all followers
        followers = UserFollowOrganization.objects.filter(
            content_type=post.content_type,
            object_id=post.object_id
        ).values_list('user_id', flat=True)
        
        # Also include members if they aren't already following
        # For simplicity, we'll just iterate and create
        # In production, use bulk_create
        
        feed_items = []
        for user_id in followers:
            feed_items.append(
                Feed(
                    user_id=user_id,
                    post=post,
                    source_type='following',
                    relevance_score=80.0 # High initial score for followers
                )
            )
            
        Feed.objects.bulk_create(feed_items, ignore_conflicts=True)
        logger.info(f"Fanned out post {post_id} to {len(feed_items)} followers")
        
    except Post.DoesNotExist:
        logger.error(f"Post {post_id} not found for fan-out")
    except Exception as e:
        logger.error(f"Error in fan-out for post {post_id}: {e}")


@shared_task
def refresh_user_feeds():
    """
    Refresh feeds for all active users.

    This periodic task:
    1. Gets recent posts (last 7 days)
    2. Calculates relevance scores
    3. Updates or creates feed entries
    4. Removes old entries
    """
    logger.info("Starting feed refresh for all users")

    cutoff_date = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(
        created_at__gte=cutoff_date,
        is_active=True
    ).select_related('author')

    active_users = User.objects.filter(is_active=True)

    total_processed = 0
    total_created = 0

    for user in active_users:
        try:
            for post in recent_posts:
                # Check if post should be in feed
                should_include, reason = should_include_in_feed(user, post)

                if should_include:
                    # Calculate scores
                    scores = calculate_relevance_score(user, post)
                    source = get_source_type(user, post)

                    # Update or create feed entry
                    feed, created = Feed.objects.update_or_create(
                        user=user,
                        post=post,
                        defaults={
                            'relevance_score': scores['total'],
                            'engagement_score': scores['engagement'],
                            'recency_score': scores['recency'],
                            'relationship_score': scores['relationship'],
                            'priority_boost': scores['type_bonus'],
                            'source_type': source,
                        }
                    )

                    if created:
                        total_created += 1

                    total_processed += 1

        except Exception as e:
            logger.error(f"Error processing feed for user {user.email}: {e}")

    logger.info(f"Feed refresh complete. Processed: {total_processed}, Created: {total_created}")
    return {'processed': total_processed, 'created': total_created}


@shared_task
def refresh_user_feed(user_id: str):
    """
    Refresh feed for a specific user.

    Args:
        user_id: UUID of user
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Refreshing feed for user {user.email}")

        cutoff_date = timezone.now() - timedelta(days=7)
        recent_posts = Post.objects.filter(
            created_at__gte=cutoff_date,
            is_active=True
        ).select_related('author')

        processed = 0
        created = 0

        for post in recent_posts:
            should_include, reason = should_include_in_feed(user, post)

            if should_include:
                scores = calculate_relevance_score(user, post)
                source = get_source_type(user, post)

                feed, was_created = Feed.objects.update_or_create(
                    user=user,
                    post=post,
                    defaults={
                        'relevance_score': scores['total'],
                        'engagement_score': scores['engagement'],
                        'recency_score': scores['recency'],
                        'relationship_score': scores['relationship'],
                        'priority_boost': scores['type_bonus'],
                        'source_type': source,
                    }
                )

                if was_created:
                    created += 1
                processed += 1

        logger.info(f"Feed refresh complete for {user.email}. Processed: {processed}, Created: {created}")
        return {'user_id': str(user_id), 'processed': processed, 'created': created}

    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {'error': 'User not found'}
    except Exception as e:
        logger.error(f"Error refreshing feed for user {user_id}: {e}")
        return {'error': str(e)}


@shared_task
def cleanup_old_feed_items():
    """
    Remove feed entries older than 30 days.

    Keeps database clean and performant.
    """
    logger.info("Cleaning up old feed entries")

    cutoff_date = timezone.now() - timedelta(days=30)

    deleted_count, _ = Feed.objects.filter(
        created_at__lt=cutoff_date
    ).delete()

    logger.info(f"Deleted {deleted_count} old feed entries")
    return {'deleted_count': deleted_count}


@shared_task
def update_trending_content():
    """
    Update trending content markers.

    Identifies highly engaging posts and marks them as trending.
    """
    logger.info("Updating trending content")

    # Get posts from last 24 hours with high engagement
    cutoff = timezone.now() - timedelta(hours=24)

    trending_posts = Post.objects.filter(
        created_at__gte=cutoff,
        is_active=True
    ).filter(
        likes_count__gte=10  # Minimum 10 likes
    ).order_by('-likes_count', '-comments_count')[:50]

    # Update feed entries for these posts
    updated_count = 0
    for post in trending_posts:
        Feed.objects.filter(post=post).update(source_type='trending')
        updated_count += 1

    logger.info(f"Marked {updated_count} posts as trending")
    return {'trending_count': updated_count}


@shared_task
def rescore_feed_entries():
    """
    Rescore all recent feed entries.

    Useful after algorithm changes.
    """
    logger.info("Rescoring feed entries")

    cutoff = timezone.now() - timedelta(days=3)

    feed_entries = Feed.objects.filter(
        created_at__gte=cutoff
    ).select_related('user', 'post')

    updated_count = 0
    for feed_entry in feed_entries:
        try:
            scores = calculate_relevance_score(feed_entry.user, feed_entry.post)

            feed_entry.relevance_score = scores['total']
            feed_entry.engagement_score = scores['engagement']
            feed_entry.recency_score = scores['recency']
            feed_entry.relationship_score = scores['relationship']
            feed_entry.priority_boost = scores['type_bonus']
            feed_entry.save()

            updated_count += 1

        except Exception as e:
            logger.error(f"Error rescoring feed entry {feed_entry.id}: {e}")

    logger.info(f"Rescored {updated_count} feed entries")
    return {'rescored_count': updated_count}
