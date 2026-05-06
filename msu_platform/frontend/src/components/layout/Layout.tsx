// Layout Component

import React from 'react';
import { Navbar } from './Navbar';
import { Footer } from './Footer';

interface LayoutProps {
  children: React.ReactNode;
  showFooter?: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, showFooter = true }) => {
  return (
    <div className="min-h-screen relative overflow-x-hidden bg-slate-50 dark:bg-msu-dark text-slate-900 dark:text-white transition-colors duration-500">
      {/* Background Ornaments */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-msu-blue/5 dark:bg-msu-blue/20 rounded-full blur-[120px]" />
        <div className="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-msu-gold/5 dark:bg-msu-gold/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-[10%] left-[20%] w-[25%] h-[25%] bg-blue-400/5 dark:bg-blue-400/10 rounded-full blur-[80px]" />
      </div>

      <Navbar />
      <main className="pt-24 relative z-0">
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  );
};

export default Layout;
