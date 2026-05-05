# Database Migration Guide

**Created:** May 5, 2026
**Migrations:** 0003_feed_and_search.py, 0004_add_search_vector.py

---

## 📋 Overview

Two new migrations have been created for the enhanced features:

1. **0003_feed_and_search.py** - Creates feed and search models
2. **0004_add_search_vector.py** - Adds PostgreSQL full-text search (PostgreSQL only)

---

## 🚀 Running Migrations

### Development (SQLite)

```bash
# Navigate to project directory
cd msu_platform

# Run migrations
python manage.py migrate organizations

# Expected output:
# Running migrations:
#   Applying organizations.0003_feed_and_search... OK
#   Applying organizations.0004_add_search_vector... OK (with warning)
```

**Note:** Migration 0004 will skip the search_vector creation on SQLite with a warning. This is expected behavior.

### Production (PostgreSQL)

```bash
# Ensure PostgreSQL database is configured
# Check .env file has DATABASE_URL pointing to PostgreSQL

# Run migrations
python manage.py migrate organizations

# Expected output:
# Running migrations:
#   Applying organizations.0003_feed_and_search... OK
#   Applying organizations.0004_add_search_vector... OK
#   ✅ Search vector and GIN index created successfully
```

---

## 📊 Models Created

### Migration 0003: Feed and Search Models

**Feed Models (6 models):**
1. **Post** - Organization posts with engagement tracking
2. **PostMedia** - Multiple media attachments per post
3. **PostLike** - User likes on posts
4. **PostComment** - Comments with nested replies
5. **PostShare** - Post sharing tracking
6. **Feed** - Personalized user feed

**Search Models (2 models):**
7. **SearchIndex** - Organization search index
8. **PopularSearch** - Trending search queries

**Total Tables Created:** 8
**Total Indexes Created:** 18

### Migration 0004: Search Vector (PostgreSQL Only)

**Fields Added:**
- `search_vector` (tsvector) - Generated column for full-text search

**Indexes Added:**
- GIN index on `search_vector` for fast full-text search

---

## 🔍 Database Schema

### Posts Table

```sql
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    author_id UUID REFERENCES users(id),
    content_type_id INTEGER REFERENCES django_content_type(id),
    object_id UUID,
    post_type VARCHAR(20),
    title VARCHAR(200),
    content TEXT,
    image VARCHAR(100),
    video VARCHAR(100),
    event_date TIMESTAMP,
    event_location VARCHAR(200),
    event_link VARCHAR(200),
    visibility VARCHAR(20),
    is_pinned BOOLEAN DEFAULT FALSE,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    tags VARCHAR(500)
);
```

### Search Index Table

```sql
CREATE TABLE search_index (
    id UUID PRIMARY KEY,
    organization_type VARCHAR(50),
    organization_id UUID,
    name VARCHAR(200),
    description TEXT,
    category VARCHAR(100),
    tags TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_approved BOOLEAN DEFAULT FALSE,
    member_count INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    -- PostgreSQL only:
    search_vector TSVECTOR GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(category, '')), 'C') ||
        setweight(to_tsvector('english', coalesce(tags, '')), 'D')
    ) STORED
);
```

---

## 📈 Performance Considerations

### Indexes Created

**Post Indexes:**
- `posts_created_idx` - Fast ordering by creation date
- `posts_org_idx` - Fast lookup by organization
- `posts_type_idx` - Fast filtering by post type
- `posts_pinned_idx` - Fast pinned posts retrieval
- `posts_vis_idx` - Fast visibility filtering

**PostLike Indexes:**
- `likes_post_user_idx` - Fast like checking
- `likes_user_idx` - Fast user likes retrieval
- **Unique constraint** on (post, user) - Prevents duplicate likes

**PostComment Indexes:**
- `comments_post_idx` - Fast comment retrieval
- `comments_user_idx` - Fast user comments

**Feed Indexes:**
- `feeds_user_idx` - Fast user feed retrieval
- `feeds_relevance_idx` - Fast ranking by relevance
- `feeds_read_idx` - Fast unread items filtering
- **Unique constraint** on (user, post) - Prevents duplicates

**Search Indexes:**
- `search_type_idx` - Fast filtering by organization type
- `search_approved_idx` - Fast approved items retrieval
- `search_category_idx` - Fast category filtering
- `search_index_search_vector_idx` (GIN) - Fast full-text search

**Total Indexes:** 18

### Expected Performance

**SQLite (Development):**
- Post queries: < 50ms
- Search queries: < 100ms (using LIKE)
- Feed queries: < 50ms

**PostgreSQL (Production):**
- Post queries: < 10ms
- Search queries: < 20ms (using full-text search)
- Feed queries: < 10ms

---

## 🧪 Verifying Migrations

### Check Migration Status

```bash
python manage.py showmigrations organizations
```

**Expected output:**
```
organizations
 [X] 0001_initial
 [X] 0002_enable_rls
 [X] 0003_feed_and_search
 [X] 0004_add_search_vector
```

### Verify Tables Created

**SQLite:**
```bash
python manage.py dbshell
```

```sql
.tables
-- Should show: posts, post_media, post_likes, post_comments, post_shares, feeds, search_index, popular_searches

.schema posts
-- Should show the posts table structure
```

