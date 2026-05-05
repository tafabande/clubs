"""
Follow and interest models for organizations.

Allows users to follow organizations and express interest.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.users.models import User
import uuid


class UserFollowOrganization(models.Model):
    """
    Track users following organizations.

    Generic relation allows following any organization type:
    - Club
    - Church
    - SportsTeam
    - Activity
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_organizations',
        help_text='User following the organization'
    )

    # Generic foreign key to any organization
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text='Type of organization (Club, Church, Sports Team, Activity)'
    )
    object_id = models.UUIDField(help_text='ID of the organization')
    organization = GenericForeignKey('content_type', 'object_id')

    # Notification preferences
    notify_on_posts = models.BooleanField(default=True, help_text='Notify on new posts')
    notify_on_events = models.BooleanField(default=True, help_text='Notify on new events')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_follow_organization'
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='follow_org_user_idx'),
            models.Index(fields=['content_type', 'object_id', '-created_at'], name='follow_org_ct_idx'),
            models.Index(fields=['user', 'content_type'], name='follow_org_user_ct_idx'),
            models.Index(fields=['user', 'notify_on_posts'], name='follow_org_notify_posts_idx'),
            models.Index(fields=['user', 'notify_on_events'], name='follow_org_notify_events_idx'),
        ]

    def __str__(self):
        org_name = str(self.organization) if self.organization else 'Unknown'
        return f"{self.user.email} follows {org_name}"

    @property
    def organization_name(self):
        """Return organization name."""
        return str(self.organization) if self.organization else ''

    @property
    def organization_type(self):
        """Return organization type."""
        if self.content_type:
            return self.content_type.model
        return ''


class UserInterestOrganization(models.Model):
    """
    Track users interested in joining organizations.

    Differs from following:
    - Following: passive observation
    - Interest: intent to join/participate

    Used for:
    - Recruitment tracking
    - Interest analytics
    - Targeted notifications
    """

    INTEREST_LEVELS = [
        ('low', 'Low Interest'),
        ('medium', 'Medium Interest'),
        ('high', 'High Interest'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organization_interests',
        help_text='User interested in the organization'
    )

    # Generic foreign key to any organization
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text='Type of organization'
    )
    object_id = models.UUIDField(help_text='ID of the organization')
    organization = GenericForeignKey('content_type', 'object_id')

    # Interest details
    interest_level = models.CharField(
        max_length=10,
        choices=INTEREST_LEVELS,
        default='medium',
        help_text='Level of interest'
    )
    notes = models.TextField(blank=True, help_text='User notes about interest')

    # Status tracking
    contacted = models.BooleanField(default=False, help_text='Has organization contacted user?')
    contacted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_interest_organization'
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='interest_org_user_idx'),
            models.Index(fields=['content_type', 'object_id', '-created_at'], name='interest_org_ct_idx'),
            models.Index(fields=['interest_level', '-created_at'], name='interest_org_level_idx'),
            models.Index(fields=['contacted', '-created_at'], name='interest_org_contacted_idx'),
            models.Index(fields=['content_type', 'object_id', 'contacted'], name='interest_org_ct_contacted_idx'),
        ]

    def __str__(self):
        org_name = str(self.organization) if self.organization else 'Unknown'
        return f"{self.user.email} interested in {org_name} ({self.interest_level})"

    @property
    def organization_name(self):
        """Return organization name."""
        return str(self.organization) if self.organization else ''

    @property
    def organization_type(self):
        """Return organization type."""
        if self.content_type:
            return self.content_type.model
        return ''

    def mark_contacted(self):
        """Mark that user has been contacted."""
        from django.utils import timezone
        self.contacted = True
        self.contacted_at = timezone.now()
        self.save(update_fields=['contacted', 'contacted_at', 'updated_at'])
