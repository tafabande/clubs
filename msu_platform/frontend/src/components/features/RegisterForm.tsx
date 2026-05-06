// Register Form Component

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus } from 'lucide-react';
import { useAuth } from '@/hooks';
import { Button, Input } from '@/components/ui';
import { getErrorMessage } from '@/services';
import type { RegisterRequest } from '@/types';

export const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const { register, isRegistering, registerError } = useAuth();

  const [formData, setFormData] = useState<RegisterRequest>({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
  });

  const [confirmPassword, setConfirmPassword] = useState('');
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

    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
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

    if (formData.password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
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

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {registerError && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {getErrorMessage(registerError)}
        </div>
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
        />
      </div>

      <Input
        label="Username"
        name="username"
        type="text"
        value={formData.username}
        onChange={handleChange}
        error={errors.username}
        placeholder="johndoe"
        autoComplete="username"
        helperText="At least 3 characters"
      />

      <Input
        label="Email"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        error={errors.email}
        placeholder="john.doe@msu.ac.zw"
        autoComplete="email"
      />

      <Input
        label="Password"
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        error={errors.password}
        placeholder="At least 8 characters"
        autoComplete="new-password"
      />

      <Input
        label="Confirm Password"
        name="confirmPassword"
        type="password"
        value={confirmPassword}
        onChange={(e) => {
          setConfirmPassword(e.target.value);
          if (errors.confirmPassword) {
            setErrors((prev) => ({ ...prev, confirmPassword: '' }));
          }
        }}
        error={errors.confirmPassword}
        placeholder="Re-enter your password"
        autoComplete="new-password"
      />

      <Button type="submit" className="w-full" isLoading={isRegistering}>
        <UserPlus size={20} />
        Create Account
      </Button>

      <p className="text-center text-white/60 text-sm">
        Already have an account?{' '}
        <Link to="/login" className="text-msu-gold hover:underline">
          Login here
        </Link>
      </p>
    </form>
  );
};

export default RegisterForm;
