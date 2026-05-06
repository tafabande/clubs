"""Church models."""
from django.db import models
from apps.users.models import User
from .base import BaseOrganization
import uuid


class Church(BaseOrganization):
    """Model for campus churches."""

    DENOMINATION_CHOICES = [
        ('protestant', 'Protestant'),
        ('catholic', 'Catholic'),
        ('orthodox', 'Orthodox'),
        ('pentecostal', 'Pentecostal'),
        ('islamic', 'Islamic'),
        ('other', 'Other'),
    ]

    denomination = models.CharField(max_length=50, choices=DENOMINATION_CHOICES)
    service_times = models.JSONField(default=dict, blank=True)
    pastor_name = models.CharField(max_length=255, blank=True)
    pastor_contact = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'churches'
        indexes = [
            models.Index(fields=['is_active', 'is_approved'], name='churches_status_idx'),
            models.Index(fields=['denomination', 'is_active'], name='churches_denomination_idx'),
            models.Index(fields=['created_by'], name='churches_creator_idx'),
            models.Index(fields=['-created_at'], name='churches_created_idx'),
        ]


class ChurchMembership(models.Model):
    """Church membership model."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='church_memberships')
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='memberships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    ministry = models.CharField(max_length=100, blank=True, help_text='Choir, Youth, etc.')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'church_memberships'
        unique_together = ['user', 'church']
        indexes = [
            models.Index(fields=['church', 'status'], name='church_mem_ch_stat_idx'),
            models.Index(fields=['user', 'status'], name='church_mem_usr_stat_idx'),
        ]
