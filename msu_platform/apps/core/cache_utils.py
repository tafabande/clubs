"""
Cache utilities for MSU Platform.

Provides helper functions and decorators for caching across the application.
"""
from functools import wraps
from django.core.cache import cache
from django.conf import settings
import hashlib
import json
from typing import Any, Callable, Optional


# Cache timeout constants (in seconds)
CACHE_TIMEOUT_1_MIN = 60
CACHE_TIMEOUT_5_MIN = 300
CACHE_TIMEOUT_10_MIN = 600
CACHE_TIMEOUT_15_MIN = 900
CACHE_TIMEOUT_30_MIN = 1800
CACHE_TIMEOUT_1_HOUR = 3600
CACHE_TIMEOUT_1_DAY = 86400


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate a unique cache key from prefix and arguments.

    Args:
        prefix: Cache key prefix
        *args: Positional arguments to include in key
        **kwargs: Keyword arguments to include in key

    Returns:
        Unique cache key string
    """
    # Serialize arguments to JSON for consistent hashing
    key_data = {
        'args': [str(arg) for arg in args],
        'kwargs': {k: str(v) for k, v in sorted(kwargs.items())}
    }
    key_string = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()

    key_prefix = settings.CACHES['default'].get('KEY_PREFIX', 'msu')
    return f"{key_prefix}:{prefix}:{key_hash}"


def get_or_set_cache(
    key: str,
    default_func: Callable,
    timeout: Optional[int] = None,
    *args,
    **kwargs
) -> Any:
    """
    Get value from cache or set it using default function.

    Args:
        key: Cache key
        default_func: Function to call if cache miss
        timeout: Cache timeout in seconds
        *args: Arguments to pass to default_func
        **kwargs: Keyword arguments to pass to default_func

    Returns:
        Cached value or result of default_func
    """
    value = cache.get(key)

    if value is None:
        value = default_func(*args, **kwargs)
        cache.set(key, value, timeout)

    return value


def invalidate_cache(*keys: str) -> None:
    """
    Invalidate (delete) one or more cache keys.

    Args:
        *keys: Cache keys to invalidate
    """
    if keys:
        cache.delete_many(keys)


def invalidate_cache_pattern(pattern: str) -> None:
    """
    Invalidate all cache keys matching a pattern.

    Note: This requires Redis and uses the KEYS command.
    Use sparingly in production as it can be slow.

    Args:
        pattern: Cache key pattern (e.g., "user:*")
    """
    try:
        # Get the Redis client
        redis_client = cache.client.get_client()

        # Get all keys matching pattern
        key_prefix = settings.CACHES['default'].get('KEY_PREFIX', 'msu')
        full_pattern = f"{key_prefix}:{pattern}"
        keys = redis_client.keys(full_pattern)

        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        # Log error but don't break application
        print(f"Error invalidating cache pattern {pattern}: {e}")


def cache_result(timeout: int = CACHE_TIMEOUT_5_MIN, key_prefix: str = None):
    """
    Decorator to cache function results.

    Args:
        timeout: Cache timeout in seconds
        key_prefix: Custom cache key prefix (defaults to function name)

    Example:
        @cache_result(timeout=300, key_prefix='user_profile')
        def get_user_profile(user_id):
            return User.objects.get(id=user_id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            prefix = key_prefix or func.__name__
            cache_key = generate_cache_key(prefix, *args, **kwargs)

            # Try to get from cache
            result = cache.get(cache_key)

            if result is None:
                # Cache miss - call function
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)

            return result

        return wrapper
    return decorator


