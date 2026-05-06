import api from '@/lib/axios';
import { AuthResponse, LoginCredentials, RegisterCredentials, User } from '@/types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/users/login/', credentials);
    return response.data;
  },

  async register(credentials: RegisterCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/users/register/', credentials);
    return response.data;
  },

  async logout(): Promise<void> {
    const refresh = localStorage.getItem('refresh_token');
    if (refresh) {
      await api.post('/users/logout/', { refresh });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me/');
    return response.data;
  },
};
