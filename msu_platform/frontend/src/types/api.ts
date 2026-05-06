// API Response Types and Models

// ============================================================================
// User Types
// ============================================================================

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile_picture?: string;
  bio?: string;
  date_joined: string;
  last_login?: string;
}

export interface UserProfile extends User {
  following_count: number;
  followers_count: number;
  organizations_count: number;
}

// ============================================================================
// Organization Types
// ============================================================================

export enum OrganizationType {
  CLUB = 'club',
  CHURCH = 'church',
  SPORTS_TEAM = 'sports_team',
  ACTIVITY = 'activity',
}

export interface BaseOrganization {
  id: number;
  name: string;
  description: string;
  organization_type: OrganizationType;
  logo?: string;
  cover_photo?: string;
  contact_email?: string;
  contact_phone?: string;
  created_at: string;
  updated_at: string;
  members_count: number;
  posts_count: number;
  is_member?: boolean;
}

export interface Club extends BaseOrganization {
  organization_type: OrganizationType.CLUB;
  club_type: 'academic' | 'social' | 'professional' | 'cultural' | 'other';
  meeting_schedule?: string;
  faculty?: string;
}

export interface Church extends BaseOrganization {
  organization_type: OrganizationType.CHURCH;
  denomination?: string;
  service_times?: string;
  location?: string;
}

export interface SportsTeam extends BaseOrganization {
  organization_type: OrganizationType.SPORTS_TEAM;
  sport_name: string;
  coach?: string;
  training_schedule?: string;
  achievements?: string;
}

export interface Activity extends BaseOrganization {
  organization_type: OrganizationType.ACTIVITY;
  activity_type: 'workshop' | 'seminar' | 'competition' | 'social' | 'other';
  start_date?: string;
  end_date?: string;
  venue?: string;
}

export type Organization = Club | Church | SportsTeam | Activity;

// ============================================================================
// Post Types
// ============================================================================

export interface PostMedia {
  id: number;
  media_type: 'image' | 'video' | 'document';
  file_url: string;
  thumbnail_url?: string;
  caption?: string;
  created_at: string;
}

export interface PostLike {
  id: number;
  user: User;
  created_at: string;
}

export interface PostComment {
  id: number;
  user: User;
  content: string;
  created_at: string;
  updated_at: string;
  replies_count: number;
  likes_count: number;
}

export interface Post {
  id: number;
  organization: BaseOrganization;
  author: User;
  content: string;
  media: PostMedia[];
  created_at: string;
  updated_at: string;
  likes_count: number;
  comments_count: number;
  is_liked?: boolean;
  is_pinned: boolean;
}

export interface PostDetail extends Post {
  comments: PostComment[];
  likes: PostLike[];
}

// ============================================================================
// Event Types
// ============================================================================

export interface Event {
  id: number;
  organization: BaseOrganization;
  title: string;
  description: string;
  event_type: 'meeting' | 'workshop' | 'social' | 'competition' | 'other';
  start_time: string;
  end_time: string;
  location?: string;
  venue?: string;
  max_participants?: number;
  current_participants: number;
  is_registered?: boolean;
  created_at: string;
  updated_at: string;
}

// ============================================================================
// Membership Types
// ============================================================================

export enum MembershipRole {
  ADMIN = 'admin',
  MODERATOR = 'moderator',
  MEMBER = 'member',
}

export enum MembershipStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
}

export interface Membership {
  id: number;
  user: User;
  organization: BaseOrganization;
  role: MembershipRole;
  status: MembershipStatus;
  joined_at: string;
}

// ============================================================================
// Authentication Types
// ============================================================================

export interface LoginRequest {
  email: string;
  password: string;
}


export interface RegisterRequest {
  email: string;
  student_id: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone?: string;
  faculty?: string;
  department?: string;
  year_of_study?: number;
}


export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface TokenRefreshRequest {
  refresh: string;
}

export interface TokenRefreshResponse {
  access: string;
}

// ============================================================================
// API Response Wrappers
// ============================================================================

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
  status?: number;
}

export interface ApiSuccess<T = unknown> {
  data: T;
  message?: string;
}

// ============================================================================
// Request Types
// ============================================================================

export interface CreatePostRequest {
  organization_id: number;
  content: string;
  media_files?: File[];
}

export interface UpdatePostRequest {
  content?: string;
}

export interface CreateCommentRequest {
  content: string;
}

export interface CreateOrganizationRequest {
  name: string;
  description: string;
  organization_type: OrganizationType;
  logo?: File;
  cover_photo?: File;
  contact_email?: string;
  contact_phone?: string;
  // Type-specific fields
  club_type?: string;
  denomination?: string;
  sport_name?: string;
  activity_type?: string;
}

export interface UpdateOrganizationRequest {
  name?: string;
  description?: string;
  logo?: File;
  cover_photo?: File;
  contact_email?: string;
  contact_phone?: string;
}

export interface JoinOrganizationRequest {
  organization_id: number;
}

export interface CreateEventRequest {
  organization_id: number;
  title: string;
  description: string;
  event_type: string;
  start_time: string;
  end_time: string;
  location?: string;
  venue?: string;
  max_participants?: number;
}

// ============================================================================
// Filter and Search Types
// ============================================================================

export interface OrganizationFilters {
  organization_type?: OrganizationType;
  search?: string;
  ordering?: 'name' | '-name' | 'created_at' | '-created_at' | 'members_count' | '-members_count';
  page?: number;
  page_size?: number;
}

export interface PostFilters {
  organization_id?: number;
  author_id?: number;
  search?: string;
  ordering?: 'created_at' | '-created_at' | 'likes_count' | '-likes_count';
  page?: number;
  page_size?: number;
}

export interface EventFilters {
  organization_id?: number;
  event_type?: string;
  start_date?: string;
  end_date?: string;
  search?: string;
  ordering?: 'start_time' | '-start_time';
  page?: number;
  page_size?: number;
}
