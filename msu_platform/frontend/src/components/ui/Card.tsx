// Card Component

import React from 'react';
import { cn } from '@/utils/cn';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  hover = false,
  className,
  ...props
}) => {
  return (
    <div
      className={cn(
        'card',
        hover && 'cursor-pointer hover:scale-[1.02] transition-transform',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
