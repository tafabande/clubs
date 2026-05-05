"""Activity models."""
from django.db import models
from apps.users.models import User
from .base import BaseOrganization
import uuid


class Activity(BaseOrganization):
    """Model for campus activities."""

    ACTIVITY_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('competition', 'Competition'),
        ('seminar', 'Seminar'),
        ('social', 'Social Event'),
        ('other', 'Other'),
    ]

    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_participants = models.IntegerField(default=50)
    registration_deadline = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)

    class Meta:
        db_table = 'activities'
        verbose_name_plural = 'Activities'
        indexes = [
            models.Index(fields=['is_active', 'is_approved'], name='activities_status_idx'),
            models.Index(fields=['activity_type', 'is_active'], name='activities_type_idx'),
            models.Index(fields=['start_date'], name='activities_start_date_idx'),
            models.Index(fields=['end_date'], name='activities_end_date_idx'),
            models.Index(fields=['registration_deadline'], name='activities_reg_deadline_idx'),
            models.Index(fields=['is_recurring', 'start_date'], name='activities_recurring_idx'),
            models.Index(fields=['created_by'], name='activities_creator_idx'),
        ]


class ActivityRegistration(models.Model):
    """Activity registration model."""

    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_registrations')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registration_data = models.JSONField(default=dict, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_registrations'
        unique_together = ['user', 'activity']
        indexes = [
            models.Index(fields=['activity', 'status'], name='activity_reg_activity_status_idx'),
            models.Index(fields=['user', 'status'], name='activity_reg_user_status_idx'),
            models.Index(fields=['-registered_at'], name='activity_reg_registered_idx'),
        ]
