// Organizations Service

import api from './api';
import { API_ENDPOINTS } from '@/utils/constants';
import { OrganizationType } from '@/types';
import type {
  Organization,
  PaginatedResponse,
  OrganizationFilters,
  CreateOrganizationRequest,
  UpdateOrganizationRequest,
  Membership,
  Post,
} from '@/types';

/**
 * Helper to get the correct endpoint for an organization type
 */
const getEndpointByType = (type?: OrganizationType | string) => {
  switch (type) {
    case OrganizationType.CLUB:
    case 'club':
    case 'clubs':
      return API_ENDPOINTS.CLUBS;
    case OrganizationType.CHURCH:
    case 'church':
    case 'churches':
      return API_ENDPOINTS.CHURCHES;
    case OrganizationType.SPORTS_TEAM:
    case 'sports_team':
    case 'sports-teams':
      return API_ENDPOINTS.SPORTS_TEAMS;
    case OrganizationType.ACTIVITY:
    case 'activity':
    case 'activities':
      return API_ENDPOINTS.ACTIVITIES;
    default:
      return API_ENDPOINTS.CLUBS; // Default to clubs
  }
};

/**
 * Helper to get the pluralized type string for URLs
 */
const getPluralType = (type: OrganizationType | string): string => {
  const t = (type || 'club').toLowerCase();
  switch (t) {
    case OrganizationType.CLUB:
    case 'club':
    case 'clubs':
      return 'clubs';
    case OrganizationType.CHURCH:
    case 'church':
    case 'churches':
      return 'churches';
    case OrganizationType.SPORTS_TEAM:
    case 'sports_team':
    case 'sports-team':
    case 'sports-teams':
      return 'sports-teams';
    case OrganizationType.ACTIVITY:
    case 'activity':
    case 'activities':
      return 'activities';
    default:
      return String(t).replace('_', '-');
  }
};

export const organizationsService = {
  /**
   * Get all organizations with filters
   */
  async getOrganizations(filters?: OrganizationFilters): Promise<PaginatedResponse<Organization>> {
    // If we have a search query, use the global search endpoint
    if (filters?.search) {
      const response = await api.get<PaginatedResponse<Organization>>(
        API_ENDPOINTS.SEARCH,
        { params: filters }
      );
      return response.data;
    }

    // Otherwise, fetch from the specific type endpoint if provided, or default to clubs
    const endpoint = getEndpointByType(filters?.organization_type);
    const response = await api.get<PaginatedResponse<Organization>>(
      endpoint,
      { params: filters }
    );
    return response.data;
  },

  /**
   * Get organization by ID and type
   */
  async getOrganization(type: OrganizationType | string, id: string | number): Promise<Organization> {
    const pluralType = getPluralType(type);
    const response = await api.get<Organization>(API_ENDPOINTS.ORGANIZATION_DETAIL(pluralType, id));
    return response.data;
  },

  /**
   * Create new organization
   */
  async createOrganization(data: CreateOrganizationRequest): Promise<Organization> {
    const formData = new FormData();

    // Add text fields
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && !(value instanceof File)) {
        formData.append(key, String(value));
      }
    });

    // Add file fields
    if (data.logo) {
      formData.append('logo', data.logo);
    }
    if (data.cover_photo) {
      formData.append('cover_photo', data.cover_photo);
    }

    const endpoint = getEndpointByType(data.organization_type);
    const response = await api.post<Organization>(
      endpoint,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  /**
   * Update organization
   */
  async updateOrganization(
    type: OrganizationType | string,
    id: string | number,
    data: UpdateOrganizationRequest
  ): Promise<Organization> {
    const formData = new FormData();
    const pluralType = getPluralType(type);

    // Add text fields
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && !(value instanceof File)) {
        formData.append(key, String(value));
      }
    });

    // Add file fields
    if (data.logo) {
      formData.append('logo', data.logo);
    }
    if (data.cover_photo) {
      formData.append('cover_photo', data.cover_photo);
    }

    const response = await api.patch<Organization>(
      API_ENDPOINTS.ORGANIZATION_DETAIL(pluralType, id),
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  /**
   * Delete organization
   */
  async deleteOrganization(type: OrganizationType | string, id: string | number): Promise<void> {
    const pluralType = getPluralType(type);
    await api.delete(API_ENDPOINTS.ORGANIZATION_DETAIL(pluralType, id));
  },

  /**
   * Join organization
   */
  async joinOrganization(type: OrganizationType | string, id: string | number): Promise<Membership> {
    const pluralType = getPluralType(type);
    const response = await api.post<Membership>(API_ENDPOINTS.ORGANIZATION_JOIN(pluralType, id));
    return response.data;
  },

  /**
   * Leave organization
   */
  async leaveOrganization(type: OrganizationType | string, id: string | number): Promise<void> {
    const pluralType = getPluralType(type);
    await api.post(API_ENDPOINTS.ORGANIZATION_LEAVE(pluralType, id));
  },

  /**
   * Get organization members
   */
  async getOrganizationMembers(type: OrganizationType | string, id: string | number): Promise<PaginatedResponse<Membership>> {
    const pluralType = getPluralType(type);
    const response = await api.get<PaginatedResponse<Membership>>(
      API_ENDPOINTS.ORGANIZATION_MEMBERS(pluralType, id)
    );
    return response.data;
  },

  /**
   * Get organization posts
   */
  async getOrganizationPosts(type: OrganizationType | string, id: string | number): Promise<PaginatedResponse<Post>> {
    const pluralType = getPluralType(type);
    const response = await api.get<PaginatedResponse<Post>>(
      API_ENDPOINTS.ORGANIZATION_POSTS(pluralType, id)
    );
    return response.data;
  },
};

export default organizationsService;
