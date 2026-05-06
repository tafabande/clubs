// React Router Configuration

import { createBrowserRouter, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './components/layout/ProtectedRoute';

// Pages
import HomePage from './pages/Home';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import DashboardPage from './pages/Dashboard';
import OrganizationsPage from './pages/Organizations';
import OrganizationDetailPage from './pages/OrganizationDetail';
import ProfilePage from './pages/Profile';
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
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    ),
  },
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
    path: '/404',
    element: <NotFoundPage />,
  },
  {
    path: '*',
    element: <Navigate to="/404" replace />,
  },
]);

export default router;
