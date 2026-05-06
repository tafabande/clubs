// React Router Configuration - with RBAC Dashboard Routes

import { createBrowserRouter, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import RoleGuard from './components/RoleGuard';

// Pages
import HomePage from './pages/Home';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import DashboardPage from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import ModeratorDashboard from './pages/ModeratorDashboard';
import OrgLeaderDashboard from './pages/OrgLeaderDashboard';
import OrganizationsPage from './pages/Organizations';
import OrganizationDetailPage from './pages/OrganizationDetail';
import ProfilePage from './pages/Profile';
import SettingsPage from './pages/Settings';
import NotFoundPage from './pages/NotFound';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },

  // ── Role-Based Dashboards ──────────────────────────────────────
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/admin',
    element: (
      <RoleGuard allowedRoles={['admin']}>
        <AdminDashboard />
      </RoleGuard>
    ),
  },
  {
    path: '/moderator',
    element: (
      <RoleGuard allowedRoles={['admin', 'moderator']}>
        <ModeratorDashboard />
      </RoleGuard>
    ),
  },
  {
    path: '/org-leader',
    element: (
      <RoleGuard allowedRoles={['admin', 'org_leader']}>
        <OrgLeaderDashboard />
      </RoleGuard>
    ),
  },

  // ── Standard Routes ────────────────────────────────────────────
  {
    path: '/organizations',
    element: <OrganizationsPage />,
  },
  {
    path: '/organizations/:type/:id',
    element: <OrganizationDetailPage />,
  },
  {
    path: '/profile',
    element: (
      <ProtectedRoute>
        <ProfilePage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/settings',
    element: (
      <ProtectedRoute>
        <SettingsPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/404',
    element: <NotFoundPage />,
  },
  {
    path: '*',
    element: <Navigate to="/404" replace />,
  },
]);

export default router;
