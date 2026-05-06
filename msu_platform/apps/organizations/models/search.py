"""
Search functionality for organizations.

Provides full-text search across all organization types with filtering.
"""
from django.db import models
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.indexes import GinIndex
import uuid


class SearchIndex(models.Model):
    """
    Search index for fast full-text search across all organizations.

    This model stores searchable content from all organization types
    for efficient searching.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Organization reference
    organization_type = models.CharField(
        max_length=50,
        choices=[
            ('club', 'Club'),
            ('church', 'Church'),
            ('sports_team', 'Sports Team'),
            ('activity', 'Activity'),
        ]
    )
    organization_id = models.UUIDField()

    # Searchable fields
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    tags = models.TextField(blank=True, help_text='Space-separated tags')

    # Search vector for PostgreSQL full-text search (disabled on SQLite)
    search_vector = models.TextField(null=True, blank=True)

    # Metadata
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    member_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'search_index'
        indexes = [
            models.Index(fields=['search_vector'], name='search_vector_idx'),
            models.Index(fields=['organization_type', 'is_active'], name='search_type_active_idx'),
            models.Index(fields=['is_active', 'is_approved', '-member_count'], name='search_status_count_idx'),
            models.Index(fields=['category', '-member_count'], name='search_category_idx'),
            models.Index(fields=['organization_id'], name='search_org_id_idx'),
            models.Index(fields=['organization_type', 'organization_id'], name='search_org_type_id_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.organization_type})"

    @classmethod
    def search(cls, query, organization_type=None, category=None, limit=20):
        """
        Perform full-text search.

        Args:
            query: Search query string
            organization_type: Filter by organization type
            category: Filter by category
            limit: Maximum results

        Returns:
            QuerySet of SearchIndex objects ranked by relevance
        """
        search_query = SearchQuery(query)
        qs = cls.objects.filter(is_active=True, is_approved=True)

        # Filter by type
        if organization_type:
            qs = qs.filter(organization_type=organization_type)

        # Filter by category
        if category:
            qs = qs.filter(category=category)

        # Rank by relevance
        qs = qs.annotate(
            rank=SearchRank(models.F('search_vector'), search_query)
        ).filter(
            rank__gte=0.1  # Minimum relevance threshold
        ).order_by('-rank', '-member_count')[:limit]

        return qs


class PopularSearch(models.Model):
    """Track popular search queries for analytics and suggestions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(max_length=200, unique=True)
    search_count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'popular_searches'
        ordering = ['-search_count', '-last_searched']
        indexes = [
            models.Index(fields=['-search_count'], name='popular_search_count_idx'),
            models.Index(fields=['-last_searched'], name='popular_search_date_idx'),
            models.Index(fields=['query'], name='popular_search_query_idx'),
        ]

    def __str__(self):
        return f"{self.query} ({self.search_count} searches)"

    @classmethod
    def record_search(cls, query):
        """Record a search query."""
        obj, created = cls.objects.get_or_create(
            query=query.lower().strip(),
            defaults={'search_count': 1}
        )
        if not created:
            obj.search_count += 1
            obj.save()
        return obj

    @classmethod
    def get_trending(cls, limit=10):
        """Get trending search queries."""
        return cls.objects.all()[:limit]
