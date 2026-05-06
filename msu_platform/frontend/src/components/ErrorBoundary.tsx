import { Component, ErrorInfo, ReactNode } from 'react';


interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="flex h-screen w-full flex-col items-center justify-center p-4 text-center">
            <h1 className="mb-4 text-4xl font-bold text-red-600">Something went wrong</h1>
            <p className="mb-6 text-gray-600">
              We're sorry for the inconvenience. Please try refreshing the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="rounded bg-blue-600 px-6 py-2 font-bold text-white transition hover:bg-blue-700"
            >
              Refresh Page
            </button>
            {import.meta.env.DEV && (
              <pre className="mt-8 max-w-full overflow-auto rounded bg-gray-100 p-4 text-left text-xs text-red-500">
                {this.state.error?.toString()}
              </pre>
            )}

          </div>
        )
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
