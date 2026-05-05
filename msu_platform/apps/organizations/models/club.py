"""Club models."""
from django.db import models
from apps.users.models import User
from .base import BaseOrganization
import uuid


class Club(BaseOrganization):
    """Model for student clubs."""

    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('arts', 'Arts & Culture'),
        ('science', 'Science'),
        ('business', 'Business & Entrepreneurship'),
        ('sports', 'Sports & Recreation'),
        ('service', 'Community Service'),
        ('academic', 'Academic'),
        ('other', 'Other'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    faculty_advisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='advised_clubs'
    )
    meeting_location = models.CharField(max_length=255, blank=True)
    meeting_schedule = models.TextField(blank=True)
    max_members = models.IntegerField(default=100)

    class Meta:
        db_table = 'clubs'
        indexes = [
            models.Index(fields=['is_active', 'is_approved'], name='clubs_status_idx'),
            models.Index(fields=['category', 'is_active'], name='clubs_category_idx'),
            models.Index(fields=['created_by'], name='clubs_creator_idx'),
            models.Index(fields=['-created_at'], name='clubs_created_idx'),
            models.Index(fields=['is_approved', '-created_at'], name='clubs_approved_created_idx'),
        ]


class ClubMembership(models.Model):
    """Club membership model."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    position = models.CharField(max_length=100, blank=True, help_text='Officer, Member, etc.')
    joined_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_club_members')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'club_memberships'
        unique_together = ['user', 'club']
        indexes = [
            models.Index(fields=['club', 'status'], name='club_membership_club_status_idx'),
            models.Index(fields=['user', 'status'], name='club_membership_user_status_idx'),
            models.Index(fields=['status', '-joined_at'], name='club_membership_status_joined_idx'),
        ]
