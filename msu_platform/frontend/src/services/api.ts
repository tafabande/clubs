// Enhanced Axios API Client

import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { API_BASE_URL, API_TIMEOUT, STORAGE_KEYS } from '@/utils/constants';
import { logger } from '@/utils/logger';
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

// Request interceptor - Add auth token to requests (fallback for cookies)
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    if (accessToken && config.headers) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    logger.api.request(config);
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors and token refresh
api.interceptors.response.use(
  (response) => {
    logger.api.response(response);
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Handle 401 errors - Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
        const response = await axios.post(`${API_BASE_URL}auth/refresh/`, 
          { refresh: refreshToken }, 
          { withCredentials: true }
        );

        const { access, refresh } = response.data;
        
        // Update local storage
        if (access) localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, access);
        if (refresh) localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh);

        // Retry the original request with new token
        if (access && originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access}`;
        }
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed - Clear user data from localStorage and redirect
        console.error('Token refresh failed, redirecting to login:', refreshError);
        localStorage.removeItem(STORAGE_KEYS.USER);
        localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
        localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);

        // Redirect to login
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }

        return Promise.reject(refreshError);
      }
    }

    logger.api.error(error);
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

      // Handle field-specific errors (DRF default format)
      if (typeof errorData === 'object' && errorData !== null) {
        // If it's a dictionary of field errors
        const entries = Object.entries(errorData);
        if (entries.length > 0) {
          const [field, messages] = entries[0];
          if (Array.isArray(messages) && messages.length > 0) {
            return `${field}: ${messages[0]}`;
          }
          if (typeof messages === 'string') {
            return messages;
          }
        }
      }

      // Handle nested errors object
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

export const apiClient = api;
export default api;
