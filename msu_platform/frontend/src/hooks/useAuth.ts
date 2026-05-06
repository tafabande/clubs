// Authentication Hook

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { authService } from '@/services';
import { QUERY_KEYS } from '@/utils/constants';
import type { LoginRequest, RegisterRequest, UpdateProfileRequest } from '@/types';

export const useAuth = () => {
  const queryClient = useQueryClient();

  // Get current user query
  const {
    data: user,
    isLoading,
    isFetching,
    error,
  } = useQuery({
    queryKey: [QUERY_KEYS.ME],
    queryFn: () => authService.getCurrentUser(),
    enabled: authService.isAuthenticated(),
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const isUserAuthenticated = !!user || authService.isAuthenticated();

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: (credentials: LoginRequest) => authService.login(credentials),
    onSuccess: (data) => {
      // Immediate update to cache
      queryClient.setQueryData([QUERY_KEYS.ME], data.user);
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.ORGANIZATIONS] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POSTS] });
    },
  });

  // Register mutation
  const registerMutation = useMutation({
    mutationFn: (userData: RegisterRequest) => authService.register(userData),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.ME], data.user);
    },
  });

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      queryClient.clear();
      queryClient.setQueryData([QUERY_KEYS.ME], null);
    },
  });

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: (data: UpdateProfileRequest) => authService.updateProfile(data),
    onSuccess: (updatedUser) => {
      queryClient.setQueryData([QUERY_KEYS.ME], updatedUser);
    },
  });

  return {
    user: user ?? authService.getStoredUser() ?? null,
    isLoading: isLoading && authService.isAuthenticated() && !user,
    isAuthenticated: isUserAuthenticated,
    isFetching,
    error,
    login: loginMutation.mutateAsync,
    register: registerMutation.mutateAsync,
    logout: logoutMutation.mutateAsync,
    updateProfile: updateProfileMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
    isUpdatingProfile: updateProfileMutation.isPending,
    loginError: loginMutation.error,
    registerError: registerMutation.error,
    updateProfileError: updateProfileMutation.error,
  };
};

export default useAuth;
