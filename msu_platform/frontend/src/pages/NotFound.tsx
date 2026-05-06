// 404 Not Found Page Component

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home } from 'lucide-react';
import { Button, Card } from '@/components/ui';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <Card className="text-center max-w-md">
        <h1 className="text-9xl font-black text-msu-gold mb-4">404</h1>
        <h2 className="text-3xl font-bold mb-4">Page Not Found</h2>
        <p className="text-white/60 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Button onClick={() => navigate('/')}>
          <Home size={20} />
          Back to Home
        </Button>
      </Card>
    </div>
  );
};

export default NotFoundPage;
