// Authentication Service

import api from './api';
import { API_ENDPOINTS, STORAGE_KEYS } from '@/utils/constants';
import { logger } from '@/utils/logger';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
  UpdateProfileRequest,
} from '@/types';

export const authService = {
  /**
   * Login user with credentials
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    logger.info('Attempting login...', credentials.email);
    const response = await api.post<AuthResponse>(API_ENDPOINTS.LOGIN, credentials);

    // Store user data and tokens
    logger.info('Login successful, storing user data');
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));
    if (response.data.access) localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access);
    if (response.data.refresh) localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.refresh);

    return response.data;
  },

  /**
   * Register new user
   */
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(API_ENDPOINTS.REGISTER, userData);

    // Store user data and tokens
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));
    if (response.data.access) localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access);
    if (response.data.refresh) localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.refresh);

    return response.data;
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    logger.info('Logging out user...');
    try {
      // Call logout endpoint (if backend supports it)
      await api.post(API_ENDPOINTS.LOGOUT);
      logger.info('Logout API call successful');
    } catch (error) {
      // Continue with local logout even if API call fails
      logger.error('Logout API call failed:', error);
    } finally {
      // Clear local user storage
      logger.info('Clearing local storage');
      localStorage.removeItem(STORAGE_KEYS.USER);
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    }
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<void> {
    // refresh endpoint will read refresh_token from cookie
    await api.post(API_ENDPOINTS.REFRESH, {});
  },

  /**
   * Update user profile
   */
  async updateProfile(data: UpdateProfileRequest): Promise<User> {
    const formData = new FormData();

    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (value instanceof File) {
          formData.append(key, value);
        } else {
          formData.append(key, String(value));
        }
      }
    });

    const response = await api.patch<User>(API_ENDPOINTS.ME, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // Update stored user data
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data));

    return response.data;
  },

  /**
   * Get current user from API
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>(API_ENDPOINTS.ME);

    // Update stored user data
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data));

    return response.data;
  },

  /**
   * Get stored user from localStorage
   */
  getStoredUser(): User | null {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);

    if (!userStr) {
      return null;
    }

    try {
      return JSON.parse(userStr) as User;
    } catch (error) {
      console.error('Failed to parse stored user:', error);
      return null;
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const user = localStorage.getItem(STORAGE_KEYS.USER);
    return !!user;
  },

  /**
   * Get tokens (obsolete with httpOnly cookies)
   */
  getAccessToken(): string | null {
    return null;
  },

  getRefreshToken(): string | null {
    return null;
  },
};

export default authService;
