"""
Script to migrate data from Flask SQLite database to Django PostgreSQL.
Run this after Django migrations are complete.
"""
import json
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def export_flask_data():
    """Export club data from Flask database to JSON."""
    # Use the static clubs.json as seed data
    flask_data_path = Path(__file__).parent.parent.parent / 'static' / 'clubs.json'

    if not flask_data_path.exists():
        print(f"Flask data not found at {flask_data_path}")
        return []

    with open(flask_data_path, 'r') as f:
        clubs_data = json.load(f)

    print(f"Exported {len(clubs_data)} clubs from Flask data")
    return clubs_data


def import_to_django(clubs_data):
    """Import club data into Django database."""
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    django.setup()

    from apps.users.models import User
    from apps.organizations.models import Club

    # Get or create a default admin user
    admin_user, created = User.objects.get_or_create(
        email='admin@msu.ac.zw',
        defaults={
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True,
            'is_verified': True,
        }
    )

    if created:
        admin_user.set_password('admin123')  # Change this!
        admin_user.save()
        print("Created admin user: admin@msu.ac.zw / admin123")

    # Import clubs
    imported = 0
    for club_data in clubs_data:
        # Map category
        category_map = {
            'Engineering': 'technology',
            'Games': 'sports',
            'Environmental': 'service',
            'Arts': 'arts',
            'Academic': 'academic',
            'Science': 'science',
            'Technology': 'technology',
        }

        category = category_map.get(club_data.get('category', 'Other'), 'other')

        club, created = Club.objects.get_or_create(
            email=club_data['email'],
            defaults={
                'name': club_data['name'],
                'description': club_data.get('description', ''),
                'category': category,
                'website': club_data.get('website', ''),
                'created_by': admin_user,
                'is_active': True,
                'is_approved': True,
                'approved_by': admin_user,
            }
        )

        if created:
            imported += 1
            print(f"  Imported: {club.name}")

    print(f"\nImported {imported} clubs into Django database")


if __name__ == '__main__':
    print("Starting Flask to Django data migration...")
    print("=" * 60)

    clubs_data = export_flask_data()

    if clubs_data:
        print("\nImporting to Django...")
        import_to_django(clubs_data)

    print("\nMigration complete!")
