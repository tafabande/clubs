import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bell, LogOut, Menu, X, Inbox, CheckCircle2, Sun, Moon } from 'lucide-react';
import { useAuth, useAppContext } from '@/hooks';
import { Button, Avatar } from '@/components/ui';
import { motion, AnimatePresence } from 'framer-motion';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const { theme, setTheme } = useAppContext();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

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
      <nav className="glass dark:glass-dark fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl px-6 md:px-8 py-3 md:py-4 z-[60] flex items-center justify-between rounded-2xl transition-all duration-500 shadow-2xl border border-white/20 dark:border-white/10">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <motion.div 
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.8, ease: "anticipate" }}
            className="w-10 h-10 bg-msu-gold rounded-xl flex items-center justify-center shadow-lg shadow-msu-gold/20"
          >
            <span className="text-msu-blue font-black text-xl">M</span>
          </motion.div>
          <span className="text-xl md:text-2xl font-black tracking-tighter text-slate-900 dark:text-white flex items-center gap-1">
            MSU<span className="text-msu-gold">HUB</span>
            {isAuthenticated && user?.is_verified && (
              <CheckCircle2 size={16} className="text-blue-400 fill-blue-400/20" />
            )}
          </span>
        </Link>

        {/* Navigation Links - Desktop */}
        <div className="hidden md:flex items-center gap-8">
          <Link to="/organizations" className="nav-link font-black text-sm uppercase tracking-widest hover:text-msu-gold transition-colors">
            Societies
          </Link>
          {isAuthenticated && (
            <Link to="/dashboard" className="nav-link font-black text-sm uppercase tracking-widest hover:text-msu-gold transition-colors">
              Dashboard
            </Link>
          )}
        </div>

          <div className="flex items-center gap-2 md:gap-4">
            <button 
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="p-2 hover:bg-slate-100 dark:hover:bg-white/10 rounded-xl transition-all active:scale-90 group"
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? (
                <Sun size={20} className="text-msu-gold" />
              ) : (
                <Moon size={20} className="text-msu-blue" />
              )}
            </button>

            {isAuthenticated ? (
              <>
                <div className="relative">
                  <button 
                    onClick={() => setShowNotifications(!showNotifications)}
                    className="p-2 hover:bg-slate-100 dark:hover:bg-white/10 rounded-xl transition-all active:scale-90 relative group"
                  >
                    <Bell size={20} className="text-slate-600 dark:text-slate-400 group-hover:text-msu-blue dark:group-hover:text-white transition-colors" />
                    <span className="absolute top-2 right-2 w-2 h-2 bg-msu-gold rounded-full ring-2 ring-white dark:ring-msu-dark animate-pulse" />
                  </button>

                  <AnimatePresence>
                    {showNotifications && (
                      <motion.div 
                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                        className="absolute right-0 mt-4 w-80 glass-dark rounded-2xl shadow-2xl border border-white/10 overflow-hidden"
                      >
                        <div className="p-4 border-b border-white/10 flex justify-between items-center bg-white/5">
                          <h3 className="font-bold text-white">Notifications</h3>
                          <span className="text-xs bg-msu-gold text-msu-blue px-2 py-1 rounded-full font-bold">1 New</span>
                        </div>
                        <div className="max-h-80 overflow-y-auto">
                          <div className="p-4 hover:bg-white/5 transition-colors cursor-pointer border-l-4 border-msu-gold">
                            <p className="text-sm text-white font-medium mb-1">Welcome to MSU Hub!</p>
                            <p className="text-xs text-white/50">Explore societies and connect with peers.</p>
                            <p className="text-xs text-msu-gold mt-2">Just now</p>
                          </div>
                          <div className="p-8 text-center flex flex-col items-center justify-center text-white/40">
                            <Inbox size={32} className="mb-2 opacity-50" />
                            <p className="text-sm">You're all caught up</p>
                          </div>
                        </div>
                        <div className="p-3 border-t border-white/10 bg-black/20 text-center">
                          <button 
                            className="text-xs text-white/60 hover:text-white transition-colors"
                            onClick={() => setShowNotifications(false)}
                          >
                            Mark all as read
                          </button>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                <Link to="/profile" className="hover:scale-110 active:scale-90 transition-all">
                  <Avatar
                    src={user?.profile_picture}
                    alt={user?.first_name || 'User'}
                    size="sm"
                    fallback={user?.first_name?.[0]}
                    className="ring-2 ring-msu-gold/20"
                  />
                </Link>

                <Button variant="ghost" size="sm" onClick={handleLogout} className="hidden lg:flex hover:bg-red-500/10 hover:text-red-500 transition-colors">
                  <LogOut size={16} />
                  Log out
                </Button>
              </>
            ) : (
              <div className="flex items-center gap-3">
                <Button variant="ghost" size="sm" onClick={() => navigate('/login')} className="hover:bg-white/10">
                  Log in
                </Button>
                <Button variant="gold" size="sm" onClick={() => navigate('/register')} className="shadow-lg shadow-msu-gold/30 hover:shadow-msu-gold/50 transition-all">
                  Guest / Join Now
                </Button>
              </div>
            )}
          </div>

        {/* Mobile Menu Toggle */}
        <button 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="md:hidden p-2 glass dark:glass-dark rounded-xl text-msu-blue dark:text-msu-gold hover:bg-white/10 transition-colors"
        >
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </nav>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 z-50 md:hidden bg-slate-900/95 backdrop-blur-xl p-8 pt-28 overflow-y-auto"
          >
            <div className="flex flex-col gap-6 items-center text-center">
              <Link 
                to="/organizations" 
                onClick={() => setIsMenuOpen(false)}
                className="text-3xl font-black text-white hover:text-msu-gold transition-colors p-4 w-full rounded-2xl hover:bg-white/5"
              >
                Societies
              </Link>
              {isAuthenticated ? (
                <>
                  <Link 
                    to="/dashboard" 
                    onClick={() => setIsMenuOpen(false)}
                    className="text-3xl font-black text-white hover:text-msu-gold transition-colors p-4 w-full rounded-2xl hover:bg-white/5"
                  >
                    Dashboard
                  </Link>
                  <Link 
                    to="/profile" 
                    onClick={() => setIsMenuOpen(false)}
                    className="text-3xl font-black text-white hover:text-msu-gold transition-colors p-4 w-full rounded-2xl hover:bg-white/5"
                  >
                    Profile
                  </Link>
                  <Button variant="gold" className="w-full text-xl py-6 mt-4 shadow-lg shadow-msu-gold/20" onClick={handleLogout}>
                    Log out
                  </Button>
                </>
              ) : (
                <div className="flex flex-col gap-4 w-full mt-4">
                  <Button variant="ghost" className="text-white text-xl py-6 bg-white/5 hover:bg-white/10" onClick={() => { setIsMenuOpen(false); navigate('/login'); }}>
                    Log in
                  </Button>
                  <Button variant="gold" className="text-xl py-6 shadow-lg shadow-msu-gold/30" onClick={() => { setIsMenuOpen(false); navigate('/register'); }}>
                    Join MSU Hub
                  </Button>
                </div>
              )}
              
              <button 
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className="mt-8 flex items-center gap-3 text-white/60 hover:text-white transition-colors"
              >
                {theme === 'dark' ? <Sun size={24} /> : <Moon size={24} />}
                <span className="text-lg font-bold">Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Navbar;