**PostgreSQL:**
```bash
python manage.py dbshell
```

```sql
\dt
-- Should show all tables including new feed and search tables

\d posts
-- Should show the posts table structure

\di
-- Should show all indexes including new ones
```

### Verify Search Vector (PostgreSQL Only)

```sql
-- Check if search_vector column exists
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'search_index'
AND column_name = 'search_vector';

-- Should return:
--  column_name   | data_type
-- ---------------+-----------
--  search_vector | tsvector

-- Check if GIN index exists
SELECT indexname
FROM pg_indexes
WHERE tablename = 'search_index'
AND indexname = 'search_index_search_vector_idx';

-- Should return:
--           indexname
-- -------------------------------
--  search_index_search_vector_idx
```

---

## 🔄 Populating Search Index

After running migrations, you'll need to populate the search index with existing organizations.

### Create Management Command

**File:** `apps/organizations/management/commands/populate_search_index.py`

```python
from django.core.management.base import BaseCommand
from apps.organizations.models import (
    Club, Church, SportsTeam, Activity, SearchIndex
)


class Command(BaseCommand):
    help = 'Populate search index with existing organizations'

    def handle(self, *args, **options):
        # Clear existing index
        SearchIndex.objects.all().delete()

        # Index clubs
        for club in Club.objects.filter(is_active=True):
            SearchIndex.objects.create(
                organization_type='club',
                organization_id=club.id,
                name=club.name,
                description=club.description,
                category=club.category,
                is_active=club.is_active,
                is_approved=club.is_approved,
                member_count=club.clubmembership_set.count()
            )

        # Index churches
        for church in Church.objects.filter(is_active=True):
            SearchIndex.objects.create(
                organization_type='church',
                organization_id=church.id,
                name=church.name,
                description=church.description,
                category=church.denomination,
                is_active=church.is_active,
                is_approved=church.is_approved,
                member_count=church.churchmembership_set.count()
            )

        # Index sports teams
        for team in SportsTeam.objects.filter(is_active=True):
            SearchIndex.objects.create(
                organization_type='sports_team',
                organization_id=team.id,
                name=team.name,
                description=team.description,
                category=team.sport,
                is_active=team.is_active,
                is_approved=team.is_approved,
                member_count=team.sportsteammembership_set.count()
            )

        # Index activities
        for activity in Activity.objects.filter(is_active=True):
            SearchIndex.objects.create(
                organization_type='activity',
                organization_id=activity.id,
                name=activity.name,
                description=activity.description,
                category=activity.activity_type,
                is_active=activity.is_active,
                is_approved=activity.is_approved,
                member_count=activity.activityregistration_set.count()
            )

        count = SearchIndex.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully indexed {count} organizations')
        )
```

### Run Population Command

```bash
python manage.py populate_search_index
```

---

## 🔧 Troubleshooting

### Issue: Migration fails with "table already exists"

**Solution:**
```bash
# Check which migrations are applied
python manage.py showmigrations

# If needed, fake the migration
python manage.py migrate organizations 0003_feed_and_search --fake

# Then run the next migration
python manage.py migrate organizations
```

### Issue: search_vector field not working

**Cause:** Using SQLite in development

**Solution:** This is expected. The search_vector field is PostgreSQL-only. In development with SQLite, use basic search:

```python
# Instead of full-text search
SearchIndex.objects.filter(
    name__icontains=query
) | SearchIndex.objects.filter(
    description__icontains=query
)
```

### Issue: GIN index creation fails

**Cause:** PostgreSQL version < 12

**Solution:** Upgrade PostgreSQL or modify migration to not use generated columns:

```sql
-- Alternative for PostgreSQL < 12
ALTER TABLE search_index ADD COLUMN search_vector tsvector;

-- Create trigger to update search_vector
CREATE FUNCTION search_index_trigger() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', coalesce(NEW.name, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(NEW.description, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(NEW.category, '')), 'C') ||
    setweight(to_tsvector('english', coalesce(NEW.tags, '')), 'D');
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER search_vector_update
BEFORE INSERT OR UPDATE ON search_index
FOR EACH ROW EXECUTE FUNCTION search_index_trigger();
```

---

## 📝 Next Steps

After running migrations:

1. ✅ **Verify migrations applied** - `python manage.py showmigrations`
2. ✅ **Check database tables** - `python manage.py dbshell`
3. ✅ **Populate search index** - `python manage.py populate_search_index`
4. ✅ **Test feed creation** - Create a test post via Django shell
5. ✅ **Test search** - Try searching for organizations
6. ✅ **Implement views** - Use code from ENHANCED_FEATURES_GUIDE.md
7. ✅ **Test APIs** - Test all endpoints

---

## 🎉 Summary

**Migrations Created:** 2
**Tables Created:** 8
**Indexes Created:** 18
**Status:** ✅ Ready to Apply

Run the migrations to enable:
- ✅ Social feed functionality
- ✅ Full-text search
- ✅ Engagement tracking (likes, comments, shares)
- ✅ Personalized feeds
- ✅ Trending searches

**Commands:**
```bash
python manage.py migrate organizations
python manage.py populate_search_index  # After creating the command
```

---

**Last Updated:** May 5, 2026
**Version:** 1.0
