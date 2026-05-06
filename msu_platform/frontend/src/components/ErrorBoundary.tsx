import { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

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
          <div className="min-h-screen w-full flex items-center justify-center p-6 bg-slate-50 dark:bg-msu-dark">
            <div className="glass dark:glass-dark max-w-2xl w-full rounded-3xl p-8 md:p-12 text-center animate-in">
              <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <AlertTriangle className="text-red-500 w-10 h-10" />
              </div>
              <h1 className="text-4xl md:text-5xl font-black mb-4 text-slate-900 dark:text-white tracking-tight">
                Oops! Something went wrong.
              </h1>
              <p className="text-lg text-slate-600 dark:text-white/60 mb-8 max-w-lg mx-auto">
                We've encountered an unexpected error while trying to load this page. Please try refreshing or come back later.
              </p>
              
              <button
                onClick={() => window.location.reload()}
                className="btn-primary inline-flex items-center gap-2 mx-auto"
              >
                <RefreshCw size={20} />
                Refresh Page
              </button>

              {import.meta.env.DEV && this.state.error && (
                <div className="mt-12 text-left bg-black/20 dark:bg-black/40 rounded-2xl p-6 overflow-x-auto border border-red-500/20">
                  <p className="text-red-400 font-mono text-sm font-bold mb-2">Error Details:</p>
                  <pre className="text-red-300/80 font-mono text-xs whitespace-pre-wrap">
                    {this.state.error.toString()}
                  </pre>
                </div>
              )}
            </div>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
