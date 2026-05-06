"""
Seed default RBAC roles and permissions for MSU Platform.
Creates the 4-tier role system: System Admin, Moderator, Org Leader, General User.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.permissions.models import Permission, Role, RolePermission


# ── Permission Definitions ──────────────────────────────────────────────────
PERMISSIONS = [
    # System permissions
    ('system.manage_users', 'Manage Users', 'Add, remove, edit any user account', 'system'),
    ('system.manage_organizations', 'Manage Organizations', 'Approve, edit, remove any organization', 'system'),
    ('system.manage_posts', 'Manage All Posts', 'Edit or delete any post on the platform', 'system'),
    ('system.view_analytics', 'View System Analytics', 'Access traffic, usage, performance data', 'system'),
    ('system.view_audit_logs', 'View Audit Logs', 'Access full audit trail', 'system'),
    ('system.manage_roles', 'Manage Roles', 'Assign/revoke roles for users', 'system'),
    ('system.system_maintenance', 'System Maintenance', 'Perform maintenance operations', 'system'),
    ('system.resolve_errors', 'Resolve Errors', 'Monitor and resolve system errors', 'system'),
    ('system.view_security_events', 'View Security Events', 'Access security event logs', 'system'),

    # Moderation permissions
    ('mod.monitor_content', 'Monitor Content', 'View and review user-generated content', 'system'),
    ('mod.enforce_rules', 'Enforce Rules', 'Flag, hide, or remove rule-violating content', 'system'),
    ('mod.suspend_users', 'Suspend Users', 'Temporarily suspend user accounts', 'system'),
    ('mod.view_reports', 'View Reports', 'Access user reports and complaints', 'system'),
    ('mod.view_mod_stats', 'View Moderation Stats', 'Access basic moderation statistics', 'system'),

    # Organization-scoped permissions
    ('org.manage_page', 'Manage Organization Page', 'Edit org details, settings, logo', 'club'),
    ('org.manage_members', 'Manage Members', 'Approve, remove, change member roles', 'club'),
    ('org.manage_posts', 'Manage Org Posts', 'Create, edit, delete posts for the org', 'club'),
    ('org.create_events', 'Create Events', 'Create and manage org events', 'club'),
    ('org.view_analytics', 'View Org Analytics', 'View engagement and outreach stats', 'club'),
    ('org.manage_settings', 'Manage Org Settings', 'Change org configuration', 'club'),

    # General user permissions
    ('user.view_feed', 'View Feed', 'Access the main feed', 'system'),
    ('user.create_posts', 'Create Posts', 'Create posts in joined orgs', 'system'),
    ('user.join_organizations', 'Join Organizations', 'Request membership in orgs', 'system'),
    ('user.follow_organizations', 'Follow Organizations', 'Follow org updates', 'system'),
    ('user.manage_profile', 'Manage Profile', 'Edit own profile and settings', 'system'),
]

# ── Role Definitions ────────────────────────────────────────────────────────
ROLES = {
    'System Administrator': {
        'description': 'Full system access. All actions are logged and auditable.',
        'org_type': 'system',
        'is_system': True,
        'permissions': [p[0] for p in PERMISSIONS],  # ALL permissions
    },
    'Moderator': {
        'description': 'Community safety focused. Content monitoring and rule enforcement.',
        'org_type': 'system',
        'is_system': True,
        'permissions': [
            'mod.monitor_content', 'mod.enforce_rules', 'mod.suspend_users',
            'mod.view_reports', 'mod.view_mod_stats',
            'user.view_feed', 'user.manage_profile',
        ],
    },
    'Club President': {
        'description': 'Full management of their club page, members, and events.',
        'org_type': 'club',
        'is_system': False,
        'permissions': [
            'org.manage_page', 'org.manage_members', 'org.manage_posts',
            'org.create_events', 'org.view_analytics', 'org.manage_settings',
            'user.view_feed', 'user.create_posts', 'user.manage_profile',
        ],
    },
    'Church Leader': {
        'description': 'Full management of their church page, members, and events.',
        'org_type': 'church',
        'is_system': False,
        'permissions': [
            'org.manage_page', 'org.manage_members', 'org.manage_posts',
            'org.create_events', 'org.view_analytics', 'org.manage_settings',
            'user.view_feed', 'user.create_posts', 'user.manage_profile',
        ],
    },
    'Team Captain': {
        'description': 'Full management of their sports team page and roster.',
        'org_type': 'sports_team',
        'is_system': False,
        'permissions': [
            'org.manage_page', 'org.manage_members', 'org.manage_posts',
            'org.create_events', 'org.view_analytics', 'org.manage_settings',
            'user.view_feed', 'user.create_posts', 'user.manage_profile',
        ],
    },
    'Activity Coordinator': {
        'description': 'Full management of their activity/event page.',
        'org_type': 'activity',
        'is_system': False,
        'permissions': [
            'org.manage_page', 'org.manage_members', 'org.manage_posts',
            'org.create_events', 'org.view_analytics', 'org.manage_settings',
            'user.view_feed', 'user.create_posts', 'user.manage_profile',
        ],
    },
    'General User': {
        'description': 'Standard platform user. Personal dashboard, follow communities.',
        'org_type': 'system',
        'is_system': True,
        'permissions': [
            'user.view_feed', 'user.create_posts', 'user.join_organizations',
            'user.follow_organizations', 'user.manage_profile',
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed default RBAC roles and permissions for MSU Platform'

    def handle(self, *args, **options):
        self.stdout.write('\nSeeding RBAC roles and permissions...\n')

        with transaction.atomic():
            # Create permissions
            perm_map = {}
            for codename, name, desc, resource_type in PERMISSIONS:
                perm, created = Permission.objects.get_or_create(
                    codename=codename,
                    defaults={'name': name, 'description': desc, 'resource_type': resource_type}
                )
                perm_map[codename] = perm
                status = 'CREATED' if created else 'EXISTS'
                self.stdout.write(f'  [{status}] Permission: {codename}')

            # Create roles and assign permissions
            for role_name, config in ROLES.items():
                role, created = Role.objects.get_or_create(
                    name=role_name,
                    defaults={
                        'description': config['description'],
                        'organization_type': config['org_type'],
                        'is_system_role': config['is_system'],
                    }
                )
                status = 'CREATED' if created else 'EXISTS'
                self.stdout.write(f'\n  [{status}] Role: {role_name}')

                # Assign permissions
                for perm_code in config['permissions']:
                    if perm_code in perm_map:
                        RolePermission.objects.get_or_create(
                            role=role, permission=perm_map[perm_code]
                        )

                self.stdout.write(f'    -> {len(config["permissions"])} permissions assigned')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {Permission.objects.count()} permissions, {Role.objects.count()} roles seeded.\n'
        ))
