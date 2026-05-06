// Logger Utility for Frontend
// Provides structured logging for debugging and monitoring

const isDev = import.meta.env.DEV;

export const logger = {
  info: (message: string, ...args: any[]) => {
    if (isDev) {
      console.log(`%c[INFO] %c${message}`, 'color: #3b82f6; font-weight: bold;', 'color: inherit;', ...args);
    }
  },
  warn: (message: string, ...args: any[]) => {
    console.warn(`%c[WARN] %c${message}`, 'color: #f59e0b; font-weight: bold;', 'color: inherit;', ...args);
  },
  error: (message: string, ...args: any[]) => {
    console.error(`%c[ERROR] %c${message}`, 'color: #ef4444; font-weight: bold;', 'color: inherit;', ...args);
  },
  debug: (message: string, ...args: any[]) => {
    if (isDev) {
      console.debug(`%c[DEBUG] %c${message}`, 'color: #8b5cf6; font-weight: bold;', 'color: inherit;', ...args);
    }
  },
  // API specific logging
  api: {
    request: (config: any) => {
      if (isDev) {
        console.groupCollapsed(`%c[API REQ] %c${config.method?.toUpperCase()} ${config.url}`, 'color: #10b981; font-weight: bold;', 'color: inherit;');
        console.log('Params:', config.params);
        console.log('Data:', config.data);
        console.log('Headers:', config.headers);
        console.groupEnd();
      }
    },
    response: (response: any) => {
      if (isDev) {
        console.log(`%c[API RES] %c${response.status} ${response.config.url}`, 'color: #10b981; font-weight: bold;', 'color: inherit;', response.data);
      }
    },
    error: (error: any) => {
      console.group(`%c[API ERR] %c${error.response?.status || 'Network'} ${error.config?.url}`, 'color: #ef4444; font-weight: bold;', 'color: inherit;');
      console.error('Message:', error.message);
      console.error('Data:', error.response?.data);
      console.groupEnd();
    }
  }
};

export default logger;
