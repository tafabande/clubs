"""
Dashboard API views for role-based dashboards.
Each dashboard endpoint returns data scoped to the user's role and permissions.
All admin/mod actions are logged via AuditService.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta

from apps.users.models import User
from apps.organizations.models import (
    Club, Church, SportsTeam, Activity,
    Post, PostLike, PostComment, SearchIndex,
    ClubMembership, ChurchMembership, SportsTeamMembership,
)
from apps.permissions.models import UserRole, Role
from apps.permissions.services import PermissionService
from apps.audit.models import AuditLog, SecurityEvent, UserActivityLog


def _get_user_system_role(user):
    """Get the highest system role for a user."""
    if user.is_superuser:
        return 'system_admin'
    roles = UserRole.objects.filter(
        user=user, content_type__isnull=True, object_id__isnull=True
    ).select_related('role').order_by('-role__is_system_role')
    for ur in roles:
        if not ur.is_expired():
            name = ur.role.name.lower().replace(' ', '_')
            if 'admin' in name:
                return 'system_admin'
            if 'moderator' in name:
                return 'moderator'
    return 'user'


def _get_user_led_orgs(user):
    """Get organizations where user is a leader."""
    leader_roles = ['Club President', 'Church Leader', 'Team Captain', 'Activity Coordinator']
    org_roles = UserRole.objects.filter(
        user=user, role__name__in=leader_roles
    ).select_related('role', 'content_type')
    return [ur for ur in org_roles if not ur.is_expired()]


# ── User Role Info Endpoint ─────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_role_info(request):
    """Return current user's role, permissions, and dashboard type."""
    user = request.user
    system_role = _get_user_system_role(user)
    led_orgs = _get_user_led_orgs(user)
    permissions = PermissionService.get_user_permissions(user)

    # Determine dashboard type
    if system_role == 'system_admin':
        dashboard = 'admin'
    elif system_role == 'moderator':
        dashboard = 'moderator'
    elif led_orgs:
        dashboard = 'org_leader'
    else:
        dashboard = 'user'

    return Response({
        'role': system_role,
        'dashboard': dashboard,
        'is_org_leader': len(led_orgs) > 0,
        'led_organizations': [
            {
                'id': str(ur.object_id),
                'type': ur.content_type.model if ur.content_type else None,
                'role': ur.role.name,
            }
            for ur in led_orgs
        ],
        'permissions': list(permissions.values_list('codename', flat=True)),
    })


# ── Admin Dashboard ─────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """System Admin dashboard - full system overview. Superuser or System Admin role required."""
    user = request.user
    role = _get_user_system_role(user)
    if role != 'system_admin' and not user.is_superuser:
        SecurityEvent.objects.create(
            event_type='PERMISSION_VIOLATION', severity='HIGH',
            user=user, ip_address=_get_ip(request),
            description=f'Unauthorized admin dashboard access attempt by {user.email}',
        )
        return Response({'detail': 'Insufficient permissions.'}, status=status.HTTP_403_FORBIDDEN)

    now = timezone.now()
    last_30d = now - timedelta(days=30)
    last_7d = now - timedelta(days=7)

    return Response({
        'overview': {
            'total_users': User.objects.count(),
            'active_users_30d': User.objects.filter(last_login__gte=last_30d).count(),
            'new_users_7d': User.objects.filter(created_at__gte=last_7d).count(),
            'verified_users': User.objects.filter(is_verified=True).count(),
        },
        'organizations': {
            'clubs': Club.objects.count(),
            'churches': Church.objects.count(),
            'sports_teams': SportsTeam.objects.count(),
            'activities': Activity.objects.count(),
            'pending_approval': (
                Club.objects.filter(is_approved=False).count() +
                Church.objects.filter(is_approved=False).count() +
                SportsTeam.objects.filter(is_approved=False).count()
            ),
        },
        'content': {
            'total_posts': Post.objects.count(),
            'posts_7d': Post.objects.filter(created_at__gte=last_7d).count(),
            'total_comments': PostComment.objects.count(),
            'total_likes': PostLike.objects.count(),
        },
        'security': {
            'events_7d': SecurityEvent.objects.filter(timestamp__gte=last_7d).count(),
            'unresolved_events': SecurityEvent.objects.filter(resolved=False).count(),
            'critical_events': SecurityEvent.objects.filter(
                severity='CRITICAL', resolved=False
            ).count(),
        },
        'recent_audit': list(
            AuditLog.objects.select_related('user').order_by('-timestamp')[:10].values(
                'id', 'action', 'timestamp', 'user__email', 'ip_address'
            )
        ),
    })


# ── Moderator Dashboard ─────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def moderator_dashboard(request):
    """Moderator dashboard - content monitoring and moderation stats."""
    user = request.user
    role = _get_user_system_role(user)
    if role not in ('system_admin', 'moderator') and not user.is_superuser:
        SecurityEvent.objects.create(
            event_type='PERMISSION_VIOLATION', severity='MEDIUM',
            user=user, ip_address=_get_ip(request),
            description=f'Unauthorized moderator dashboard access by {user.email}',
        )
        return Response({'detail': 'Insufficient permissions.'}, status=status.HTTP_403_FORBIDDEN)

    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)

    return Response({
        'content_stats': {
            'posts_24h': Post.objects.filter(created_at__gte=last_24h).count(),
            'posts_7d': Post.objects.filter(created_at__gte=last_7d).count(),
            'comments_24h': PostComment.objects.filter(created_at__gte=last_24h).count(),
            'flagged_posts': Post.objects.filter(is_active=False).count(),
        },
        'user_stats': {
            'new_users_7d': User.objects.filter(created_at__gte=last_7d).count(),
            'suspended_users': User.objects.filter(is_active=False).count(),
        },
        'recent_posts': list(
            Post.objects.select_related('author').order_by('-created_at')[:20].values(
                'id', 'title', 'content', 'post_type', 'created_at',
                'author__email', 'author__first_name', 'author__last_name',
                'likes_count', 'comments_count', 'is_active',
            )
        ),
        'recent_security': list(
            SecurityEvent.objects.filter(
                severity__in=['HIGH', 'CRITICAL']
            ).order_by('-timestamp')[:10].values(
                'id', 'event_type', 'severity', 'description', 'timestamp', 'resolved'
            )
        ),
    })


