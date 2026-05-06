import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
// import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import { queryClient } from '@/lib/react-query';
import { AuthProvider } from '@/context/AuthContext';
import { AppProvider } from '@/context/AppContext';
import AppRoutes from '@/routes';

import ErrorBoundary from '@/components/ErrorBoundary';

const App: React.FC = () => {
  console.log('App.tsx: Rendering App component...');
  return (

    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AppProvider>
          <AuthProvider>
            <BrowserRouter>
              <AppRoutes />
            </BrowserRouter>
          </AuthProvider>
        </AppProvider>
        {/* <ReactQueryDevtools initialIsOpen={false} /> */}

      </QueryClientProvider>

    </ErrorBoundary>
  );
};

export default App;
