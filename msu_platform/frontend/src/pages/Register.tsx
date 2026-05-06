import React from 'react';
import { motion } from 'framer-motion';
import { RegisterForm } from '@/components/features';
import { Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

const Register: React.FC = () => {
  return (
    <div className="min-h-screen relative overflow-hidden bg-slate-950 flex items-center justify-center px-6 py-20">
      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <motion.div 
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
            x: [0, 100, 0],
            y: [0, 50, 0]
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute -top-24 -left-24 w-96 h-96 bg-msu-gold/10 rounded-full blur-[120px]" 
        />
        <motion.div 
          animate={{ 
            scale: [1, 1.3, 1],
            rotate: [0, -90, 0],
            x: [0, -100, 0],
            y: [0, -50, 0]
          }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          className="absolute -bottom-24 -right-24 w-96 h-96 bg-msu-blue/20 rounded-full blur-[120px]" 
        />
      </div>

      <div className="w-full max-w-5xl grid lg:grid-cols-2 gap-12 items-center relative z-10">
        {/* Left Side - Brand & Info */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          className="hidden lg:block space-y-8"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 glass-dark rounded-full text-msu-gold text-xs font-black uppercase tracking-widest">
            <Sparkles size={14} />
            Join the MSU Tribe
          </div>
          <h1 className="text-7xl font-black text-white leading-none tracking-tighter">
            START YOUR <br /> 
            <span className="text-gradient">JOURNEY</span> AT <br />
            <span className="text-msu-gold">MSU HUB</span>
          </h1>
          <p className="text-slate-400 text-xl max-w-md font-medium leading-relaxed">
            Create your profile, follow your favorite organizations, and stay updated with everything happening on campus.
          </p>
        </motion.div>

        {/* Right Side - Register Form */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full max-w-2xl mx-auto"
        >
          <div className="glass-dark p-8 md:p-10 rounded-[40px] border border-white/10 shadow-2xl relative overflow-hidden group">
            {/* Logo Mobile */}
            <div className="flex lg:hidden items-center justify-center gap-3 mb-10">
              <div className="w-12 h-12 bg-msu-gold rounded-2xl flex items-center justify-center shadow-lg shadow-msu-gold/20">
                <span className="text-msu-blue font-black text-2xl">M</span>
              </div>
              <span className="text-3xl font-black text-white tracking-tighter">
                MSU<span className="text-msu-gold">HUB</span>
              </span>
            </div>

            <div className="mb-8 text-center lg:text-left">
              <h2 className="text-4xl font-black text-white mb-2 tracking-tight">Create Account</h2>
              <p className="text-slate-500 font-medium">Be part of the most vibrant student community</p>
            </div>

            <RegisterForm />

            <div className="mt-8 pt-8 border-t border-white/5 text-center">
              <p className="text-slate-500 text-sm font-medium">
                Already have an account?{' '}
                <Link to="/login" className="text-msu-gold font-black hover:text-white transition-colors">
                  Sign In instead
                </Link>
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Register;
