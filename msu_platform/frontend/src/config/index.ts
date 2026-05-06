export const CONFIG = {
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  APP_NAME: 'MSU Platform',
  STORAGE_KEYS: {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    USER: 'user_data',
  },
};
