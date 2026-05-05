"""
Cache middleware for API responses.

Caches API responses based on user, URL, and query parameters.
"""
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from apps.core.cache_utils import generate_cache_key, CACHE_TIMEOUT_5_MIN
import json


class APICacheMiddleware(MiddlewareMixin):
    """
    Middleware to cache API responses.

    Caches GET requests for authenticated users.
    Cache key includes user ID, path, and query parameters.
    """

    # Paths that should not be cached
    EXCLUDE_PATHS = [
        '/admin/',
        '/api/auth/',
        '/api/users/me/',
    ]

    # Paths with custom cache timeouts (in seconds)
    CUSTOM_TIMEOUTS = {
        '/api/feed/': 300,  # 5 minutes
        '/api/search/': 600,  # 10 minutes
        '/api/organizations/': 300,  # 5 minutes
        '/api/posts/': 180,  # 3 minutes
    }

    def process_request(self, request):
        """
        Check cache before processing request.
        """
        # Only cache GET requests
        if request.method != 'GET':
            return None

        # Don't cache excluded paths
        if any(request.path.startswith(path) for path in self.EXCLUDE_PATHS):
            return None

        # Don't cache if caching is disabled
        if not getattr(request, 'cache_enabled', True):
            return None

        # Generate cache key
        user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
        cache_key = self._generate_cache_key(request, user_id)

        # Try to get from cache
        cached_response = cache.get(cache_key)

        if cached_response is not None:
            # Return cached response
            request._cached_response = True
            return self._create_response(cached_response)

        # Store cache key for use in process_response
        request._cache_key = cache_key

        return None

    def process_response(self, request, response):
        """
        Cache successful responses.
        """
        # Check if response should be cached
        if not self._should_cache_response(request, response):
            return response

        # Get cache key from request
        cache_key = getattr(request, '_cache_key', None)
        if not cache_key:
            return response

        # Determine cache timeout
        timeout = self._get_cache_timeout(request.path)

        # Cache the response
        cache_data = {
            'status_code': response.status_code,
            'content': response.content.decode('utf-8'),
            'content_type': response.get('Content-Type', 'application/json'),
        }

        cache.set(cache_key, cache_data, timeout)

        return response

    def _generate_cache_key(self, request, user_id):
        """Generate cache key for request."""
        path = request.path
        query_params = sorted(request.GET.items())

        return generate_cache_key(
            'api_response',
            user_id,
            path,
            *query_params
        )

    def _should_cache_response(self, request, response):
        """Determine if response should be cached."""
        # Don't cache if request was served from cache
        if getattr(request, '_cached_response', False):
            return False

        # Only cache successful responses
        if response.status_code != 200:
            return False

        # Only cache GET requests
        if request.method != 'GET':
            return False

        # Don't cache excluded paths
        if any(request.path.startswith(path) for path in self.EXCLUDE_PATHS):
            return False

        return True

    def _get_cache_timeout(self, path):
        """Get cache timeout for path."""
        for prefix, timeout in self.CUSTOM_TIMEOUTS.items():
            if path.startswith(prefix):
                return timeout

        return CACHE_TIMEOUT_5_MIN

    def _create_response(self, cache_data):
        """Create HTTP response from cached data."""
        from django.http import HttpResponse

        response = HttpResponse(
            content=cache_data['content'],
            status=cache_data['status_code'],
            content_type=cache_data['content_type']
        )

        # Add header to indicate cached response
        response['X-Cache'] = 'HIT'

        return response
