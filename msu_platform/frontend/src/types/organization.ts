export type OrganizationType = 'club' | 'church' | 'sports' | 'other';

export interface Organization {
  id: string;
  name: string;
  slug: string;
  description: string;
  logo?: string;
  banner?: string;
  organization_type: OrganizationType;
  faculty?: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  followers_count: number;
  members_count: number;
}

export interface OrganizationMember {
  id: string;
  user_id: string;
  organization_id: string;
  role: 'member' | 'admin' | 'moderator';
  joined_at: string;
}
