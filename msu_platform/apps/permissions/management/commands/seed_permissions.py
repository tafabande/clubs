"""
Management command to seed initial permissions and roles.
"""
from django.core.management.base import BaseCommand
from apps.permissions.models import Permission, Role, RolePermission


class Command(BaseCommand):
    help = 'Seed initial permissions and roles'

    def handle(self, *args, **options):
        self.stdout.write('Seeding permissions and roles...')

        # Create permissions
        permissions_data = [
            # Club permissions
            {'codename': 'can_create_club', 'name': 'Can create club', 'resource_type': 'club'},
            {'codename': 'can_edit_club', 'name': 'Can edit club', 'resource_type': 'club'},
            {'codename': 'can_delete_club', 'name': 'Can delete club', 'resource_type': 'club'},
            {'codename': 'can_approve_club_members', 'name': 'Can approve club members', 'resource_type': 'club'},
            {'codename': 'can_manage_club_events', 'name': 'Can manage club events', 'resource_type': 'club'},
            {'codename': 'can_view_club_analytics', 'name': 'Can view club analytics', 'resource_type': 'club'},

            # Church permissions
            {'codename': 'can_create_church', 'name': 'Can create church', 'resource_type': 'church'},
            {'codename': 'can_edit_church', 'name': 'Can edit church', 'resource_type': 'church'},
            {'codename': 'can_delete_church', 'name': 'Can delete church', 'resource_type': 'church'},
            {'codename': 'can_approve_church_members', 'name': 'Can approve church members', 'resource_type': 'church'},
            {'codename': 'can_manage_church_events', 'name': 'Can manage church events', 'resource_type': 'church'},

            # Sports Team permissions
            {'codename': 'can_create_sports_team', 'name': 'Can create sports team', 'resource_type': 'sports_team'},
            {'codename': 'can_edit_sports_team', 'name': 'Can edit sports team', 'resource_type': 'sports_team'},
            {'codename': 'can_delete_sports_team', 'name': 'Can delete sports team', 'resource_type': 'sports_team'},
            {'codename': 'can_approve_team_members', 'name': 'Can approve team members', 'resource_type': 'sports_team'},
            {'codename': 'can_manage_team_roster', 'name': 'Can manage team roster', 'resource_type': 'sports_team'},

            # Activity permissions
            {'codename': 'can_create_activity', 'name': 'Can create activity', 'resource_type': 'activity'},
            {'codename': 'can_edit_activity', 'name': 'Can edit activity', 'resource_type': 'activity'},
            {'codename': 'can_delete_activity', 'name': 'Can delete activity', 'resource_type': 'activity'},
            {'codename': 'can_manage_activity_registrations', 'name': 'Can manage activity registrations', 'resource_type': 'activity'},

            # System permissions
            {'codename': 'can_approve_organizations', 'name': 'Can approve organizations', 'resource_type': 'system'},
            {'codename': 'can_manage_users', 'name': 'Can manage users', 'resource_type': 'system'},
            {'codename': 'can_view_audit_logs', 'name': 'Can view audit logs', 'resource_type': 'system'},
        ]

        for perm_data in permissions_data:
            perm, created = Permission.objects.get_or_create(
                codename=perm_data['codename'],
                defaults={
                    'name': perm_data['name'],
                    'resource_type': perm_data['resource_type']
                }
            )
            if created:
                self.stdout.write(f'  Created permission: {perm.name}')

        # Create roles
        roles_data = [
            # System roles
            {'name': 'Platform Admin', 'organization_type': 'system', 'is_system_role': True,
             'permissions': ['can_approve_organizations', 'can_manage_users', 'can_view_audit_logs']},
            {'name': 'Faculty Advisor', 'organization_type': 'system', 'is_system_role': True,
             'permissions': ['can_approve_organizations']},
            {'name': 'Student', 'organization_type': 'system', 'is_system_role': True,
             'permissions': []},

            # Club roles
            {'name': 'Club President', 'organization_type': 'club', 'is_system_role': False,
             'permissions': ['can_edit_club', 'can_approve_club_members', 'can_manage_club_events', 'can_view_club_analytics']},
            {'name': 'Club Officer', 'organization_type': 'club', 'is_system_role': False,
             'permissions': ['can_manage_club_events']},
            {'name': 'Club Member', 'organization_type': 'club', 'is_system_role': False,
             'permissions': []},

            # Church roles
            {'name': 'Church Leader', 'organization_type': 'church', 'is_system_role': False,
             'permissions': ['can_edit_church', 'can_approve_church_members', 'can_manage_church_events']},
            {'name': 'Church Member', 'organization_type': 'church', 'is_system_role': False,
             'permissions': []},

            # Sports Team roles
            {'name': 'Team Captain', 'organization_type': 'sports_team', 'is_system_role': False,
             'permissions': ['can_edit_sports_team', 'can_approve_team_members', 'can_manage_team_roster']},
            {'name': 'Team Coach', 'organization_type': 'sports_team', 'is_system_role': False,
             'permissions': ['can_edit_sports_team', 'can_manage_team_roster']},
            {'name': 'Team Member', 'organization_type': 'sports_team', 'is_system_role': False,
             'permissions': []},

            # Activity roles
            {'name': 'Activity Coordinator', 'organization_type': 'activity', 'is_system_role': False,
             'permissions': ['can_edit_activity', 'can_manage_activity_registrations']},
            {'name': 'Activity Participant', 'organization_type': 'activity', 'is_system_role': False,
             'permissions': []},
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'organization_type': role_data['organization_type'],
                    'is_system_role': role_data['is_system_role']
                }
            )

            if created:
                self.stdout.write(f'  Created role: {role.name}')

                # Assign permissions to role
                for perm_codename in role_data['permissions']:
                    try:
                        permission = Permission.objects.get(codename=perm_codename)
                        RolePermission.objects.get_or_create(role=role, permission=permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'    Permission {perm_codename} not found'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded permissions and roles'))
