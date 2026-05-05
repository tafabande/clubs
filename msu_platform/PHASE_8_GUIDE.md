# Phase 8: React Frontend Implementation Guide

**Status:** 🔄 In Progress (Setup Complete)
**Overall Progress:** 90% (Phase 8 setup done, implementation in progress)

---

## 📋 Overview

Phase 8 creates a modern React frontend for the MSU Platform using Vite, TypeScript, and Tailwind CSS. The frontend provides a user-friendly interface for browsing organizations, managing memberships, and user authentication.

---

## ✅ Completed: Project Setup

### Files Created

1. **`frontend/package.json`** - Dependencies and scripts
2. **`frontend/vite.config.ts`** - Vite configuration with proxy
3. **`frontend/tsconfig.json`** - TypeScript configuration
4. **`frontend/tsconfig.node.json`** - Node TypeScript config
5. **`frontend/tailwind.config.js`** - Tailwind CSS configuration
6. **`frontend/postcss.config.js`** - PostCSS configuration
7. **`frontend/index.html`** - Main HTML entry point

### Directory Structure Created

```
frontend/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/          # Page components (routes)
│   ├── services/       # API services
│   ├── stores/         # Zustand state management
│   ├── types/          # TypeScript types
│   ├── utils/          # Utility functions
│   └── hooks/          # Custom React hooks
├── public/             # Static assets
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── index.html
```

### Dependencies Installed

**Core:**
- React 18.2.0
- React DOM 18.2.0
- React Router DOM 6.22.0

**State Management:**
- Zustand 4.5.0 (lightweight state management)
- TanStack React Query 5.22.0 (server state)

**Form Handling:**
- React Hook Form 7.50.0
- Zod 3.22.4 (validation)
- @hookform/resolvers 3.3.4

**HTTP & API:**
- Axios 1.6.7

**Styling:**
- Tailwind CSS 3.4.1
- PostCSS 8.4.35
- Autoprefixer 10.4.17

**Build Tools:**
- Vite 5.1.0
- TypeScript 5.2.2
- @vitejs/plugin-react 4.2.1

---

## 🎯 Implementation Roadmap

