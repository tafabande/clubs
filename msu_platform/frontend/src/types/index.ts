// Central export point for all types

export * from './api';

// Re-import from api for local use in this file
import type { User as ApiUser } from './api';
import type { RegisterRequest as ApiRegisterRequest } from './api';

// ============================================================================
// Component Props Types
// ============================================================================

export interface ChildrenProps {
  children: React.ReactNode;
}

export interface ClassNameProps {
  className?: string;
}

export interface BaseComponentProps extends ChildrenProps, ClassNameProps {}

// ============================================================================
// Form Types
// ============================================================================

export interface FormFieldError {
  message: string;
  type: string;
}

export interface FormErrors {
  [key: string]: FormFieldError | undefined;
}

// ============================================================================
// UI State Types
// ============================================================================

export type ButtonVariant = 'primary' | 'secondary' | 'gold' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

// ============================================================================
// Route Types
// ============================================================================

export interface RouteConfig {
  path: string;
  element: React.ReactNode;
  protected?: boolean;
  title?: string;
}

// ============================================================================
// Auth Context Types (used by AuthContext.tsx)
// ============================================================================

export interface AuthState {
  user: ApiUser | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  student_id: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

// ============================================================================
// Context Types
// ============================================================================

export interface AuthContextType {
  user: ApiUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: ApiRegisterRequest) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

export interface AppContextType {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
  toasts: Toast[];
}
