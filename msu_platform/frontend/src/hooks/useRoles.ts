// Role-based access control hook
// Fetches user's role, permissions, and dashboard type from the backend

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/api';
import { QUERY_KEYS, API_ENDPOINTS } from '@/utils/constants';
import { useAuth } from './useAuth';

export type DashboardType = 'admin' | 'moderator' | 'org_leader' | 'user';

export interface RoleInfo {
  role: string;
  dashboard: DashboardType;
  is_org_leader: boolean;
  led_organizations: Array<{
    id: string;
    type: string | null;
    role: string;
  }>;
  permissions: string[];
}

export const useRoles = () => {
  const { isAuthenticated } = useAuth();

  const { data, isLoading, error } = useQuery<RoleInfo>({
    queryKey: [QUERY_KEYS.DASHBOARD_ROLE],
    queryFn: async () => {
      const res = await apiClient.get(API_ENDPOINTS.DASHBOARD_ROLE);
      return res.data;
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
    retry: 1,
  });

  const hasPermission = (codename: string): boolean => {
    if (!data) return false;
    if (data.role === 'system_admin') return true;
    return data.permissions.includes(codename);
  };

  return {
    roleInfo: data ?? null,
    dashboard: data?.dashboard ?? 'user',
    isAdmin: data?.role === 'system_admin',
    isModerator: data?.role === 'moderator' || data?.role === 'system_admin',
    isOrgLeader: data?.is_org_leader ?? false,
    ledOrganizations: data?.led_organizations ?? [],
    permissions: data?.permissions ?? [],
    hasPermission,
    isLoading,
    error,
  };
};

export default useRoles;
