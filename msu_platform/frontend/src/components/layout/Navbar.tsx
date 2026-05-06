import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bell, LogOut, User, Menu, X } from 'lucide-react';
import { useAuth } from '@/hooks';
import { Button, Avatar } from '@/components/ui';
import { motion, AnimatePresence } from 'framer-motion';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <>
      <nav className="glass dark:glass-dark fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl px-6 md:px-8 py-3 md:py-4 z-[60] flex items-center justify-between rounded-2xl transition-all duration-500 shadow-2xl">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <motion.div 
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.8, ease: "anticipate" }}
            className="w-10 h-10 bg-msu-gold rounded-xl flex items-center justify-center shadow-lg shadow-msu-gold/20"
          >
            <span className="text-msu-blue font-black text-xl">M</span>
          </motion.div>
          <span className="text-xl md:text-2xl font-black tracking-tighter text-slate-900 dark:text-white">
            MSU<span className="text-msu-gold">HUB</span>
          </span>
        </Link>

        {/* Navigation Links - Desktop */}
        <div className="hidden md:flex items-center gap-8">
          <Link to="/organizations" className="nav-link font-black text-sm uppercase tracking-widest">
            Organizations
          </Link>
          {isAuthenticated && (
            <Link to="/dashboard" className="nav-link font-black text-sm uppercase tracking-widest">
              Dashboard
            </Link>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2 md:gap-4">
          <div className="hidden md:flex items-center gap-4">
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

          {/* Mobile Menu Toggle */}
          <button 
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 glass dark:glass-dark rounded-xl text-msu-blue dark:text-msu-gold"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 z-50 md:hidden bg-slate-900/95 backdrop-blur-xl p-8 pt-24"
          >
            <div className="flex flex-col gap-8 items-center text-center">
              <Link 
                to="/organizations" 
                onClick={() => setIsMenuOpen(false)}
                className="text-4xl font-black text-white hover:text-msu-gold transition-colors"
              >
                Organizations
              </Link>
              {isAuthenticated ? (
                <>
                  <Link 
                    to="/dashboard" 
                    onClick={() => setIsMenuOpen(false)}
                    className="text-4xl font-black text-white hover:text-msu-gold transition-colors"
                  >
                    Dashboard
                  </Link>
                  <Link 
                    to="/profile" 
                    onClick={() => setIsMenuOpen(false)}
                    className="text-4xl font-black text-white hover:text-msu-gold transition-colors"
                  >
                    Profile
                  </Link>
                  <Button variant="gold" className="w-full text-xl py-6" onClick={handleLogout}>
                    Logout
                  </Button>
                </>
              ) : (
                <div className="flex flex-col gap-4 w-full">
                  <Button variant="ghost" className="text-white text-2xl py-6" onClick={() => navigate('/login')}>
                    Login
                  </Button>
                  <Button variant="gold" className="text-2xl py-6" onClick={() => navigate('/register')}>
                    Join MSU Hub
                  </Button>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Navbar;
