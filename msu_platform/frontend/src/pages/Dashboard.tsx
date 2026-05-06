import React from 'react';
import { useAuth } from '@/context/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <div className="rounded-lg bg-white p-6 shadow-md">
        <h2 className="text-xl font-semibold mb-2">Welcome, {user?.first_name}!</h2>
        <p className="text-gray-600">This is your personal dashboard.</p>
      </div>
    </div>
  );
};

export default Dashboard;
