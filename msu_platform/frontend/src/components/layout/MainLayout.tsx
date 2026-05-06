import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="py-8">
        <Outlet />
      </main>
      <footer className="border-t bg-white py-8">
        <div className="container mx-auto px-4 text-center text-gray-500">
          &copy; {new Date().getFullYear()} Midlands State University. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;
