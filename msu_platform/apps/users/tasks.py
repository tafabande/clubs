"""
Celery tasks for user-related background operations.
"""
from celery import shared_task
from apps.users.models import User, UserFollow
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_user_social_counts(user_id: str):
    """
    Update followers and following counts for a user.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Calculate counts
        user.followers_count_val = UserFollow.objects.filter(following=user).count()
        user.following_count_val = UserFollow.objects.filter(follower=user).count()
        
        user.save(update_fields=['followers_count_val', 'following_count_val'])
        logger.info(f"Updated social counts for user {user.email}")
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found for count update")
    except Exception as e:
        logger.error(f"Error updating user social counts: {e}")
