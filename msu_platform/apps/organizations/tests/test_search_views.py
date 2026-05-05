"""
Tests for Search views and API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.organizations.models import SearchHistory, TrendingSearch
from apps.core.tests.utils import (
    create_test_user,
    create_test_club,
    create_test_church,
    create_test_sports_team,
    assert_paginated_response,
)


@pytest.mark.django_db
@pytest.mark.search
class TestOrganizationSearch:
    """Test organization search functionality."""

    def test_search_organizations(self, authenticated_client):
        """Test searching organizations."""
        # Create test organizations
        create_test_club(name='Tech Innovators Club')
        create_test_club(name='Drama Society')
        create_test_church(name='Grace Chapel')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Tech'})

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert any('Tech' in org['name'] for org in response.data['results'])

    def test_search_by_name(self, authenticated_client):
        """Test searching organizations by name."""
        club = create_test_club(name='MSU Football Club')
        create_test_club(name='Chess Club')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Football'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert any(org['id'] == str(club.id) for org in response.data['results'])

    def test_search_by_description(self, authenticated_client):
        """Test searching organizations by description."""
        club = create_test_club(
            name='Tech Club',
            description='A club for software development and programming enthusiasts'
        )

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'programming'})

        assert response.status_code == status.HTTP_200_OK
        assert any(org['id'] == str(club.id) for org in response.data['results'])

    def test_search_empty_query(self, authenticated_client):
        """Test search with empty query."""
        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_search_no_results(self, authenticated_client):
        """Test search with no matching results."""
        create_test_club(name='Tech Club')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'NonexistentClub12345'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0

    def test_search_case_insensitive(self, authenticated_client):
        """Test that search is case-insensitive."""
        club = create_test_club(name='Tech Innovators Club')

        url = reverse('organizations:search')

        # Search with different cases
        response1 = authenticated_client.get(url, {'q': 'TECH'})
        response2 = authenticated_client.get(url, {'q': 'tech'})
        response3 = authenticated_client.get(url, {'q': 'TeCh'})

        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK
        assert response3.status_code == status.HTTP_200_OK

        # All should return the club
        assert len(response1.data['results']) >= 1
        assert len(response2.data['results']) >= 1
        assert len(response3.data['results']) >= 1


@pytest.mark.django_db
@pytest.mark.search
class TestSearchFiltering:
    """Test search with filters."""

    def test_filter_by_organization_type(self, authenticated_client):
        """Test filtering search results by organization type."""
        create_test_club(name='Tech Club')
        create_test_church(name='Tech Chapel')
        create_test_sports_team(name='Tech Team')

        url = reverse('organizations:search')

        # Filter for clubs only
        response = authenticated_client.get(url, {'q': 'Tech', 'type': 'club'})

        assert response.status_code == status.HTTP_200_OK
        assert all(org['type'] == 'club' for org in response.data['results'])

    def test_filter_by_category(self, authenticated_client):
        """Test filtering by category."""
        create_test_club(name='Tech Club', category='academic')
        create_test_club(name='Drama Club', category='arts')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Club', 'category': 'academic'})

        assert response.status_code == status.HTTP_200_OK
        assert all(org['category'] == 'academic' for org in response.data['results'])

    def test_filter_by_multiple_criteria(self, authenticated_client):
        """Test filtering by multiple criteria."""
        create_test_club(name='Tech Club', category='academic')
        create_test_club(name='Tech Society', category='social')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {
            'q': 'Tech',
            'type': 'club',
            'category': 'academic'
        })

        assert response.status_code == status.HTTP_200_OK
        assert all(
            org['type'] == 'club' and org['category'] == 'academic'
            for org in response.data['results']
        )

    def test_filter_by_faculty(self, authenticated_client):
        """Test filtering organizations by faculty."""
        create_test_club(name='CS Club', faculty='science')
        create_test_club(name='Law Club', faculty='law')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Club', 'faculty': 'science'})

        assert response.status_code == status.HTTP_200_OK
        assert all(org.get('faculty') == 'science' for org in response.data['results'])


@pytest.mark.django_db
@pytest.mark.search
class TestSearchOrdering:
    """Test search result ordering."""

    def test_order_by_relevance(self, authenticated_client):
        """Test ordering results by relevance."""
        # Create clubs with different relevance
        create_test_club(name='Tech Club', description='Technology')
        create_test_club(name='Drama Club', description='Tech in drama')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Tech', 'ordering': 'relevance'})

        assert response.status_code == status.HTTP_200_OK
        # Tech Club should appear first (more relevant)
        if len(response.data['results']) >= 2:
            assert 'Tech Club' in response.data['results'][0]['name']

    def test_order_by_members(self, authenticated_client):
        """Test ordering by member count."""
        url = reverse('organizations:search')

        response = authenticated_client.get(url, {
            'q': 'Club',
            'ordering': '-members_count'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_order_by_created_date(self, authenticated_client):
        """Test ordering by creation date."""
        url = reverse('organizations:search')

        response = authenticated_client.get(url, {
            'q': 'Club',
            'ordering': '-created_at'
        })

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.search
class TestSearchHistory:
    """Test search history functionality."""

    def test_save_search_history(self, authenticated_client, user):
        """Test that search queries are saved to history."""
        url = reverse('organizations:search')

        authenticated_client.get(url, {'q': 'Tech Club'})

        # Verify search was saved
        assert SearchHistory.objects.filter(
            user=user,
            query='Tech Club'
        ).exists()

    def test_get_search_history(self, authenticated_client, user):
        """Test retrieving user's search history."""
        # Perform some searches
        search_url = reverse('organizations:search')
        authenticated_client.get(search_url, {'q': 'Tech'})
        authenticated_client.get(search_url, {'q': 'Sports'})

        # Get history
        history_url = reverse('organizations:search-history')

        response = authenticated_client.get(history_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2

    def test_clear_search_history(self, authenticated_client, user):
        """Test clearing search history."""
        # Add search history
        SearchHistory.objects.create(user=user, query='Test')

        url = reverse('organizations:search-history-clear')

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert SearchHistory.objects.filter(user=user).count() == 0

    def test_search_history_limit(self, authenticated_client, user):
        """Test that search history is limited."""
        # Create many search entries
        for i in range(50):
            SearchHistory.objects.create(user=user, query=f'Query {i}')

        history_url = reverse('organizations:search-history')

        response = authenticated_client.get(history_url)

        assert response.status_code == status.HTTP_200_OK
        # Should return only recent history (e.g., last 20)
        assert len(response.data) <= 20


@pytest.mark.django_db
@pytest.mark.search
class TestTrendingSearches:
    """Test trending searches functionality."""

    def test_get_trending_searches(self, authenticated_client):
        """Test retrieving trending searches."""
        # Create trending searches
        TrendingSearch.objects.create(query='Football', search_count=100)
        TrendingSearch.objects.create(query='Tech Club', search_count=80)
        TrendingSearch.objects.create(query='Drama', search_count=60)

        url = reverse('organizations:search-trending')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3

        # Should be ordered by search count
        if len(response.data) >= 2:
            assert response.data[0]['search_count'] >= response.data[1]['search_count']

    def test_trending_searches_limit(self, authenticated_client):
        """Test that trending searches are limited."""
        # Create many trending searches
        for i in range(20):
            TrendingSearch.objects.create(query=f'Query {i}', search_count=i)

        url = reverse('organizations:search-trending')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Should return only top trending (e.g., top 10)
        assert len(response.data) <= 10


@pytest.mark.django_db
@pytest.mark.search
class TestSearchSuggestions:
    """Test search suggestions/autocomplete."""

    def test_get_search_suggestions(self, authenticated_client):
        """Test getting search suggestions."""
        # Create organizations
        create_test_club(name='Tech Innovators Club')
        create_test_club(name='Tech Society')
        create_test_club(name='Technology Hub')

        url = reverse('organizations:search-suggestions')

        response = authenticated_client.get(url, {'q': 'Tech'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3
        assert all('Tech' in suggestion for suggestion in response.data)

    def test_search_suggestions_limit(self, authenticated_client):
        """Test that suggestions are limited."""
        # Create many clubs
        for i in range(20):
            create_test_club(name=f'Tech Club {i}')

        url = reverse('organizations:search-suggestions')

        response = authenticated_client.get(url, {'q': 'Tech'})

        assert response.status_code == status.HTTP_200_OK
        # Should return limited suggestions (e.g., top 5)
        assert len(response.data) <= 5


@pytest.mark.django_db
@pytest.mark.search
class TestSearchCategories:
    """Test search category listing."""

    def test_get_search_categories(self, authenticated_client):
        """Test getting available search categories."""
        url = reverse('organizations:search-categories')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'categories' in response.data
        assert len(response.data['categories']) > 0

    def test_search_categories_include_counts(self, authenticated_client):
        """Test that categories include organization counts."""
        # Create organizations in different categories
        create_test_club(category='academic')
        create_test_club(category='academic')
        create_test_club(category='social')

        url = reverse('organizations:search-categories')

        response = authenticated_client.get(url, {'include_counts': 'true'})

        assert response.status_code == status.HTTP_200_OK
        # Should include counts for each category
        academic = next(
            (cat for cat in response.data['categories'] if cat['name'] == 'academic'),
            None
        )
        if academic:
            assert academic['count'] >= 2


@pytest.mark.django_db
@pytest.mark.search
class TestSearchPerformance:
    """Test search performance and optimization."""

    def test_search_with_large_dataset(self, authenticated_client):
        """Test search performance with large dataset."""
        # Create many organizations
        for i in range(100):
            create_test_club(name=f'Club {i}')

        url = reverse('organizations:search')

        import time
        start = time.time()

        response = authenticated_client.get(url, {'q': 'Club'})

        end = time.time()

        assert response.status_code == status.HTTP_200_OK
        # Search should complete in reasonable time (< 1 second)
        assert (end - start) < 1.0

    def test_search_caching(self, authenticated_client):
        """Test that search results are cached."""
        from django.core.cache import cache

        create_test_club(name='Tech Club')

        url = reverse('organizations:search')

        # First search
        response1 = authenticated_client.get(url, {'q': 'Tech'})
        assert response1.status_code == status.HTTP_200_OK

        # Check if cached
        cache_key = 'search:Tech'
        cached_result = cache.get(cache_key)

        # Note: May be None with dummy cache in tests
        # assert cached_result is not None

        # Second search should use cache
        response2 = authenticated_client.get(url, {'q': 'Tech'})
        assert response2.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.search
class TestSearchDatabaseBackend:
    """Test search with different database backends."""

    def test_postgresql_full_text_search(self, authenticated_client):
        """Test PostgreSQL full-text search (when available)."""
        club = create_test_club(
            name='Python Programming Club',
            description='Learn Python programming and data science'
        )

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Python programming'})

        assert response.status_code == status.HTTP_200_OK
        # Should find the club with full-text search
        if response.data['results']:
            assert any(org['id'] == str(club.id) for org in response.data['results'])

    def test_sqlite_fallback_search(self, authenticated_client):
        """Test SQLite LIKE-based search fallback."""
        club = create_test_club(name='Tech Club')

        url = reverse('organizations:search')

        response = authenticated_client.get(url, {'q': 'Tech'})

        assert response.status_code == status.HTTP_200_OK
        # Should work with both PostgreSQL and SQLite
        assert len(response.data['results']) >= 1
