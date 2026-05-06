"""
Signal handlers for organization models.

Handles:
- Follow count updates
- Feed generation triggers
- Notification triggers
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.organizations.models import UserFollowOrganization, UserInterestOrganization, Post
from apps.organizations.models.club import ClubMembership
from apps.organizations.models.church import ChurchMembership
from apps.organizations.models.sports import SportsTeamMembership
from apps.organizations.models.activity import ActivityMembership
from apps.users.models import UserFollow
from apps.organizations.tasks import update_organization_counts, fan_out_post_to_followers
from apps.users.tasks import update_user_social_counts
import logging

logger = logging.getLogger(__name__)


# User Follow Signals
@receiver(post_save, sender=UserFollow)
def on_user_follow_created(sender, instance, created, **kwargs):
    if created:
        update_user_social_counts.delay(str(instance.follower_id))
        update_user_social_counts.delay(str(instance.following_id))

@receiver(post_delete, sender=UserFollow)
def on_user_follow_deleted(sender, instance, **kwargs):
    update_user_social_counts.delay(str(instance.follower_id))
    update_user_social_counts.delay(str(instance.following_id))


# Organization Follow Signals
@receiver(post_save, sender=UserFollowOrganization)
def on_organization_follow_created(sender, instance, created, **kwargs):
    if created:
        update_organization_counts.delay(instance.content_type_id, str(instance.object_id))

@receiver(post_delete, sender=UserFollowOrganization)
def on_organization_follow_deleted(sender, instance, **kwargs):
    update_organization_counts.delay(instance.content_type_id, str(instance.object_id))


# Post Signals
@receiver(post_save, sender=Post)
def on_post_created(sender, instance, created, **kwargs):
    if created:
        # Update org post count
        update_organization_counts.delay(instance.content_type_id, str(instance.object_id))
        # Fan out to followers
        fan_out_post_to_followers.delay(str(instance.id))

@receiver(post_delete, sender=Post)
def on_post_deleted(sender, instance, **kwargs):
    update_organization_counts.delay(instance.content_type_id, str(instance.object_id))


# Membership Signals (example for Club)
@receiver(post_save, sender=ClubMembership)
def on_club_membership_update(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(instance.club)
    update_organization_counts.delay(ct.id, str(instance.club_id))

@receiver(post_delete, sender=ClubMembership)
def on_club_membership_delete(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(instance.club)
    update_organization_counts.delay(ct.id, str(instance.club_id))
