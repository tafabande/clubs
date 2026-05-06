export interface User {
  id: string;
  email: string;
  student_id?: string;
  first_name: string;
  last_name: string;
  phone?: string;
  faculty?: string;
  department?: string;
  year_of_study?: number;
  is_active: boolean;
  is_staff: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
  followers_count?: number;
  following_count?: number;
  organizations_following_count?: number;
}

export type UserRole = 'student' | 'staff' | 'admin';
