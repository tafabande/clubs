// Central export point for all types

export * from './api';

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
// Context Types
// ============================================================================

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
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

// Re-export specific types for convenience
export type { User, Organization, Post, Event } from './api';
