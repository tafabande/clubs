"""
Migration to add PostgreSQL full-text search vector.

This migration adds the search_vector field to SearchIndex model
for PostgreSQL full-text search. It only runs on PostgreSQL databases.

For SQLite (development), this migration is skipped and basic search
using LIKE queries is used instead.
"""
from django.db import migrations


def add_search_vector(apps, schema_editor):
    """Add search vector field and GIN index (PostgreSQL only)."""
    if schema_editor.connection.vendor == 'postgresql':
        # Import PostgreSQL-specific modules
        from django.contrib.postgres.search import SearchVector
        from django.contrib.postgres.indexes import GinIndex

        # Add search_vector as a generated column
        # Note: This requires PostgreSQL 12+
        schema_editor.execute("""
            ALTER TABLE search_index
            ADD COLUMN search_vector tsvector
            GENERATED ALWAYS AS (
                setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
                setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
                setweight(to_tsvector('english', coalesce(category, '')), 'C') ||
                setweight(to_tsvector('english', coalesce(tags, '')), 'D')
            ) STORED;
        """)

        # Create GIN index on search_vector for fast full-text search
        schema_editor.execute("""
            CREATE INDEX search_index_search_vector_idx
            ON search_index
            USING GIN (search_vector);
        """)

        print("✅ Search vector and GIN index created successfully")
    else:
        print("⚠️  Warning: Full-text search requires PostgreSQL. Skipping search_vector creation.")
        print("   Basic search using LIKE queries will be used instead.")


def remove_search_vector(apps, schema_editor):
    """Remove search vector field and index."""
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("""
            DROP INDEX IF EXISTS search_index_search_vector_idx;
        """)
        schema_editor.execute("""
            ALTER TABLE search_index DROP COLUMN IF EXISTS search_vector;
        """)


class Migration(migrations.Migration):
    """Add PostgreSQL search vector migration."""

    dependencies = [
        ('organizations', '0003_feed_and_search'),
    ]

    operations = [
        migrations.RunPython(
            add_search_vector,
            remove_search_vector,
            hints={'target_db': 'default'}
        ),
    ]