### 1. Core Setup (COMPLETE ✅)
- [x] Initialize Vite + React + TypeScript project
- [x] Configure Tailwind CSS
- [x] Set up project structure
- [x] Configure TypeScript paths (@/* aliases)
- [x] Set up Vite proxy for API requests

### 2. API Services (Next Priority)

**Files to Create:**

**`src/services/api.ts`** - Axios instance with interceptors
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('/api/auth/refresh/', {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

**`src/services/auth.ts`** - Authentication API
```typescript
import api from './api';

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/auth/login/', { email, password });
    return response.data;
  },

  async register(data: RegisterData) {
    const response = await api.post('/auth/register/', data);
    return response.data;
  },

  async logout() {
    const response = await api.post('/auth/logout/');
    return response.data;
  },

  async refreshToken(refreshToken: string) {
    const response = await api.post('/auth/refresh/', { refresh: refreshToken });
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me/');
    return response.data;
  },

  async verifyEmail(token: string) {
    const response = await api.get(`/auth/verify-email/${token}/`);
    return response.data;
  },

  async requestPasswordReset(email: string) {
    const response = await api.post('/auth/password-reset/', { email });
    return response.data;
  },

  async confirmPasswordReset(token: string, password: string) {
    const response = await api.post('/auth/password-reset-confirm/', { token, password });
    return response.data;
  },
};
```

**`src/services/organizations.ts`** - Organization APIs
```typescript
import api from './api';

export const organizationService = {
  // Clubs
  async getClubs(params?: SearchParams) {
    const response = await api.get('/clubs/', { params });
    return response.data;
  },

  async getClub(id: string) {
    const response = await api.get(`/clubs/${id}/`);
    return response.data;
  },

  async createClub(data: ClubData) {
    const response = await api.post('/clubs/', data);
    return response.data;
  },

  async updateClub(id: string, data: Partial<ClubData>) {
    const response = await api.patch(`/clubs/${id}/`, data);
    return response.data;
  },

  async joinClub(id: string) {
    const response = await api.post(`/clubs/${id}/join/`);
    return response.data;
  },

  async leaveClub(id: string) {
    const response = await api.post(`/clubs/${id}/leave/`);
    return response.data;
  },

  async getClubMembers(id: string) {
    const response = await api.get(`/clubs/${id}/members/`);
    return response.data;
  },

  async approveMember(clubId: string, membershipId: string) {
    const response = await api.post(`/clubs/${clubId}/approve_member/`, {
      membership_id: membershipId,
    });
    return response.data;
  },

  // Similar methods for churches, sports teams, activities
};
```

### 3. State Management

**`src/stores/authStore.ts`** - Authentication state
```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, accessToken: string, refreshToken: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      setAuth: (user, accessToken, refreshToken) =>
        set({ user, accessToken, refreshToken, isAuthenticated: true }),
      clearAuth: () =>
        set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

### 4. Authentication Pages

**Pages to Create:**
- `src/pages/Login.tsx` - Login page
- `src/pages/Register.tsx` - Registration page
- `src/pages/VerifyEmail.tsx` - Email verification page
- `src/pages/ForgotPassword.tsx` - Password reset request
- `src/pages/ResetPassword.tsx` - Password reset form

**Key Features:**
- Form validation with Zod
- Error handling
- Loading states
- Success messages
- Redirect after login
- Remember me option

### 5. Organization Pages

**Pages to Create:**
- `src/pages/Home.tsx` - Landing page
- `src/pages/OrganizationList.tsx` - Browse organizations
- `src/pages/OrganizationDetail.tsx` - Organization details
- `src/pages/Dashboard.tsx` - User dashboard
- `src/pages/CreateOrganization.tsx` - Create organization

**Features:**
- Search and filters
- Pagination
- Category filtering
- Sort options
- Membership status
- Join/leave buttons
- Member list
- Admin actions

### 6. Components

**Layout Components:**
- `src/components/Layout/Header.tsx` - Navigation header
- `src/components/Layout/Footer.tsx` - Footer
- `src/components/Layout/Sidebar.tsx` - Dashboard sidebar

**UI Components:**
- `src/components/UI/Button.tsx` - Button component
- `src/components/UI/Input.tsx` - Input field
- `src/components/UI/Card.tsx` - Card component
- `src/components/UI/Modal.tsx` - Modal dialog
- `src/components/UI/Badge.tsx` - Status badge
- `src/components/UI/Loading.tsx` - Loading spinner
- `src/components/UI/Alert.tsx` - Alert message

**Organization Components:**
- `src/components/Organization/OrganizationCard.tsx` - Organization card
- `src/components/Organization/OrganizationGrid.tsx` - Grid view
- `src/components/Organization/MemberList.tsx` - Member list
- `src/components/Organization/JoinButton.tsx` - Join button with logic

### 7. Routing

**`src/App.tsx`**
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
// ... other imports

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-email/:token" element={<VerifyEmail />} />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Organization routes */}
          <Route path="/clubs" element={<OrganizationList type="clubs" />} />
          <Route path="/clubs/:id" element={<OrganizationDetail type="clubs" />} />

          {/* 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

---

## 🎨 Design System

### Colors (Tailwind)
- **Primary:** Blue (#3b82f6) - MSU brand color
- **Secondary:** Gray shades for backgrounds
- **Success:** Green (#10b981)
- **Danger:** Red (#ef4444)
- **Warning:** Yellow (#f59e0b)

### Typography
- **Headings:** Font-bold, various sizes
- **Body:** Font-normal, text-gray-700
- **Labels:** Font-medium, text-sm

### Components
- **Buttons:** Rounded, shadow, hover effects
- **Cards:** White background, border, shadow
- **Inputs:** Border, focus ring, placeholder
- **Modals:** Backdrop, centered, animated

---

## 📱 Responsive Design

### Breakpoints
- **sm:** 640px (mobile)
- **md:** 768px (tablet)
- **lg:** 1024px (laptop)
- **xl:** 1280px (desktop)

### Mobile-First Approach
- Stack layouts vertically on mobile
- Collapse navigation to hamburger menu
- Touch-friendly button sizes (min 44x44px)
- Responsive images

---

## 🔒 Security Considerations

### JWT Token Management
- Store tokens in localStorage (with HttpOnly option on backend)
- Automatic token refresh
- Clear tokens on logout
- Redirect to login on auth failure

### Input Validation
- Client-side validation with Zod
- Sanitize user input
- XSS prevention (React escapes by default)
- CSRF token handling

### API Security
- Always use HTTPS in production
- Validate responses
- Handle errors gracefully
- Rate limiting awareness

---

## 🚀 Development Workflow

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

### 3. Build for Production
```bash
npm run build
```

### 4. Preview Production Build
```bash
npm run preview
```

---

## 📊 Next Implementation Steps

### Immediate (Complete Phase 8)
1. Create `src/main.tsx` and `src/App.tsx`
2. Implement authentication pages (Login, Register)
3. Create API services (auth, organizations)
4. Set up Zustand stores
5. Build organization browsing pages
6. Create reusable UI components
7. Implement routing and protected routes
8. Add responsive design
9. Test authentication flow
10. Test organization CRUD operations

### Testing
1. Manual testing of all pages
2. Test authentication flow
3. Test organization browsing
4. Test join/leave functionality
5. Test responsive design
6. Cross-browser testing

### Deployment Preparation
1. Build production bundle
2. Configure environment variables
3. Set up static file serving in Django
4. Configure CORS properly
5. Test production build

---

## 🎯 Success Criteria

Phase 8 is complete when:
- [ ] Users can register and login
- [ ] Users can verify their email
- [ ] Users can reset their password
- [ ] Users can browse all organization types
- [ ] Users can search and filter organizations
- [ ] Users can view organization details
- [ ] Users can join/leave organizations
- [ ] Members can see other members
- [ ] Creators can manage their organizations
- [ ] Admins can approve members
- [ ] Responsive design works on all devices
- [ ] All forms have validation
- [ ] Errors are handled gracefully
- [ ] Loading states are shown

---

## 📚 Additional Resources

### Documentation
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Router](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://github.com/pmndrs/zustand)

### Best Practices
- Component composition over inheritance
- Keep components small and focused
- Use TypeScript for type safety
- Extract reusable logic to custom hooks
- Optimize performance with React.memo and useMemo
- Handle loading and error states
- Provide accessibility (ARIA labels, keyboard navigation)

---

**Status:** Setup Complete, Implementation Ready
**Next Session:** Implement authentication pages and API services
**Estimated Remaining Time:** 2-3 days of development
