import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { organizationService } from '@/services/organization.service';

export const useOrganizations = (params?: any) => {
  return useQuery({
    queryKey: ['organizations', params],
    queryFn: () => organizationService.getOrganizations(params),
  });
};

export const useOrganization = (slug: string) => {
  return useQuery({
    queryKey: ['organization', slug],
    queryFn: () => organizationService.getOrganizationBySlug(slug),
    enabled: !!slug,
  });
};

export const useFollowOrganization = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => organizationService.followOrganization(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['organizations'] });
      queryClient.invalidateQueries({ queryKey: ['organization'] });
    },
  });
};
