import { ApiError } from '@/types';

export const handleApiError = (error: any): ApiError => {
  if (error.response) {
    // Server responded with a status code outside the 2xx range
    const data = error.response.data;
    return {
      message: data.detail || data.message || 'An error occurred with the server.',
      code: data.code,
      errors: data.errors,
    };
  } else if (error.request) {
    // Request was made but no response was received
    return {
      message: 'No response from server. Please check your internet connection.',
    };
  } else {
    // Something happened in setting up the request
    return {
      message: error.message || 'An unexpected error occurred.',
    };
  }
};

export const logError = (error: any, context?: string) => {
  console.error(`[Error]${context ? ` in ${context}:` : ''}`, error);
  // Here you could send error to a monitoring service like Sentry
};
