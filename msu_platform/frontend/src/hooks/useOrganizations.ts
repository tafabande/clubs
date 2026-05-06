// Organizations Hook

import { useQuery, useMutation, useQueryClient, useInfiniteQuery } from '@tanstack/react-query';
import { organizationsService } from '@/services';
import { QUERY_KEYS, DEFAULT_PAGE_SIZE } from '@/utils/constants';
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
        page: pageParam,
        page_size: DEFAULT_PAGE_SIZE,
      }),
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.next ? allPages.length + 1 : undefined;
    },
    initialPageParam: 1,
  });
};

/**
 * Get single organization by ID
 */
export const useOrganization = (id: number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, id],
    queryFn: () => organizationsService.getOrganization(id),
    enabled: !!id,
  });
};

/**
 * Get organization members
 */
export const useOrganizationMembers = (id: number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, id, 'members'],
    queryFn: () => organizationsService.getOrganizationMembers(id),
    enabled: !!id,
  });
};

/**
 * Get organization posts
 */
export const useOrganizationPosts = (id: number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, id, 'posts'],
    queryFn: () => organizationsService.getOrganizationPosts(id),
    enabled: !!id,
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
    mutationFn: ({ id, data }: { id: number; data: UpdateOrganizationRequest }) =>
      organizationsService.updateOrganization(id, data),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATION, variables.id] });
    },
  });
};

/**
 * Delete organization mutation
 */
export const useDeleteOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => organizationsService.deleteOrganization(id),
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
    mutationFn: (id: number) => organizationsService.joinOrganization(id),
    onSuccess: (data, id) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATION, id] });
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
    mutationFn: (id: number) => organizationsService.leaveOrganization(id),
    onSuccess: (data, id) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATION, id] });
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
    queryFn: () => organizationsService.searchOrganizations(query),
    enabled: query.length > 2, // Only search if query is at least 3 characters
  });
};
