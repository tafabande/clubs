// React Query Client Configuration

import { QueryClient } from '@tanstack/react-query';
import { getErrorMessage } from '@/services/api';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
    },
    mutations: {
      retry: false,
      onError: (error) => {
        console.error('Mutation error:', getErrorMessage(error));
      },
    },
  },
});

export default queryClient;
