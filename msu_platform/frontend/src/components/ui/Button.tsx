// Button Component

import React from 'react';
import { cn } from '@/utils/cn';
import type { ButtonVariant, ButtonSize } from '@/types';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  children: React.ReactNode;
}

const variantStyles: Record<ButtonVariant, string> = {
  primary: 'btn-primary',
  secondary: 'bg-slate-200 dark:bg-white/10 text-slate-900 dark:text-white hover:bg-slate-300 dark:hover:bg-white/20 active:scale-95',
  gold: 'btn-gold',
  outline: 'border-2 border-slate-200 dark:border-white/10 bg-transparent hover:border-msu-gold hover:text-msu-gold active:scale-95',
  ghost: 'bg-transparent hover:bg-slate-100 dark:hover:bg-white/5 active:scale-95',
  danger: 'bg-red-600 hover:bg-red-700 text-white active:scale-95',
};

const sizeStyles: Record<ButtonSize, string> = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg',
};

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className,
  children,
  disabled,
  ...props
}) => {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-xl font-bold transition-all duration-300',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current" />
      )}
      {children}
    </button>
  );
};

export default Button;
