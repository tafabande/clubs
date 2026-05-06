// Navbar Component

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bell, LogOut, User } from 'lucide-react';
import { useAuth } from '@/hooks';
import { Button, Avatar } from '@/components/ui';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="glass fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl px-8 py-4 z-50 flex items-center justify-between">
      {/* Logo */}
      <Link to="/" className="flex items-center gap-2">
        <div className="w-10 h-10 bg-msu-gold rounded-lg flex items-center justify-center">
          <span className="text-msu-blue font-black text-xl">M</span>
        </div>
        <span className="text-2xl font-black tracking-tighter">
          MSU<span className="text-msu-gold">HUB</span>
        </span>
      </Link>

      {/* Navigation Links */}
      <div className="hidden md:flex items-center gap-8">
        <Link to="/organizations" className="hover:text-msu-gold transition-colors">
          Organizations
        </Link>
        {isAuthenticated && (
          <>
            <Link to="/dashboard" className="hover:text-msu-gold transition-colors">
              Dashboard
            </Link>
          </>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-4">
        {isAuthenticated ? (
          <>
            <button className="p-2 hover:bg-white/10 rounded-lg transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-1 right-1 w-2 h-2 bg-msu-gold rounded-full" />
            </button>

            <Link to="/profile" className="hover:opacity-80 transition-opacity">
              <Avatar
                src={user?.profile_picture}
                alt={user?.username || 'User'}
                size="sm"
                fallback={user?.username?.[0]}
              />
            </Link>

            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut size={16} />
              Logout
            </Button>
          </>
        ) : (
          <>
            <Button variant="secondary" size="sm" onClick={() => navigate('/login')}>
              Login
            </Button>
            <Button variant="primary" size="sm" onClick={() => navigate('/register')}>
              Join Now
            </Button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
