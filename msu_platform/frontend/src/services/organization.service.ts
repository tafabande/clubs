import api from '@/lib/axios';
import { Organization, PaginatedResponse } from '@/types';

export const organizationService = {
  async getOrganizations(params?: any): Promise<PaginatedResponse<Organization>> {
    const response = await api.get<PaginatedResponse<Organization>>('/organizations/', { params });
    return response.data;
  },

  async getOrganizationBySlug(slug: string): Promise<Organization> {
    const response = await api.get<Organization>(`/organizations/${slug}/`);
    return response.data;
  },

  async followOrganization(id: string): Promise<void> {
    await api.post(`/organizations/${id}/follow/`);
  },

  async unfollowOrganization(id: string): Promise<void> {
    await api.post(`/organizations/${id}/unfollow/`);
  },
};
