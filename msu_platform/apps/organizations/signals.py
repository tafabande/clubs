"""
Signal handlers for organization models.

Handles:
- Follow count updates
- Feed generation triggers
- Notification triggers
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.organizations.models import UserFollowOrganization, UserInterestOrganization
from apps.users.models import UserFollow
import logging

logger = logging.getLogger(__name__)


# User Follow Signals (for follower/following counts)
# Note: Counts are calculated via properties, so no need to maintain separate fields

@receiver(post_save, sender=UserFollow)
def on_user_follow_created(sender, instance, created, **kwargs):
    """Handle user follow creation."""
    if created:
        logger.info(f"{instance.follower.email} followed {instance.following.email}")
        # Can trigger notifications here


@receiver(post_delete, sender=UserFollow)
def on_user_follow_deleted(sender, instance, **kwargs):
    """Handle user unfollow."""
    logger.info(f"{instance.follower.email} unfollowed {instance.following.email}")


# Organization Follow Signals

@receiver(post_save, sender=UserFollowOrganization)
def on_organization_follow_created(sender, instance, created, **kwargs):
    """Handle organization follow creation."""
    if created:
        logger.info(
            f"{instance.user.email} followed organization {instance.organization_name} "
            f"({instance.organization_type})"
        )
        # Can trigger:
        # - Welcome notification
        # - Feed generation
        # - Analytics update


@receiver(post_delete, sender=UserFollowOrganization)
def on_organization_follow_deleted(sender, instance, **kwargs):
    """Handle organization unfollow."""
    logger.info(
        f"{instance.user.email} unfollowed organization {instance.organization_name}"
    )


# Interest Signals

@receiver(post_save, sender=UserInterestOrganization)
def on_organization_interest_created(sender, instance, created, **kwargs):
    """Handle organization interest creation."""
    if created:
        logger.info(
            f"{instance.user.email} expressed {instance.interest_level} interest in "
            f"{instance.organization_name}"
        )
        # Can trigger:
        # - Notification to organization admins
        # - Add user to recruitment list
        # - Analytics update
