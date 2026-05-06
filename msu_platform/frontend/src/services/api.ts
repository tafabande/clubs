// Enhanced Axios API Client

import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { API_BASE_URL, API_TIMEOUT, STORAGE_KEYS } from '@/utils/constants';
import type { ApiError } from '@/types';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token to requests (handled by cookies now)
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Handle 401 errors - Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token - refresh endpoint will read refresh_token from cookie
        await axios.post(`${API_BASE_URL}/auth/refresh/`, {}, { withCredentials: true });

        // Retry the original request (it will now send the new access_token cookie)
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed - Clear user data from localStorage and redirect
        localStorage.removeItem(STORAGE_KEYS.USER);

        // Redirect to login
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Helper function to extract error message
export const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;

    // Check for detailed error message
    if (axiosError.response?.data) {
      const errorData = axiosError.response.data;

      // Handle different error response formats
      if (errorData.detail) {
        return errorData.detail;
      }

      if (errorData.message) {
        return errorData.message;
      }

      // Handle field-specific errors
      if (errorData.errors) {
        const firstError = Object.values(errorData.errors)[0];
        if (Array.isArray(firstError) && firstError.length > 0) {
          return firstError[0];
        }
      }
    }

    // Fallback to error message
    if (axiosError.message) {
      return axiosError.message;
    }
  }

  // Generic error
  if (error instanceof Error) {
    return error.message;
  }

  return 'An unexpected error occurred';
};

// Helper function to check if error is network error
export const isNetworkError = (error: unknown): boolean => {
  if (axios.isAxiosError(error)) {
    return !error.response && error.code === 'ERR_NETWORK';
  }
  return false;
};

export default api;