# ── Organization Leader Dashboard ────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def org_leader_dashboard(request):
    """Org leader dashboard - scoped to user's own organizations only."""
    user = request.user
    led_orgs = _get_user_led_orgs(user)
    is_admin = _get_user_system_role(user) == 'system_admin' or user.is_superuser

    if not led_orgs and not is_admin:
        return Response({'detail': 'You do not lead any organizations.'}, status=status.HTTP_403_FORBIDDEN)

    now = timezone.now()
    last_7d = now - timedelta(days=7)
    orgs_data = []

    for ur in led_orgs:
        ct = ur.content_type
        oid = ur.object_id
        if not ct or not oid:
            continue

        model_class = ct.model_class()
        try:
            org = model_class.objects.get(id=oid)
        except model_class.DoesNotExist:
            continue

        # Get posts for this org
        org_posts = Post.objects.filter(content_type=ct, object_id=oid)

        # Get membership count
        members = 0
        if hasattr(org, 'memberships'):
            members = org.memberships.count()

        orgs_data.append({
            'id': str(org.id),
            'name': org.name,
            'type': ct.model,
            'role': ur.role.name,
            'members_count': members,
            'followers_count': getattr(org, 'followers_count', 0),
            'posts_count': org_posts.count(),
            'posts_7d': org_posts.filter(created_at__gte=last_7d).count(),
            'engagement': {
                'total_likes': org_posts.aggregate(s=Sum('likes_count'))['s'] or 0,
                'total_comments': org_posts.aggregate(s=Sum('comments_count'))['s'] or 0,
            },
            'recent_posts': list(
                org_posts.order_by('-created_at')[:5].values(
                    'id', 'title', 'content', 'likes_count', 'comments_count', 'created_at'
                )
            ),
        })

    return Response({'organizations': orgs_data})


# ── General User Dashboard ──────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """General user dashboard - personal stats and followed communities."""
    user = request.user
    now = timezone.now()
    last_7d = now - timedelta(days=7)

    # Memberships
    club_memberships = ClubMembership.objects.filter(user=user, status='active').select_related('club')
    church_memberships = ChurchMembership.objects.filter(user=user, status='active').select_related('church')
    sports_memberships = SportsTeamMembership.objects.filter(user=user, status='active').select_related('sports_team')

    return Response({
        'profile': {
            'name': user.get_full_name(),
            'email': user.email,
            'faculty': user.faculty,
            'department': user.department,
            'year': user.year_of_study,
        },
        'memberships': {
            'clubs': [{'id': str(m.club.id), 'name': m.club.name, 'position': m.position} for m in club_memberships],
            'churches': [{'id': str(m.church.id), 'name': m.church.name, 'ministry': m.ministry} for m in church_memberships],
            'sports_teams': [{'id': str(m.sports_team.id), 'name': m.sports_team.name, 'position': m.position} for m in sports_memberships],
        },
        'stats': {
            'organizations_joined': club_memberships.count() + church_memberships.count() + sports_memberships.count(),
            'posts_count': user.posts_count,
        },
    })


# ── Admin Action Endpoints ──────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_assign_role(request):
    """Assign a role to a user. Admin only. Logged to audit."""
    user = request.user
    if not user.is_superuser and _get_user_system_role(user) != 'system_admin':
        return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    target_email = request.data.get('email')
    role_name = request.data.get('role')
    org_id = request.data.get('organization_id')
    org_type = request.data.get('organization_type')

    try:
        target_user = User.objects.get(email=target_email)
        role = Role.objects.get(name=role_name)
    except (User.DoesNotExist, Role.DoesNotExist) as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    organization = None
    if org_id and org_type:
        model_map = {
            'club': Club,
            'church': Church,
            'sportsteam': SportsTeam,
            'activity': Activity
        }
        model_class = model_map.get(org_type.lower())
        if model_class:
            try:
                organization = model_class.objects.get(id=org_id)
            except model_class.DoesNotExist:
                return Response({'detail': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)

    ur = PermissionService.assign_role(target_user, role, organization=organization, granted_by=user)

    # Audit log
    AuditLog.objects.create(
        user=user, action='CREATE', ip_address=_get_ip(request),
        changes={'action': 'assign_role', 'target': target_email, 'role': role_name},
    )

    return Response({'detail': f'Role "{role_name}" assigned to {target_email}.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mod_toggle_post(request, post_id):
    """Moderator: toggle post active/inactive. Logged to audit."""
    user = request.user
    role = _get_user_system_role(user)
    if role not in ('system_admin', 'moderator') and not user.is_superuser:
        return Response({'detail': 'Moderator access required.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    post.is_active = not post.is_active
    post.save()

    AuditLog.objects.create(
        user=user, action='UPDATE', ip_address=_get_ip(request),
        changes={'action': 'toggle_post', 'post_id': str(post_id), 'new_status': post.is_active},
    )

    action = 'restored' if post.is_active else 'hidden'
    return Response({'detail': f'Post {action} successfully.'})


def _get_ip(request):
    """Extract client IP from request."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '127.0.0.1')
