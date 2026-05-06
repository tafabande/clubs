// Authentication Service

import api from './api';
import { API_ENDPOINTS, STORAGE_KEYS } from '@/utils/constants';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
  TokenRefreshRequest,
  TokenRefreshResponse
} from '@/types';

export const authService = {
  /**
   * Login user with credentials
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(API_ENDPOINTS.LOGIN, credentials);

    // Store tokens and user data
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.refresh);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));

    return response.data;
  },

  /**
   * Register new user
   */
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(API_ENDPOINTS.REGISTER, userData);

    // Store tokens and user data
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.refresh);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));

    return response.data;
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      // Call logout endpoint (if backend supports it)
      await api.post(API_ENDPOINTS.LOGOUT);
    } catch (error) {
      // Continue with local logout even if API call fails
      console.error('Logout API call failed:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
    }
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);

    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const request: TokenRefreshRequest = { refresh: refreshToken };
    const response = await api.post<TokenRefreshResponse>(API_ENDPOINTS.REFRESH, request);

    // Update access token
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access);

    return response.data.access;
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
    const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    return !!token;
  },

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  },

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  },
};

export default authService;
