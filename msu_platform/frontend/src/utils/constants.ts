// Application Constants

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
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
  // Auth
  LOGIN: '/auth/login/',
  REGISTER: '/auth/register/',
  LOGOUT: '/auth/logout/',
  REFRESH: '/auth/refresh/',
  ME: '/auth/me/',

  // Organizations
  ORGANIZATIONS: '/orgs/',
  ORGANIZATION_DETAIL: (id: number) => `/orgs/${id}/`,
  ORGANIZATION_JOIN: (id: number) => `/orgs/${id}/join/`,
  ORGANIZATION_LEAVE: (id: number) => `/orgs/${id}/leave/`,
  ORGANIZATION_MEMBERS: (id: number) => `/orgs/${id}/members/`,
  ORGANIZATION_POSTS: (id: number) => `/orgs/${id}/posts/`,

  // Posts
  POSTS: '/posts/',
  POST_DETAIL: (id: number) => `/posts/${id}/`,
  POST_LIKE: (id: number) => `/posts/${id}/like/`,
  POST_UNLIKE: (id: number) => `/posts/${id}/unlike/`,
  POST_COMMENTS: (id: number) => `/posts/${id}/comments/`,

  // Events
  EVENTS: '/events/',
  EVENT_DETAIL: (id: number) => `/events/${id}/`,
  EVENT_REGISTER: (id: number) => `/events/${id}/register/`,
  EVENT_UNREGISTER: (id: number) => `/events/${id}/unregister/`,

  // Users
  USERS: '/users/',
  USER_DETAIL: (id: number) => `/users/${id}/`,
  USER_PROFILE: (id: number) => `/users/${id}/profile/`,
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
