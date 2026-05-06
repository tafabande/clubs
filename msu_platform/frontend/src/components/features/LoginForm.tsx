// Login Form Component

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogIn } from 'lucide-react';
import { useAuth } from '@/hooks';
import { Button, Input } from '@/components/ui';
import { getErrorMessage } from '@/services';

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoggingIn, loginError } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email address';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    try {
      await login(formData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {loginError && (
        <motion.div 
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-black uppercase tracking-widest"
        >
          {getErrorMessage(loginError)}
        </motion.div>
      )}

      <div className="space-y-5">
        <Input
          label="Email Address"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="e.g. student@msu.edu"
          autoComplete="email"
          className="bg-white/5 border-white/10 text-white placeholder:text-slate-600 focus:border-msu-gold/50"
        />

        <Input
          label="Password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="••••••••"
          autoComplete="current-password"
          className="bg-white/5 border-white/10 text-white placeholder:text-slate-600 focus:border-msu-gold/50"
        />
      </div>

      <div className="flex items-center justify-between text-xs font-black uppercase tracking-widest">
        <label className="flex items-center gap-2 text-slate-500 cursor-pointer hover:text-msu-gold transition-colors">
          <input type="checkbox" className="w-4 h-4 rounded bg-white/5 border-white/10 checked:bg-msu-gold" />
          Remember Me
        </label>
        <Link to="/forgot-password" size="sm" className="text-msu-gold hover:text-white transition-colors">
          Forgot Password?
        </Link>
      </div>

      <Button 
        type="submit" 
        variant="gold" 
        className="w-full py-6 text-lg shadow-xl shadow-msu-gold/20 hover:shadow-msu-gold/40 transition-all active:scale-[0.98]" 
        isLoading={isLoggingIn}
      >
        <LogIn size={20} />
        Sign In
      </Button>
    </form>
  );
};

export default LoginForm;
