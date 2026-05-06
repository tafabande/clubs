// Application Constants

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api';
export const API_BASE_URL = rawBaseUrl.endsWith('/') ? rawBaseUrl : `${rawBaseUrl}/`;
export const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT || '30000', 10);

export const APP_NAME = import.meta.env.VITE_APP_NAME || 'MSU Platform';
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '3.0.0';

// Local Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'msu_access_token',
  REFRESH_TOKEN: 'msu_refresh_token',
  USER: 'msu_user',
  THEME: 'msu_theme',
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  // Auth (Base path /api/auth/)
  LOGIN: 'auth/login/',
  REGISTER: 'auth/register/',
  LOGOUT: 'auth/logout/',
  REFRESH: 'auth/refresh/',
  ME: 'auth/me/',

  // Organizations (Base path /api/orgs/)
  CLUBS: 'orgs/clubs/',
  CHURCHES: 'orgs/churches/',
  SPORTS_TEAMS: 'orgs/sports-teams/',
  ACTIVITIES: 'orgs/activities/',
  
  // Dynamic detail routes
  ORGANIZATION_DETAIL: (type: string, id: string | number) => `orgs/${(type || 'club').replace('_', '-')}/${id}/`,
  ORGANIZATION_JOIN: (type: string, id: string | number) => `orgs/${(type || 'club').replace('_', '-')}/${id}/join/`,
  ORGANIZATION_LEAVE: (type: string, id: string | number) => `orgs/${(type || 'club').replace('_', '-')}/${id}/leave/`,
  ORGANIZATION_MEMBERS: (type: string, id: string | number) => `orgs/${(type || 'club').replace('_', '-')}/${id}/members/`,
  
  // Posts & Feed (Base path /api/orgs/)
  POSTS: 'orgs/posts/',
  FEED: 'orgs/feed/',
  POST_DETAIL: (id: string | number) => `orgs/posts/${id}/`,
  POST_LIKE: (id: string | number) => `orgs/posts/${id}/like/`,
  POST_UNLIKE: (id: string | number) => `orgs/posts/${id}/unlike/`,
  POST_COMMENTS: (id: string | number) => `orgs/posts/${id}/comments/`,
  ORGANIZATION_POSTS: (type: string, id: string | number) => `orgs/${(type || 'club').replace('_', '-')}/${id}/posts/`,

  // Activities / Events (Base path /api/orgs/activities/)
  EVENTS: 'orgs/activities/',
  EVENT_DETAIL: (id: string | number) => `orgs/activities/${id}/`,
  EVENT_REGISTER: (id: string | number) => `orgs/activities/${id}/register/`,
  EVENT_UNREGISTER: (id: string | number) => `orgs/activities/${id}/cancel/`,

  // Search
  SEARCH: 'orgs/search/',

  // ── RBAC Dashboard Endpoints ────────────────────────────────────
  DASHBOARD_ROLE: 'dashboard/role/',
  DASHBOARD_ADMIN: 'dashboard/admin/',
  DASHBOARD_MODERATOR: 'dashboard/moderator/',
  DASHBOARD_ORG_LEADER: 'dashboard/org-leader/',
  DASHBOARD_USER: 'dashboard/user/',
  ADMIN_ASSIGN_ROLE: 'dashboard/admin/assign-role/',
  MOD_TOGGLE_POST: (postId: string) => `dashboard/mod/toggle-post/${postId}/`,

} as const;

// Query Keys
export const QUERY_KEYS = {
  AUTH: 'auth',
  ME: 'me',
  ORGANIZATIONS: 'organizations',
  ORGANIZATION: 'organization',
  POSTS: 'posts',
  POST: 'post',
  EVENTS: 'events',
  EVENT: 'event',
  USERS: 'users',
  USER: 'user',
  DASHBOARD_ROLE: 'dashboard-role',
  DASHBOARD_ADMIN: 'dashboard-admin',
  DASHBOARD_MODERATOR: 'dashboard-moderator',
  DASHBOARD_ORG_LEADER: 'dashboard-org-leader',
  DASHBOARD_USER: 'dashboard-user',
} as const;

// Default Pagination
export const DEFAULT_PAGE_SIZE = 20;

// Toast Durations
export const TOAST_DURATION = {
  SUCCESS: 3000,
  ERROR: 5000,
  WARNING: 4000,
  INFO: 3000,
} as const;
