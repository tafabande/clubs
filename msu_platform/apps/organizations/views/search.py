"""
ViewSets for search functionality.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, F
from django.db import connection
from django.utils import timezone
from django.core.cache import cache

from apps.organizations.models import (
    SearchIndex, PopularSearch,
    Club, Church, SportsTeam, Activity
)
from apps.organizations.serializers.search import (
    SearchIndexSerializer, PopularSearchSerializer, SearchResultSerializer
)
from apps.core.cache_utils import (
    CacheKey, CACHE_TIMEOUT_10_MIN, CACHE_TIMEOUT_15_MIN, CACHE_TIMEOUT_30_MIN
)


class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for searching organizations.

    Endpoints:
    - GET /search/ - Search organizations
    - GET /search/trending/ - Get trending searches
    - GET /search/suggestions/ - Get search suggestions
    """

    serializer_class = SearchIndexSerializer
    permission_classes = [AllowAny]  # Search is public

    def get_queryset(self):
        """Get search index entries (approved and active only)."""
        return SearchIndex.objects.filter(
            is_active=True,
            is_approved=True
        )

    def list(self, request):
        """
        Search organizations with caching.

        Query params:
            - q: Search query (required)
            - type: Organization type filter (optional: club, church, sports_team, activity)
            - category: Category filter (optional)
            - limit: Number of results (default: 20, max: 100)
        """
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response(
                {'detail': 'Search query (q) is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get filters
        org_type = request.query_params.get('type', None)
        category = request.query_params.get('category', None)
        limit = min(int(request.query_params.get('limit', 20)), 100)
        page = int(request.query_params.get('page', 1))

        # Generate cache key
        cache_key = CacheKey.search_results(
            query,
            org_type=org_type,
            page=page
        )

        # Try to get from cache
        cached_results = cache.get(cache_key)

        if cached_results is not None:
            return Response(cached_results)

        # Cache miss - perform search
        # Record search query
        self._record_search(query)

        # Base queryset
        queryset = self.get_queryset()

        # Apply filters
        if org_type:
            queryset = queryset.filter(organization_type=org_type)

        if category:
            queryset = queryset.filter(category__icontains=category)

        # Perform search
        if connection.vendor == 'postgresql':
            # Use PostgreSQL full-text search
            from django.contrib.postgres.search import SearchQuery, SearchRank

            search_query = SearchQuery(query)
            queryset = queryset.annotate(
                rank=SearchRank(F('search_vector'), search_query)
            ).filter(rank__gte=0.1).order_by('-rank', '-member_count')[:limit]
        else:
            # Fallback to basic search for SQLite
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query) |
                Q(tags__icontains=query)
            ).order_by('-member_count')[:limit]

        # Enrich results with actual organization data
        results = []
        for item in queryset:
            organization = self._get_organization(item)
            if organization:
                results.append({
                    'id': str(organization.id),
                    'type': item.organization_type,
                    'name': item.name,
                    'description': item.description,
                    'category': item.category,
                    'member_count': item.member_count,
                    'is_approved': item.is_approved,
                    'organization': organization
                })

        serializer = SearchResultSerializer(results, many=True, context={'request': request})

        response_data = {
            'query': query,
            'count': len(results),
            'results': serializer.data
        }

        # Cache results for 10 minutes
        cache.set(cache_key, response_data, CACHE_TIMEOUT_10_MIN)

        return Response(response_data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """
        Get trending searches (last 7 days) with caching.

        Query params:
            - limit: Number of results (default: 10)
        """
        limit = min(int(request.query_params.get('limit', 10)), 50)

        # Try to get from cache
        cache_key = CacheKey.trending_searches()
        cached_trending = cache.get(cache_key)

        if cached_trending is not None:
            return Response(cached_trending)

        # Cache miss - fetch trending
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)

        trending = PopularSearch.objects.filter(
            last_searched__gte=seven_days_ago
        ).order_by('-search_count')[:limit]

        serializer = PopularSearchSerializer(trending, many=True)

        response_data = {
            'count': len(trending),
            'results': serializer.data
        }

        # Cache for 30 minutes
        cache.set(cache_key, response_data, CACHE_TIMEOUT_30_MIN)

        return Response(response_data)

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """
        Get search suggestions based on partial query with caching.

        Query params:
            - q: Partial query (required)
            - limit: Number of suggestions (default: 5)
        """
        query = request.query_params.get('q', '').strip()

        if not query or len(query) < 2:
            return Response({
                'suggestions': []
            })

        limit = min(int(request.query_params.get('limit', 5)), 20)

        # Generate cache key
        cache_key = CacheKey.search_suggestions(query.lower())

        # Try to get from cache
        cached_suggestions = cache.get(cache_key)

        if cached_suggestions is not None:
            return Response(cached_suggestions)

        # Cache miss - fetch suggestions
        suggestions = self.get_queryset().filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:limit]

        response_data = {
            'query': query,
            'suggestions': list(suggestions)
        }

        # Cache for 15 minutes
        cache.set(cache_key, response_data, CACHE_TIMEOUT_15_MIN)

        return Response(response_data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        Get available categories by organization type.

        Query params:
            - type: Organization type (optional)
        """
        org_type = request.query_params.get('type', None)

        queryset = self.get_queryset()

        if org_type:
            queryset = queryset.filter(organization_type=org_type)

        categories = queryset.values_list(
            'category', flat=True
        ).distinct().order_by('category')

        return Response({
            'type': org_type,
            'categories': [cat for cat in categories if cat]
        })

    def _record_search(self, query):
        """Record search query for trending analysis."""
        # Normalize query
        normalized_query = query.lower().strip()

        if len(normalized_query) < 2:
            return

        # Get or create popular search entry
        popular_search, created = PopularSearch.objects.get_or_create(
            query=normalized_query,
            defaults={'search_count': 0}
        )

        # Increment count
        popular_search.search_count = F('search_count') + 1
        popular_search.last_searched = timezone.now()
        popular_search.save(update_fields=['search_count', 'last_searched'])

    def _get_organization(self, search_item):
        """Get the actual organization object from search index item."""
        org_type = search_item.organization_type
        org_id = search_item.organization_id

        try:
            if org_type == 'club':
                return Club.objects.get(id=org_id, is_active=True)
            elif org_type == 'church':
                return Church.objects.get(id=org_id, is_active=True)
            elif org_type == 'sports_team':
                return SportsTeam.objects.get(id=org_id, is_active=True)
            elif org_type == 'activity':
                return Activity.objects.get(id=org_id, is_active=True)
        except (Club.DoesNotExist, Church.DoesNotExist, SportsTeam.DoesNotExist, Activity.DoesNotExist):
            return None

        return None
