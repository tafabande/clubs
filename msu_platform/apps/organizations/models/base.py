"""
Base organization model.
"""
from django.db import models
from apps.users.models import User
import uuid


from apps.core.validators import validate_image_file

class BaseOrganization(models.Model):
    """Abstract base model for all organization types."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True, validators=[validate_image_file])

    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_%(class)ss'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_%(class)ss')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        # Note: Indexes are defined in concrete models (Club, Church, etc.)

    def __str__(self):
        return self.name
