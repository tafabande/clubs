"""
Management command to populate search index with existing organizations.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.organizations.models import (
    Club, Church, SportsTeam, Activity, SearchIndex
)


class Command(BaseCommand):
    help = 'Populate search index with existing organizations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing search index before populating',
        )

    def handle(self, *args, **options):
        """Populate search index."""
        # Clear existing index if requested
        if options['clear']:
            self.stdout.write('Clearing existing search index...')
            SearchIndex.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Search index cleared'))

        # Track statistics
        stats = {
            'clubs': 0,
            'churches': 0,
            'sports_teams': 0,
            'activities': 0,
            'total': 0
        }

        with transaction.atomic():
            # Index clubs
            self.stdout.write('Indexing clubs...')
            for club in Club.objects.filter(is_active=True):
                SearchIndex.objects.update_or_create(
                    organization_type='club',
                    organization_id=club.id,
                    defaults={
                        'name': club.name,
                        'description': club.description or '',
                        'category': club.category,
                        'tags': club.tags if hasattr(club, 'tags') else '',
                        'is_active': club.is_active,
                        'is_approved': club.is_approved,
                        'member_count': club.memberships.count()
                    }
                )
                stats['clubs'] += 1

            # Index churches
            self.stdout.write('Indexing churches...')
            for church in Church.objects.filter(is_active=True):
                SearchIndex.objects.update_or_create(
                    organization_type='church',
                    organization_id=church.id,
                    defaults={
                        'name': church.name,
                        'description': church.description or '',
                        'category': church.denomination,
                        'tags': church.tags if hasattr(church, 'tags') else '',
                        'is_active': church.is_active,
                        'is_approved': church.is_approved,
                        'member_count': church.memberships.count()
                    }
                )
                stats['churches'] += 1

            # Index sports teams
            self.stdout.write('Indexing sports teams...')
            for team in SportsTeam.objects.filter(is_active=True):
                SearchIndex.objects.update_or_create(
                    organization_type='sports_team',
                    organization_id=team.id,
                    defaults={
                        'name': team.name,
                        'description': team.description or '',
                        'category': team.sport_type,
                        'tags': team.tags if hasattr(team, 'tags') else '',
                        'is_active': team.is_active,
                        'is_approved': team.is_approved,
                        'member_count': team.memberships.count()
                    }
                )
                stats['sports_teams'] += 1

            # Index activities
            self.stdout.write('Indexing activities...')
            for activity in Activity.objects.filter(is_active=True):
                SearchIndex.objects.update_or_create(
                    organization_type='activity',
                    organization_id=activity.id,
                    defaults={
                        'name': activity.name,
                        'description': activity.description or '',
                        'category': activity.activity_type,
                        'tags': activity.tags if hasattr(activity, 'tags') else '',
                        'is_active': activity.is_active,
                        'is_approved': activity.is_approved,
                        'member_count': activity.registrations.count()
                    }
                )
                stats['activities'] += 1

        # Calculate total
        stats['total'] = sum([
            stats['clubs'],
            stats['churches'],
            stats['sports_teams'],
            stats['activities']
        ])

        # Display results
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ Search Index Population Complete'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f"  Clubs indexed:        {stats['clubs']}")
        self.stdout.write(f"  Churches indexed:     {stats['churches']}")
        self.stdout.write(f"  Sports teams indexed: {stats['sports_teams']}")
        self.stdout.write(f"  Activities indexed:   {stats['activities']}")
        self.stdout.write(self.style.SUCCESS('-' * 60))
        self.stdout.write(self.style.SUCCESS(f"  Total indexed:        {stats['total']}"))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
