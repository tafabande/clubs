"""
Migration to enable Row-Level Security (RLS) on organization tables.

This migration applies PostgreSQL RLS policies for data access control.
It will only run on PostgreSQL databases.
"""
from django.db import migrations
from pathlib import Path


def load_sql_file():
    """Load the RLS SQL file."""
    sql_file = Path(__file__).parent.parent / 'sql' / 'enable_rls.sql'
    with open(sql_file, 'r') as f:
        return f.read()


def apply_rls(apps, schema_editor):
    """Apply RLS policies."""
    if schema_editor.connection.vendor == 'postgresql':
        sql = load_sql_file()
        schema_editor.execute(sql)
    else:
        print("Warning: RLS policies are only supported on PostgreSQL. Skipping...")


def reverse_rls(apps, schema_editor):
    """Reverse RLS policies."""
    if schema_editor.connection.vendor == 'postgresql':
        # Disable RLS on all tables
        reverse_sql = """
        ALTER TABLE clubs DISABLE ROW LEVEL SECURITY;
        ALTER TABLE churches DISABLE ROW LEVEL SECURITY;
        ALTER TABLE sports_teams DISABLE ROW LEVEL SECURITY;
        ALTER TABLE activities DISABLE ROW LEVEL SECURITY;
        ALTER TABLE club_memberships DISABLE ROW LEVEL SECURITY;
        ALTER TABLE church_memberships DISABLE ROW LEVEL SECURITY;
        ALTER TABLE sports_team_memberships DISABLE ROW LEVEL SECURITY;
        ALTER TABLE activity_registrations DISABLE ROW LEVEL SECURITY;
        
        -- Drop helper functions
        DROP FUNCTION IF EXISTS current_user_id();
        DROP FUNCTION IF EXISTS is_staff_user();
        DROP FUNCTION IF EXISTS has_organization_role(TEXT, UUID, TEXT[]);
        """
        schema_editor.execute(reverse_sql)


class Migration(migrations.Migration):
    """Enable RLS migration."""

    dependencies = [
        # This will depend on the initial organizations migration
        # Update after running makemigrations for the first time
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            apply_rls,
            reverse_rls,
            hints={'target_db': 'default'}
        ),
    ]