def cache_method(timeout: int = CACHE_TIMEOUT_5_MIN, key_prefix: str = None):
    """
    Decorator to cache method results (includes self in cache key).

    Args:
        timeout: Cache timeout in seconds
        key_prefix: Custom cache key prefix

    Example:
        class User:
            @cache_method(timeout=300, key_prefix='user_stats')
            def get_stats(self):
                return calculate_stats(self.id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Include object ID in cache key
            prefix = key_prefix or f"{self.__class__.__name__}_{func.__name__}"
            obj_id = getattr(self, 'id', None) or getattr(self, 'pk', None)

            cache_key = generate_cache_key(prefix, obj_id, *args, **kwargs)

            # Try to get from cache
            result = cache.get(cache_key)

            if result is None:
                # Cache miss - call method
                result = func(self, *args, **kwargs)
                cache.set(cache_key, result, timeout)

            return result

        return wrapper
    return decorator


def cache_page_for_user(timeout: int = CACHE_TIMEOUT_5_MIN):
    """
    Cache decorator for views that are user-specific.

    Args:
        timeout: Cache timeout in seconds

    Example:
        @cache_page_for_user(timeout=300)
        def user_feed(request):
            ...
    """
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Generate cache key including user and path
            user_id = getattr(request.user, 'id', 'anonymous')
            path = request.get_full_path()
            cache_key = generate_cache_key('view', user_id, path)

            # Try to get from cache
            response = cache.get(cache_key)

            if response is None:
                # Cache miss - call view
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key, response, timeout)

            return response

        return wrapper
    return decorator


class CacheKey:
    """
    Centralized cache key definitions.

    Provides consistent cache key naming across the application.
    """

    # User cache keys
    @staticmethod
    def user_profile(user_id: str) -> str:
        return f"user:profile:{user_id}"

    @staticmethod
    def user_followers_count(user_id: str) -> str:
        return f"user:followers_count:{user_id}"

    @staticmethod
    def user_following_count(user_id: str) -> str:
        return f"user:following_count:{user_id}"

    @staticmethod
    def user_organizations_count(user_id: str) -> str:
        return f"user:orgs_count:{user_id}"

    # Feed cache keys
    @staticmethod
    def user_feed(user_id: str, page: int = 1) -> str:
        return f"feed:user:{user_id}:page:{page}"

    @staticmethod
    def discover_feed(page: int = 1) -> str:
        return f"feed:discover:page:{page}"

    @staticmethod
    def feed_unread_count(user_id: str) -> str:
        return f"feed:unread:{user_id}"

    @staticmethod
    def organization_feed(org_type: str, org_id: str, page: int = 1) -> str:
        return f"feed:org:{org_type}:{org_id}:page:{page}"

    # Search cache keys
    @staticmethod
    def search_results(query: str, org_type: str = None, page: int = 1) -> str:
        org_filter = org_type or 'all'
        return f"search:{query}:{org_filter}:page:{page}"

    @staticmethod
    def trending_searches() -> str:
        return "search:trending"

    @staticmethod
    def search_suggestions(prefix: str) -> str:
        return f"search:suggestions:{prefix}"

    # Organization cache keys
    @staticmethod
    def organization_detail(org_type: str, org_id: str) -> str:
        return f"org:{org_type}:{org_id}"

    @staticmethod
    def organization_list(org_type: str, page: int = 1) -> str:
        return f"org:list:{org_type}:page:{page}"

    @staticmethod
    def organization_members(org_type: str, org_id: str) -> str:
        return f"org:members:{org_type}:{org_id}"

    @staticmethod
    def organization_followers_count(org_type: str, org_id: str) -> str:
        return f"org:followers_count:{org_type}:{org_id}"

    # Post cache keys
    @staticmethod
    def post_detail(post_id: str) -> str:
        return f"post:{post_id}"

    @staticmethod
    def post_likes_count(post_id: str) -> str:
        return f"post:likes:{post_id}"

    @staticmethod
    def post_comments_count(post_id: str) -> str:
        return f"post:comments:{post_id}"

    # Static data cache keys
    @staticmethod
    def categories() -> str:
        return "static:categories"

    @staticmethod
    def faculties() -> str:
        return "static:faculties"

    @staticmethod
    def departments() -> str:
        return "static:departments"


def warm_user_cache(user_id: str) -> None:
    """
    Pre-populate cache with user data.

    Args:
        user_id: User ID to warm cache for
    """
    from apps.users.models import User

    try:
        user = User.objects.get(id=user_id)

        # Cache user profile data
        profile_data = {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.get_full_name(),
            'faculty': user.faculty,
            'department': user.department,
        }
        cache.set(
            CacheKey.user_profile(str(user.id)),
            profile_data,
            CACHE_TIMEOUT_15_MIN
        )

        # Cache counts
        cache.set(
            CacheKey.user_followers_count(str(user.id)),
            user.followers_count,
            CACHE_TIMEOUT_5_MIN
        )
        cache.set(
            CacheKey.user_following_count(str(user.id)),
            user.following_count,
            CACHE_TIMEOUT_5_MIN
        )

    except User.DoesNotExist:
        pass


def invalidate_user_cache(user_id: str) -> None:
    """
    Invalidate all cache entries for a user.

    Args:
        user_id: User ID to invalidate cache for
    """
    keys = [
        CacheKey.user_profile(user_id),
        CacheKey.user_followers_count(user_id),
        CacheKey.user_following_count(user_id),
        CacheKey.user_organizations_count(user_id),
        CacheKey.feed_unread_count(user_id),
    ]
    invalidate_cache(*keys)

    # Invalidate feed pages
    invalidate_cache_pattern(f"feed:user:{user_id}:*")


def invalidate_organization_cache(org_type: str, org_id: str) -> None:
    """
    Invalidate all cache entries for an organization.

    Args:
        org_type: Organization type (club, church, sports_team, activity)
        org_id: Organization ID
    """
    keys = [
        CacheKey.organization_detail(org_type, org_id),
        CacheKey.organization_members(org_type, org_id),
        CacheKey.organization_followers_count(org_type, org_id),
    ]
    invalidate_cache(*keys)

    # Invalidate feed and list pages
    invalidate_cache_pattern(f"feed:org:{org_type}:{org_id}:*")
    invalidate_cache_pattern(f"org:list:{org_type}:*")


def invalidate_post_cache(post_id: str) -> None:
    """
    Invalidate all cache entries for a post.

    Args:
        post_id: Post ID
    """
    keys = [
        CacheKey.post_detail(post_id),
        CacheKey.post_likes_count(post_id),
        CacheKey.post_comments_count(post_id),
    ]
    invalidate_cache(*keys)
