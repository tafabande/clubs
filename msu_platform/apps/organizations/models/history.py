"""Organization history model."""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid


class OrganizationHistory(models.Model):
    """Track historical metrics for organizations."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Generic foreign key to organization
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    organization = GenericForeignKey('content_type', 'object_id')

    date = models.DateField()
    member_count = models.IntegerField(default=0)
    event_count = models.IntegerField(default=0)
    engagement_score = models.FloatField(default=0.0)

    class Meta:
        db_table = 'organization_history'
        unique_together = ['content_type', 'object_id', 'date']
        ordering = ['-date']
