# Caching and Database Indexing Strategy

## Overview

This document describes the comprehensive caching and database indexing implementation for the MSU Platform, designed to optimize performance for high-traffic scenarios.

## Table of Contents

1. [Cache Architecture](#cache-architecture)
2. [Database Indexes](#database-indexes)
3. [Query Optimization](#query-optimization)
4. [Cache Invalidation](#cache-invalidation)
5. [Usage Examples](#usage-examples)
6. [Monitoring](#monitoring)
7. [Deployment](#deployment)

---

## Cache Architecture

### Cache Backend

**Technology**: Redis (via django-redis)

**Configuration**: `config/settings/base.py`

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://localhost:6379/1'),
        'KEY_PREFIX': 'msu_platform',
        'TIMEOUT': 300,  # 5 minutes default
    }
}
```

### Cache Layers

#### 1. Middleware Caching
**File**: `apps/core/middleware/cache.py`

- **Purpose**: Automatic response caching for GET requests
- **Scope**: API endpoints
- **Timeout**: 5 minutes (customizable per endpoint)
- **Headers**: Adds `X-Cache: HIT` header for cached responses

**Excluded Paths**:
- `/admin/` - Admin interface (requires fresh data)
- `/api/auth/` - Authentication endpoints
- `/api/users/me/` - User profile (frequently changing)

#### 2. View-Level Caching
Implemented in views for specific endpoints:

**Feed Endpoints** (`apps/organizations/views/feed.py`):
- User feed: 5 minutes
- Unread count: 1 minute
- Post details: 5 minutes

**Search Endpoints** (`apps/organizations/views/search.py`):
- Search results: 10 minutes
- Trending searches: 30 minutes
- Search suggestions: 15 minutes

#### 3. Fragment Caching
Using cache utilities in `apps/core/cache_utils.py`:

**Cache Timeouts**:
```python
CACHE_TIMEOUT_1_MIN = 60
CACHE_TIMEOUT_5_MIN = 300
CACHE_TIMEOUT_10_MIN = 600
CACHE_TIMEOUT_15_MIN = 900
CACHE_TIMEOUT_30_MIN = 1800
CACHE_TIMEOUT_1_HOUR = 3600
CACHE_TIMEOUT_1_DAY = 86400
```

### Cache Keys

Centralized cache key generation in `CacheKey` class:

**User Keys**:
- `user:profile:{user_id}` - User profile data
- `user:followers_count:{user_id}` - Follower count
- `user:following_count:{user_id}` - Following count
- `user:orgs_count:{user_id}` - Organizations count

**Feed Keys**:
- `feed:user:{user_id}:page:{page}` - User feed page
- `feed:discover:page:{page}` - Discover feed
- `feed:unread:{user_id}` - Unread count
- `feed:org:{org_type}:{org_id}:page:{page}` - Organization feed

**Search Keys**:
- `search:{query}:{org_type}:page:{page}` - Search results
- `search:trending` - Trending searches
- `search:suggestions:{prefix}` - Search suggestions

**Organization Keys**:
- `org:{org_type}:{org_id}` - Organization details
- `org:list:{org_type}:page:{page}` - Organization list
- `org:members:{org_type}:{org_id}` - Member list
- `org:followers_count:{org_type}:{org_id}` - Follower count

**Post Keys**:
- `post:{post_id}` - Post details
- `post:likes:{post_id}` - Likes count
- `post:comments:{post_id}` - Comments count

**Static Data Keys**:
- `static:categories` - Categories list (1 hour TTL)
- `static:faculties` - Faculties list (1 hour TTL)
- `static:departments` - Departments list (1 hour TTL)

---

## Database Indexes

### Index Strategy

All indexes are added to improve common query patterns while minimizing write performance impact.

### User Model Indexes

**File**: `apps/users/models.py`

```python
indexes = [
    models.Index(fields=['email']),               # Login lookups
    models.Index(fields=['student_id']),          # Student ID lookups
    models.Index(fields=['faculty']),             # Faculty filtering
    models.Index(fields=['department']),          # Department filtering
    models.Index(fields=['is_active', 'is_verified']),  # Status filtering
    models.Index(fields=['faculty', 'department']),     # Combined filter
    models.Index(fields=['-created_at']),         # Recent users
]
```

### Post Model Indexes

**File**: `apps/organizations/models/feed.py`

```python
indexes = [
    models.Index(fields=['-created_at']),                     # Recent posts
    models.Index(fields=['content_type', 'object_id']),       # Organization posts
    models.Index(fields=['author', '-created_at']),           # User posts
    models.Index(fields=['post_type', '-created_at']),        # Type filtering
    models.Index(fields=['is_pinned', '-created_at']),        # Pinned posts
    models.Index(fields=['visibility', '-created_at']),       # Visibility filter
    models.Index(fields=['is_active', '-created_at']),        # Active posts
    models.Index(fields=['content_type', 'object_id', '-created_at']),  # Org recent
    models.Index(fields=['event_date']),                      # Event posts
]
```

### Feed Model Indexes

```python
indexes = [
    models.Index(fields=['user', '-created_at']),                    # User feed
    models.Index(fields=['user', '-relevance_score']),               # Ranked feed
    models.Index(fields=['user', 'is_read', '-relevance_score']),    # Unread feed
    models.Index(fields=['is_read', '-created_at']),                 # All unread
    models.Index(fields=['source_type', '-created_at']),             # Source filter
    models.Index(fields=['post', 'user']),                           # Duplicate check
]
```

### Engagement Indexes

**PostLike**:
```python
indexes = [
    models.Index(fields=['post', 'user']),         # Check if liked
    models.Index(fields=['post', '-created_at']),  # Post likes timeline
    models.Index(fields=['user', '-created_at']),  # User likes timeline
]
```

**PostComment**:
```python
indexes = [
    models.Index(fields=['post', '-created_at']),     # Post comments
    models.Index(fields=['user', '-created_at']),     # User comments
    models.Index(fields=['parent', '-created_at']),   # Nested replies
    models.Index(fields=['is_active', '-created_at']), # Active comments
]
```

### Organization Indexes

**Club**:
```python
indexes = [
    models.Index(fields=['is_active', 'is_approved']),       # Status filter
    models.Index(fields=['category', 'is_active']),          # Category filter
    models.Index(fields=['created_by']),                     # Creator lookup
    models.Index(fields=['-created_at']),                    # Recent clubs
    models.Index(fields=['is_approved', '-created_at']),     # Approved recent
]
```

**ClubMembership**:
```python
indexes = [
    models.Index(fields=['club', 'status']),    # Club members by status
    models.Index(fields=['user', 'status']),    # User memberships by status
    models.Index(fields=['status', '-joined_at']),  # Recent by status
]
```

Similar indexes applied to Church, SportsTeam, and Activity models.

### Search Indexes

**SearchIndex**:
```python
indexes = [
    GinIndex(fields=['search_vector']),              # Full-text search
    models.Index(fields=['organization_type', 'is_active']),  # Type filter
    models.Index(fields=['is_active', 'is_approved', '-member_count']),  # Status + popularity
    models.Index(fields=['category', '-member_count']),       # Category + popularity
    models.Index(fields=['organization_id']),                 # Direct lookup
    models.Index(fields=['organization_type', 'organization_id']),  # Combined lookup
]
```

**PopularSearch**:
```python
indexes = [
    models.Index(fields=['-search_count']),     # Most popular
    models.Index(fields=['-last_searched']),    # Most recent
    models.Index(fields=['query']),             # Query lookup
]
```

### Follow/Interest Indexes

**UserFollowOrganization**:
```python
indexes = [
    models.Index(fields=['user', '-created_at']),                  # User follows
    models.Index(fields=['content_type', 'object_id', '-created_at']),  # Org followers
    models.Index(fields=['user', 'content_type']),                 # User type filter
    models.Index(fields=['user', 'notify_on_posts']),              # Notification filter
    models.Index(fields=['user', 'notify_on_events']),             # Event notifications
]
```

---

## Query Optimization

### Query Optimizer Utilities

**File**: `apps/organizations/query_optimizers.py`

Provides pre-optimized querysets with proper `select_related()` and `prefetch_related()` calls.

#### PostQueryOptimizer

**get_optimized_queryset()**:
- Selects related: author, content_type
- Prefetches: media, likes, comments
- Annotates: total_likes, total_comments, total_shares

**get_feed_posts(user, limit=20)**:
- Optimized for user feed display
- Includes user_liked annotation
- Orders by pinned status and recency

**get_organization_posts(content_type, object_id, limit=20)**:
- Organization-specific post feed
- Includes engagement counts
- Optimized for organization pages

#### FeedQueryOptimizer

**get_user_feed(user, limit=20, offset=0)**:
- Optimized user feed query
- Includes post details and author
- Pre-fetches media and engagement
- Annotates user interaction status

#### OrganizationQueryOptimizer

**get_clubs_with_counts()**:
- Active, approved clubs
- Annotates member_count and post_count
- Orders by popularity

**get_club_with_members(club_id)**:
- Single club with full member data
- Optimized for detail pages
- Includes faculty advisor

Similar methods for churches, sports teams, and activities.

#### SearchQueryOptimizer

**search_organizations(query, org_type=None, limit=20)**:
- Uses PostgreSQL full-text search
- Filters by active and approved status
- Returns ranked results

#### MembershipQueryOptimizer

**get_user_memberships(user)**:
- Returns dictionary with all membership types
- Annotates counts for each organization
- Single query per type

**get_organization_members(content_type_id, object_id, status='active')**:
- Generic member getter for any org type
- Selects related user data
- Filters by status

#### CommentQueryOptimizer

**get_post_comments(post_id, limit=50)**:
- Top-level comments with nested replies
- Prefetches reply data
- Selects related users

---

## Cache Invalidation

### Automatic Invalidation via Signals

**File**: `apps/core/signals.py`

Signals automatically invalidate cache when data changes.

#### User-Related Signals

**post_save(User)**:
- Invalidates user profile cache
- Clears follower/following counts

**post_save(UserFollow)**, **post_delete(UserFollow)**:
- Invalidates both users' caches
- Clears feed caches for follower

#### Post-Related Signals

**post_save(Post)**, **post_delete(Post)**:
- Invalidates post cache
- Clears organization feed cache
- Clears discover feed cache
- Triggers feed regeneration (Celery task)

**post_save(PostLike)**, **post_delete(PostLike)**:
- Invalidates post cache
- Updates like count cache

**post_save(PostComment)**, **post_delete(PostComment)**:
- Invalidates post cache
- Updates comment count cache

**post_save(PostShare)**:
- Invalidates post cache

#### Organization-Related Signals

**post_save(Club/Church/SportsTeam/Activity)**:
- Invalidates organization cache
- Clears organization list cache
- Clears search cache

**post_delete(Club/Church/SportsTeam/Activity)**:
- Same as post_save
- Removes from all caches

#### Membership-Related Signals

**post_save(ClubMembership)**, **post_delete(ClubMembership)**:
- Invalidates organization cache
- Invalidates user cache
- Clears member lists

Similar signals for ChurchMembership, SportsTeamMembership, ActivityRegistration.

#### Follow-Related Signals

**post_save(UserFollowOrganization)**, **post_delete(UserFollowOrganization)**:
- Invalidates organization cache
- Invalidates user cache
- Clears user feed cache (new posts visible)

#### Search-Related Signals

**post_save(SearchIndex)**, **post_delete(SearchIndex)**:
- Invalidates all search caches
- Forces search result refresh

### Manual Cache Invalidation

Use utility functions for manual invalidation:

```python
from apps.core.cache_utils import (
    invalidate_user_cache,
    invalidate_organization_cache,
    invalidate_post_cache,
    invalidate_cache_pattern
)

# Invalidate user cache
invalidate_user_cache(user_id)

# Invalidate organization cache
invalidate_organization_cache('club', club_id)

# Invalidate post cache
invalidate_post_cache(post_id)

# Invalidate pattern (use sparingly)
invalidate_cache_pattern('feed:user:*')
```

---

## Usage Examples

### Using Cache Decorators

```python
from apps.core.cache_utils import cache_result, cache_method, CACHE_TIMEOUT_15_MIN

# Function caching
@cache_result(timeout=CACHE_TIMEOUT_15_MIN, key_prefix='user_stats')
def get_user_statistics(user_id):
    # Expensive calculation
    return stats

# Method caching (includes self.id in key)
class Organization:
    @cache_method(timeout=CACHE_TIMEOUT_5_MIN, key_prefix='org_members')
    def get_active_members(self):
        return self.memberships.filter(status='active').count()
```

### Using Cache Keys

```python
from django.core.cache import cache
from apps.core.cache_utils import CacheKey, CACHE_TIMEOUT_5_MIN

# Get with cache
cache_key = CacheKey.user_profile(user_id)
profile = cache.get(cache_key)

if profile is None:
    # Cache miss - fetch from database
    profile = User.objects.get(id=user_id)
    cache.set(cache_key, profile, CACHE_TIMEOUT_5_MIN)
```

### Using Query Optimizers

```python
from apps.organizations.query_optimizers import PostQueryOptimizer, FeedQueryOptimizer

# Get optimized post queryset
posts = PostQueryOptimizer.get_feed_posts(user, limit=20)

# Get optimized user feed
feed = FeedQueryOptimizer.get_user_feed(user, limit=20, offset=0)

# Get organization with counts
from apps.organizations.query_optimizers import OrganizationQueryOptimizer
clubs = OrganizationQueryOptimizer.get_clubs_with_counts()
```

### Warm Cache on User Login

```python
from apps.core.cache_utils import warm_user_cache

def on_user_login(user):
    # Pre-populate cache with user data
    warm_user_cache(str(user.id))
```

---

## Monitoring

### Cache Hit/Miss Tracking

Add monitoring to track cache performance:

```python
# In views or middleware
import logging
logger = logging.getLogger(__name__)

cache_key = CacheKey.user_feed(user_id, page)
cached_data = cache.get(cache_key)

if cached_data:
    logger.info(f'Cache HIT: {cache_key}')
else:
    logger.info(f'Cache MISS: {cache_key}')
```

### Redis Monitoring Commands

```bash
# Connect to Redis
redis-cli

# Get all keys (use sparingly in production)
KEYS msu_platform:*

# Check specific key
GET msu_platform:user:profile:123

# Get key TTL
TTL msu_platform:user:profile:123

# Monitor commands in real-time
MONITOR

# Get cache stats
INFO stats
```

### Database Index Usage

Check index usage in PostgreSQL:

```sql
-- Index usage statistics
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Unused indexes
SELECT
    schemaname,
    tablename,
    indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexrelname NOT LIKE 'pg_toast%';

-- Table sizes
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Performance Metrics to Monitor

1. **Cache Hit Rate**: Should be >70% for frequently accessed data
2. **Average Response Time**: Should decrease after caching implementation
3. **Database Query Count**: Should decrease with effective caching
4. **Redis Memory Usage**: Monitor to prevent OOM errors
5. **Slow Query Log**: Identify queries that need optimization

---

## Deployment

### Requirements

Add to `requirements.txt`:
```txt
django-redis==5.4.0
```

Already included in project requirements.

### Environment Variables

Add to `.env`:
```bash
# Redis Configuration
REDIS_URL=redis://localhost:6379/1

# Cache Settings (optional)
CACHE_MIDDLEWARE_SECONDS=300
```

### Migration Steps

1. **Apply User Model Indexes**:
```bash
python manage.py migrate users 0001_initial_indexes
```

2. **Apply Organization Model Indexes**:
```bash
python manage.py migrate organizations 0005_add_performance_indexes
```

3. **Verify Indexes Created**:
```bash
python manage.py dbshell
\di  -- List all indexes (PostgreSQL)
```

### Redis Setup

**Development (Docker)**:
```bash
docker run -d -p 6379:6379 --name msu-redis redis:alpine
```

**Production**:
- Use managed Redis service (AWS ElastiCache, Redis Cloud, etc.)
- Enable persistence (RDB or AOF)
- Set up replication for high availability
- Configure maxmemory-policy (allkeys-lru recommended)

### Cache Warming Strategy

**On Deployment**:
```python
# Management command: warm_cache.py
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.core.cache_utils import warm_user_cache

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Warm cache for active users
        users = User.objects.filter(is_active=True)[:1000]
        for user in users:
            warm_user_cache(str(user.id))

        self.stdout.write('Cache warmed successfully')
```

Run after deployment:
```bash
python manage.py warm_cache
```

### Monitoring Setup

**Add to logging configuration**:
```python
LOGGING = {
    'loggers': {
        'cache': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
```

### Performance Testing

Before and after deployment:

```bash
# Load testing with locust
pip install locust

# Create locustfile.py for testing endpoints
locust -f locustfile.py --host=https://api.msu.ac.zw

# Database query analysis
python manage.py debugsqlshell
```

---

## Best Practices

### Cache Keys
- Always use `CacheKey` class for consistency
- Include version in keys if data structure changes
- Use meaningful prefixes

### Cache Timeouts
- Frequently changing data: 1-5 minutes
- Semi-static data: 10-30 minutes
- Static data: 1 hour - 1 day
- Never cache user-sensitive data for too long

### Query Optimization
- Always use query optimizers for complex queries
- Profile queries in development
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for ManyToMany and reverse ForeignKey
- Use `only()` for large models when you need few fields
- Use `defer()` to exclude large text/blob fields

### Index Maintenance
- Monitor index usage quarterly
- Remove unused indexes
- Rebuild indexes if fragmented (PostgreSQL: `REINDEX`)
- Update statistics: `ANALYZE`

### Cache Invalidation
- Let signals handle most invalidation
- Use pattern matching sparingly (expensive)
- Invalidate specific keys when possible
- Document custom invalidation logic

---

## Troubleshooting

### Cache Issues

**Problem**: Cache not working
```bash
# Check Redis connection
redis-cli ping
# Should return: PONG

# Check Django cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> cache.get('test')
# Should return: 'value'
```

**Problem**: Stale data in cache
- Check cache invalidation signals are firing
- Verify cache timeout is appropriate
- Manual flush: `cache.clear()`

**Problem**: Redis memory full
```bash
# Check memory usage
redis-cli INFO memory

# Clear all cache (use carefully!)
redis-cli FLUSHDB
```

### Database Issues

**Problem**: Slow queries despite indexes
```sql
-- Check if indexes are being used
EXPLAIN ANALYZE SELECT ...;

-- Rebuild statistics
ANALYZE table_name;

-- Rebuild index
REINDEX INDEX index_name;
```

**Problem**: Too many indexes
- Review pg_stat_user_indexes
- Remove indexes with idx_scan = 0
- Consolidate similar indexes

---

## Future Improvements

1. **Cache Tiering**: Add in-memory cache layer (Redis + local memory)
2. **Cache Preloading**: Background task to pre-populate cache
3. **Adaptive TTLs**: Adjust TTLs based on access patterns
4. **Cache Versioning**: Automatic invalidation on model changes
5. **Distributed Caching**: Redis Cluster for scalability
6. **Query Result Caching**: Cache expensive query results at ORM level
7. **CDN Integration**: Cache static content and media files
8. **Materialized Views**: For complex aggregation queries

---

## References

- Django Caching: https://docs.djangoproject.com/en/stable/topics/cache/
- django-redis: https://github.com/jazzband/django-redis
- PostgreSQL Indexes: https://www.postgresql.org/docs/current/indexes.html
- Redis Best Practices: https://redis.io/docs/manual/patterns/

---

**Document Version**: 1.0
**Last Updated**: 2026-05-05
**Maintained By**: Development Team
