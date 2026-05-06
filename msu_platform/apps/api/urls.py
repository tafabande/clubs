"""
API URL configuration.
"""
from django.urls import path, include

app_name = 'api'

from .views import api_root
from .dashboard_views import (
    user_role_info, admin_dashboard, moderator_dashboard,
    org_leader_dashboard, user_dashboard,
    admin_assign_role, mod_toggle_post,
)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('auth/', include('apps.users.urls')),
    path('orgs/', include('apps.organizations.urls')),

    # ── RBAC Dashboard Endpoints ────────────────────────────────────
    path('dashboard/role/', user_role_info, name='dashboard-role'),
    path('dashboard/admin/', admin_dashboard, name='dashboard-admin'),
    path('dashboard/moderator/', moderator_dashboard, name='dashboard-moderator'),
    path('dashboard/org-leader/', org_leader_dashboard, name='dashboard-org-leader'),
    path('dashboard/user/', user_dashboard, name='dashboard-user'),

    # ── Admin/Mod Action Endpoints ──────────────────────────────────
    path('dashboard/admin/assign-role/', admin_assign_role, name='admin-assign-role'),
    path('dashboard/mod/toggle-post/<uuid:post_id>/', mod_toggle_post, name='mod-toggle-post'),
]
