// Register Form Component

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus } from 'lucide-react';
import { useAuth } from '@/hooks';
import { Button, Input } from '@/components/ui';
import { getErrorMessage } from '@/services';
import type { RegisterRequest } from '@/types';
import { motion } from 'framer-motion';

export const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const { register, isRegistering, registerError } = useAuth();

  const [formData, setFormData] = useState<RegisterRequest>({
    email: '',
    student_id: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    phone: '',
    faculty: '',
    department: '',
    year_of_study: 1,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ 
      ...prev, 
      [name]: name === 'year_of_study' ? parseInt(value) : value 
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.student_id.trim()) {
      newErrors.student_id = 'Student ID is required';
    }

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'First name is required';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Last name is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (formData.password !== formData.password_confirm) {
      newErrors.password_confirm = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    try {
      await register(formData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  const inputClass = "bg-white/5 border-white/10 text-white placeholder:text-slate-600 focus:border-msu-gold/50";

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {registerError && (
        <motion.div 
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-black uppercase tracking-widest"
        >
          {getErrorMessage(registerError)}
        </motion.div>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        <Input
          label="First Name"
          name="first_name"
          type="text"
          value={formData.first_name}
          onChange={handleChange}
          error={errors.first_name}
          placeholder="John"
          autoComplete="given-name"
          className={inputClass}
        />

        <Input
          label="Last Name"
          name="last_name"
          type="text"
          value={formData.last_name}
          onChange={handleChange}
          error={errors.last_name}
          placeholder="Doe"
          autoComplete="family-name"
          className={inputClass}
        />
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <Input
          label="Email Address"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="student@msu.ac.zw"
          autoComplete="email"
          className={inputClass}
        />

        <Input
          label="Student ID"
          name="student_id"
          type="text"
          value={formData.student_id}
          onChange={handleChange}
          error={errors.student_id}
          placeholder="R200000X"
          className={inputClass}
        />
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <Input
          label="Faculty"
          name="faculty"
          type="text"
          value={formData.faculty}
          onChange={handleChange}
          placeholder="e.g. Science & Tech"
          className={inputClass}
        />

        <Input
          label="Department"
          name="department"
          type="text"
          value={formData.department}
          onChange={handleChange}
          placeholder="e.g. Computer Science"
          className={inputClass}
        />
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <Input
          label="Password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="At least 8 characters"
          autoComplete="new-password"
          className={inputClass}
        />

        <Input
          label="Confirm Password"
          name="password_confirm"
          type="password"
          value={formData.password_confirm}
          onChange={handleChange}
          error={errors.password_confirm}
          placeholder="Re-enter password"
          autoComplete="new-password"
          className={inputClass}
        />
      </div>

      <Button 
        type="submit" 
        variant="gold" 
        className="w-full py-6 text-lg shadow-xl shadow-msu-gold/20 hover:shadow-msu-gold/40 transition-all active:scale-[0.98]" 
        isLoading={isRegistering}
      >
        <UserPlus size={20} />
        Create Account
      </Button>
    </form>
  );
};

export default RegisterForm;
