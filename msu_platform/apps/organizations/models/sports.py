"""Sports team models."""
from django.db import models
from apps.users.models import User
from .base import BaseOrganization
import uuid


class SportsTeam(BaseOrganization):
    """Model for sports teams."""

    SPORT_TYPE_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('volleyball', 'Volleyball'),
        ('rugby', 'Rugby'),
        ('tennis', 'Tennis'),
        ('athletics', 'Athletics'),
        ('other', 'Other'),
    ]

    DIVISION_CHOICES = [
        ('mens', "Men's"),
        ('womens', "Women's"),
        ('mixed', 'Mixed'),
    ]

    sport_type = models.CharField(max_length=50, choices=SPORT_TYPE_CHOICES)
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES)
    coach = models.CharField(max_length=255, blank=True)
    practice_schedule = models.TextField(blank=True)
    max_roster_size = models.IntegerField(default=25)

    class Meta:
        db_table = 'sports_teams'
        indexes = [
            models.Index(fields=['is_active', 'is_approved'], name='sports_status_idx'),
            models.Index(fields=['sport_type', 'is_active'], name='sports_type_idx'),
            models.Index(fields=['division', 'sport_type'], name='sports_division_type_idx'),
            models.Index(fields=['created_by'], name='sports_creator_idx'),
            models.Index(fields=['-created_at'], name='sports_created_idx'),
        ]


class SportsTeamMembership(models.Model):
    """Sports team membership model."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('injured', 'Injured'),
        ('inactive', 'Inactive'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sports_memberships')
    sports_team = models.ForeignKey(SportsTeam, on_delete=models.CASCADE, related_name='memberships')
    position = models.CharField(max_length=100, blank=True)
    jersey_number = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sports_team_memberships'
        unique_together = ['user', 'sports_team']
        indexes = [
            models.Index(fields=['sports_team', 'status'], name='sports_membership_team_status_idx'),
            models.Index(fields=['user', 'status'], name='sports_membership_user_status_idx'),
        ]
