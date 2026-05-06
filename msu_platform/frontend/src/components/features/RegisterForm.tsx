// Register Form Component

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
    faculty: 'science',
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
    setErrors({});

    if (!validate()) return;

    try {
      await register(formData);
      navigate('/dashboard');
    } catch (error: any) {
      console.error('Registration failed:', error);
      if (error?.response?.data) {
        const apiErrors = error.response.data;
        const newErrors: Record<string, string> = {};
        
        Object.keys(apiErrors).forEach(key => {
          if (Array.isArray(apiErrors[key])) {
            newErrors[key] = apiErrors[key][0];
          } else if (typeof apiErrors[key] === 'string') {
            newErrors[key] = apiErrors[key];
          }
        });
        
        setErrors(prev => ({ ...prev, ...newErrors }));
      }
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
        <div className="space-y-2">
          <label className="text-xs font-black uppercase tracking-widest text-slate-400 ml-1">
            Faculty
          </label>
          <select
            name="faculty"
            value={formData.faculty}
            onChange={handleChange}
            className={`w-full h-11 px-4 rounded-xl border transition-all outline-none focus:ring-2 focus:ring-msu-gold/20 ${inputClass} ${errors.faculty ? 'border-red-500/50' : 'border-white/10'}`}
          >
            <option value="agriculture">Faculty of Agriculture</option>
            <option value="arts">Faculty of Arts</option>
            <option value="commerce">Faculty of Commerce</option>
            <option value="education">Faculty of Education</option>
            <option value="law">Faculty of Law</option>
            <option value="science">Faculty of Science</option>
            <option value="social_sciences">Faculty of Social Sciences</option>
          </select>
          {errors.faculty && <p className="text-[10px] text-red-400 font-bold uppercase ml-1">{errors.faculty}</p>}
        </div>

        <div className="space-y-2">
          <label className="text-xs font-black uppercase tracking-widest text-slate-400 ml-1">
            Year of Study
          </label>
          <select
            name="year_of_study"
            value={formData.year_of_study}
            onChange={handleChange}
            className={`w-full h-11 px-4 rounded-xl border transition-all outline-none focus:ring-2 focus:ring-msu-gold/20 ${inputClass} ${errors.year_of_study ? 'border-red-500/50' : 'border-white/10'}`}
          >
            {[1, 2, 3, 4, 5].map(year => (
              <option key={year} value={year}>Year {year}</option>
            ))}
          </select>
          {errors.year_of_study && <p className="text-[10px] text-red-400 font-bold uppercase ml-1">{errors.year_of_study}</p>}
        </div>
      </div>

      <div className="grid md:grid-cols-1 gap-4">
        <Input
          label="Department"
          name="department"
          type="text"
          value={formData.department}
          onChange={handleChange}
          error={errors.department}
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
