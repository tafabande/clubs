// Organizations Hook

import { useQuery, useMutation, useQueryClient, useInfiniteQuery } from '@tanstack/react-query';
import { organizationsService } from '@/services';
import { QUERY_KEYS, DEFAULT_PAGE_SIZE } from '@/utils/constants';
import { OrganizationType } from '@/types';
import type {
  OrganizationFilters,
  CreateOrganizationRequest,
  UpdateOrganizationRequest,
} from '@/types';

/**
 * Get paginated organizations with filters
 */
export const useOrganizations = (filters?: OrganizationFilters) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATIONS, filters],
    queryFn: () => organizationsService.getOrganizations(filters),
  });
};

/**
 * Get infinite scroll organizations
 */
export const useInfiniteOrganizations = (filters?: OrganizationFilters) => {
  return useInfiniteQuery({
    queryKey: [QUERY_KEYS.ORGANIZATIONS, 'infinite', filters],
    queryFn: ({ pageParam = 1 }) =>
      organizationsService.getOrganizations({
        ...filters,
        page: pageParam as number,
        page_size: DEFAULT_PAGE_SIZE,
      }),
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.next ? allPages.length + 1 : undefined;
    },
    initialPageParam: 1,
  });
};

/**
 * Get single organization by type and ID
 */
export const useOrganization = (type: OrganizationType | string, id: string | number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, type, id],
    queryFn: () => organizationsService.getOrganization(type, id),
    enabled: !!id && !!type,
  });
};

/**
 * Get organization members
 */
export const useOrganizationMembers = (type: OrganizationType | string, id: string | number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, type, id, 'members'],
    queryFn: () => organizationsService.getOrganizationMembers(type, id),
    enabled: !!id && !!type,
  });
};

/**
 * Get organization posts
 */
export const useOrganizationPosts = (type: OrganizationType | string, id: string | number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, type, id, 'posts'],
    queryFn: () => organizationsService.getOrganizationPosts(type, id),
    enabled: !!id && !!type,
  });
};

/**
 * Create organization mutation
 */
export const useCreateOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateOrganizationRequest) =>
      organizationsService.createOrganization(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
    },
  });
};

/**
 * Update organization mutation
 */
export const useUpdateOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ type, id, data }: { type: OrganizationType | string; id: string | number; data: UpdateOrganizationRequest }) =>
      organizationsService.updateOrganization(type, id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATION, variables.type, variables.id] });
    },
  });
};

/**
 * Delete organization mutation
 */
export const useDeleteOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ type, id }: { type: OrganizationType | string; id: string | number }) => 
      organizationsService.deleteOrganization(type, id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
    },
  });
};

/**
 * Join organization mutation
 */
export const useJoinOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ type, id }: { type: OrganizationType | string; id: string | number }) => 
      organizationsService.joinOrganization(type, id),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATION, variables.type, variables.id] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
    },
  });
};

/**
 * Leave organization mutation
 */
export const useLeaveOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ type, id }: { type: OrganizationType | string; id: string | number }) => 
      organizationsService.leaveOrganization(type, id),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATION, variables.type, variables.id] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
    },
  });
};

/**
 * Search organizations
 */
export const useSearchOrganizations = (query: string) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATIONS, 'search', query],
    queryFn: () => organizationsService.getOrganizations({ search: query }),
    enabled: query.length > 2, // Only search if query is at least 3 characters
  });
};
