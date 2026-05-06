// Spinner Component

import React from 'react';
import { cn } from '@/utils/cn';

interface SpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg';
}

const sizeStyles = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
};

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  className,
  ...props
}) => {
  return (
    <div className={cn('flex items-center justify-center', className)} {...props}>
      <div
        className={cn(
          'animate-spin rounded-full border-b-2 border-msu-gold',
          sizeStyles[size]
        )}
      />
    </div>
  );
};

export default Spinner;
