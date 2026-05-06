export * from './user';
export * from './auth';
export * from './organization';

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  message: string;
  code?: string;
  errors?: Record<string, string[]>;
}
