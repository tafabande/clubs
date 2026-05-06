// Login Page Component

import React from 'react';
import { motion } from 'framer-motion';
import { LoginForm } from '@/components/features';
import { Card } from '@/components/ui';

const LoginPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-20">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className="w-12 h-12 bg-msu-gold rounded-lg flex items-center justify-center">
            <span className="text-msu-blue font-black text-2xl">M</span>
          </div>
          <span className="text-3xl font-black tracking-tighter">
            MSU<span className="text-msu-gold">HUB</span>
          </span>
        </div>

        <Card>
          <h1 className="text-3xl font-black mb-2">Welcome Back</h1>
          <p className="text-white/60 mb-8">Login to access your dashboard</p>

          <LoginForm />
        </Card>
      </motion.div>
    </div>
  );
};

export default LoginPage;
