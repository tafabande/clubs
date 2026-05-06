// Organizations Service

import api from './api';
import { API_ENDPOINTS } from '@/utils/constants';
import type {
  Organization,
  PaginatedResponse,
  OrganizationFilters,
  CreateOrganizationRequest,
  UpdateOrganizationRequest,
  Membership,
  Post,
} from '@/types';

export const organizationsService = {
  /**
   * Get all organizations with filters
   */
  async getOrganizations(filters?: OrganizationFilters): Promise<PaginatedResponse<Organization>> {
    const response = await api.get<PaginatedResponse<Organization>>(
      API_ENDPOINTS.ORGANIZATIONS,
      { params: filters }
    );
    return response.data;
  },

  /**
   * Get organization by ID
   */
  async getOrganization(id: number): Promise<Organization> {
    const response = await api.get<Organization>(API_ENDPOINTS.ORGANIZATION_DETAIL(id));
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

    const response = await api.post<Organization>(
      API_ENDPOINTS.ORGANIZATIONS,
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
    id: number,
    data: UpdateOrganizationRequest
  ): Promise<Organization> {
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

    const response = await api.patch<Organization>(
      API_ENDPOINTS.ORGANIZATION_DETAIL(id),
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
  async deleteOrganization(id: number): Promise<void> {
    await api.delete(API_ENDPOINTS.ORGANIZATION_DETAIL(id));
  },

  /**
   * Join organization
   */
  async joinOrganization(id: number): Promise<Membership> {
    const response = await api.post<Membership>(API_ENDPOINTS.ORGANIZATION_JOIN(id));
    return response.data;
  },

  /**
   * Leave organization
   */
  async leaveOrganization(id: number): Promise<void> {
    await api.post(API_ENDPOINTS.ORGANIZATION_LEAVE(id));
  },

  /**
   * Get organization members
   */
  async getOrganizationMembers(id: number): Promise<PaginatedResponse<Membership>> {
    const response = await api.get<PaginatedResponse<Membership>>(
      API_ENDPOINTS.ORGANIZATION_MEMBERS(id)
    );
    return response.data;
  },

  /**
   * Get organization posts
   */
  async getOrganizationPosts(id: number): Promise<PaginatedResponse<Post>> {
    const response = await api.get<PaginatedResponse<Post>>(
      API_ENDPOINTS.ORGANIZATION_POSTS(id)
    );
    return response.data;
  },

  /**
   * Search organizations
   */
  async searchOrganizations(query: string): Promise<PaginatedResponse<Organization>> {
    const response = await api.get<PaginatedResponse<Organization>>(
      API_ENDPOINTS.ORGANIZATIONS,
      { params: { search: query } }
    );
    return response.data;
  },
};

export default organizationsService;
