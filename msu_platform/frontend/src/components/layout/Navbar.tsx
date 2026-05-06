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
    <nav className="glass dark:glass-dark fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl px-8 py-4 z-50 flex items-center justify-between rounded-2xl transition-all duration-500">
      {/* Logo */}
      <Link to="/" className="flex items-center gap-2 group">
        <div className="w-10 h-10 bg-msu-gold rounded-xl flex items-center justify-center group-hover:rotate-12 transition-transform duration-300 shadow-lg shadow-msu-gold/20">
          <span className="text-msu-blue font-black text-xl">M</span>
        </div>
        <span className="text-2xl font-black tracking-tighter text-slate-900 dark:text-white">
          MSU<span className="text-msu-gold">HUB</span>
        </span>
      </Link>

      {/* Navigation Links */}
      <div className="hidden md:flex items-center gap-8">
        <Link to="/organizations" className="nav-link">
          Organizations
        </Link>
        {isAuthenticated && (
          <Link to="/dashboard" className="nav-link">
            Dashboard
          </Link>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-4">
        {isAuthenticated ? (
          <>
            <button className="p-2 hover:bg-slate-100 dark:hover:bg-white/10 rounded-xl transition-all active:scale-90 relative">
              <Bell size={20} className="text-slate-600 dark:text-slate-400" />
              <span className="absolute top-2 right-2 w-2 h-2 bg-msu-gold rounded-full ring-2 ring-white dark:ring-msu-dark" />
            </button>

            <Link to="/profile" className="hover:scale-110 active:scale-90 transition-all">
              <Avatar
                src={user?.profile_picture}
                alt={user?.username || 'User'}
                size="sm"
                fallback={user?.username?.[0]}
                className="ring-2 ring-msu-gold/20"
              />
            </Link>

            <Button variant="ghost" size="sm" onClick={handleLogout} className="hidden lg:flex">
              <LogOut size={16} />
              Logout
            </Button>
          </>
        ) : (
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" onClick={() => navigate('/login')}>
              Login
            </Button>
            <Button variant="gold" size="sm" onClick={() => navigate('/register')} className="shadow-msu-gold/30">
              Join Now
            </Button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
