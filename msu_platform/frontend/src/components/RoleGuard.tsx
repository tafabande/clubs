// RoleGuard - Route-level access control component
// Prevents unauthorized access to role-specific pages

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useRoles, DashboardType } from '@/hooks/useRoles';
import { useAuth } from '@/hooks/useAuth';

interface RoleGuardProps {
  children: React.ReactNode;
  allowedRoles: DashboardType[];
  fallback?: string;
}

export const RoleGuard: React.FC<RoleGuardProps> = ({
  children,
  allowedRoles,
  fallback = '/dashboard',
}) => {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { dashboard, isLoading: roleLoading } = useRoles();

  if (authLoading || roleLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-msu-dark">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-msu-gold/30 border-t-msu-gold rounded-full animate-spin" />
          <p className="text-white/60 text-sm">Verifying access...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!allowedRoles.includes(dashboard)) {
    return <Navigate to={fallback} replace />;
  }

  return <>{children}</>;
};

export default RoleGuard;
