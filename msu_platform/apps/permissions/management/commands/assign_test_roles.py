"""
Assign roles to existing users for testing the RBAC dashboard system.
Gives the superuser System Admin, picks a few users as moderators and org leaders.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User
from apps.permissions.models import Role, UserRole
from apps.organizations.models import Club, Church, SportsTeam


class Command(BaseCommand):
    help = 'Assign test roles to existing users for RBAC dashboard testing'

    def handle(self, *args, **options):
        self.stdout.write('\nAssigning RBAC roles to users...\n')

        with transaction.atomic():
            # 1. Assign System Admin to all superusers
            admin_role = Role.objects.get(name='System Administrator')
            for su in User.objects.filter(is_superuser=True):
                ur, created = UserRole.objects.get_or_create(
                    user=su, role=admin_role,
                    content_type=None, object_id=None,
                    defaults={'granted_by': su}
                )
                self.stdout.write(f'  [{"NEW" if created else "EXISTS"}] System Admin -> {su.email}')

            # 2. Assign Moderator to 2 random non-super users
            mod_role = Role.objects.get(name='Moderator')
            regular_users = list(User.objects.filter(is_superuser=False)[:10])
            for u in regular_users[:2]:
                ur, created = UserRole.objects.get_or_create(
                    user=u, role=mod_role,
                    content_type=None, object_id=None,
                    defaults={'granted_by': User.objects.filter(is_superuser=True).first()}
                )
                self.stdout.write(f'  [{"NEW" if created else "EXISTS"}] Moderator -> {u.email}')

            # 3. Assign Club Presidents (creator of each club)
            club_pres = Role.objects.get(name='Club President')
            club_ct = ContentType.objects.get_for_model(Club)
            for club in Club.objects.all():
                if club.created_by:
                    ur, created = UserRole.objects.get_or_create(
                        user=club.created_by, role=club_pres,
                        content_type=club_ct, object_id=club.id,
                        defaults={'granted_by': club.created_by}
                    )
                    self.stdout.write(f'  [{"NEW" if created else "EXISTS"}] Club President ({club.name}) -> {club.created_by.email}')

            # 4. Assign Church Leaders
            church_leader = Role.objects.get(name='Church Leader')
            church_ct = ContentType.objects.get_for_model(Church)
            for church in Church.objects.all():
                if church.created_by:
                    ur, created = UserRole.objects.get_or_create(
                        user=church.created_by, role=church_leader,
                        content_type=church_ct, object_id=church.id,
                        defaults={'granted_by': church.created_by}
                    )
                    self.stdout.write(f'  [{"NEW" if created else "EXISTS"}] Church Leader ({church.name}) -> {church.created_by.email}')

            # 5. Assign Team Captains
            team_cap = Role.objects.get(name='Team Captain')
            team_ct = ContentType.objects.get_for_model(SportsTeam)
            for team in SportsTeam.objects.all():
                if team.created_by:
                    ur, created = UserRole.objects.get_or_create(
                        user=team.created_by, role=team_cap,
                        content_type=team_ct, object_id=team.id,
                        defaults={'granted_by': team.created_by}
                    )
                    self.stdout.write(f'  [{"NEW" if created else "EXISTS"}] Team Captain ({team.name}) -> {team.created_by.email}')

            # 6. Assign General User role to all remaining users
            gen_user = Role.objects.get(name='General User')
            assigned_user_ids = set(UserRole.objects.values_list('user_id', flat=True))
            for u in User.objects.filter(is_superuser=False).exclude(id__in=assigned_user_ids):
                UserRole.objects.get_or_create(
                    user=u, role=gen_user,
                    content_type=None, object_id=None,
                    defaults={'granted_by': User.objects.filter(is_superuser=True).first()}
                )

        total = UserRole.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nDone! {total} role assignments total.\n'))
