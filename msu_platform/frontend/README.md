# MSU Platform Frontend

The official React TypeScript frontend for the Midlands State University social platform.

## Architecture Overview

This is a modern React application built with TypeScript, featuring a clean component-based architecture with proper separation of concerns.

### Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **TanStack Query (React Query)** - Server state management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **date-fns** - Date formatting
- **Lucide React** - Icon library

## Project Structure

```
src/
├── components/          # Reusable UI and feature components
│   ├── ui/             # Base UI components (Button, Card, Input, etc.)
│   ├── layout/         # Layout components (Navbar, Footer, Layout)
│   └── features/       # Domain-specific components (OrganizationCard, PostCard, Forms)
├── pages/              # Route-level page components
│   ├── Home.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── Organizations.tsx
│   ├── OrganizationDetail.tsx
│   ├── Profile.tsx
│   └── NotFound.tsx
├── hooks/              # Custom React hooks
│   ├── useAuth.ts      # Authentication hook
│   ├── useOrganizations.ts
│   └── usePosts.ts
├── services/           # API service layer
│   ├── api.ts          # Axios instance with interceptors
│   ├── auth.service.ts
│   ├── organizations.service.ts
│   └── posts.service.ts
├── types/              # TypeScript type definitions
│   ├── api.ts          # API response types
│   └── index.ts        # Type exports
├── utils/              # Utility functions
│   ├── constants.ts    # App constants
│   ├── queryClient.ts  # React Query configuration
│   └── cn.ts           # ClassName utility
├── contexts/           # React contexts (reserved for future use)
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── router.tsx         # Route configuration

```

## Key Features

### 1. Type-Safe API Integration

All API calls are fully typed with TypeScript interfaces matching the Django backend:

```typescript
// Example: Fetching organizations
const { data, isLoading } = useOrganizations({
  organization_type: 'club',
  search: 'debate',
});
```

### 2. Automatic Token Management

The API client automatically:
- Attaches JWT tokens to requests
- Refreshes expired tokens
- Redirects to login on authentication failure
- Handles network errors gracefully

### 3. Protected Routes

Routes are protected using the `ProtectedRoute` component:

```typescript
{
  path: '/dashboard',
  element: (
    <ProtectedRoute>
      <DashboardPage />
    </ProtectedRoute>
  ),
}
```

### 4. Infinite Scroll

Organizations and posts support infinite scrolling:

```typescript
const { data, hasNextPage, fetchNextPage } = useInfiniteOrganizations();
```

### 5. Optimistic Updates

Mutations use React Query's optimistic updates for better UX.

## Environment Variables

Create a `.env` file in the frontend directory:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_API_TIMEOUT=30000
VITE_APP_NAME=MSU Platform
VITE_APP_VERSION=3.0.0
VITE_ENABLE_DEBUG=true
```

## Development

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://127.0.0.1:8000`

### Installation

```bash
npm install --legacy-peer-deps
```

### Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Component Guidelines

### UI Components (`components/ui/`)

Reusable, generic UI components:

```typescript
import { Button, Card, Input } from '@/components/ui';

<Button variant="primary" size="lg">
  Click Me
</Button>
```

### Layout Components (`components/layout/`)

Page structure components:

```typescript
import { Layout } from '@/components/layout';

<Layout>
  <YourPageContent />
</Layout>
```

### Feature Components (`components/features/`)

Domain-specific, reusable components:

```typescript
import { OrganizationCard } from '@/components/features';

<OrganizationCard organization={org} />
```

## Custom Hooks

### useAuth

Manages authentication state:

```typescript
const { user, isAuthenticated, login, logout } = useAuth();
```

### useOrganizations

Fetches and manages organizations:

```typescript
const { data, isLoading, error } = useOrganizations({
  organization_type: 'club'
});
```

### usePosts

Fetches and manages posts/feed:

```typescript
const { data } = useInfinitePosts({ ordering: '-created_at' });
```

## Styling

### Tailwind CSS

The project uses Tailwind CSS with custom MSU theme colors:

```javascript
colors: {
  'msu-blue': '#003366',
  'msu-gold': '#FFD700',
  'msu-dark': '#0a0e1a',
}
```

### CSS Classes

Custom classes defined in `index.css`:

- `.glass` - Glassmorphism effect
- `.card` - Card container
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button

### Utility Function

Use the `cn()` utility to combine classes:

```typescript
import { cn } from '@/utils/cn';

className={cn('base-class', isActive && 'active-class', className)}
```

## API Integration

### Service Layer

All API calls go through service modules:

```typescript
// services/organizations.service.ts
export const organizationsService = {
  getOrganizations: (filters) => api.get('/orgs/', { params: filters }),
  getOrganization: (id) => api.get(`/orgs/${id}/`),
  joinOrganization: (id) => api.post(`/orgs/${id}/join/`),
  // ...
};
```

### React Query Integration

Services are wrapped in React Query hooks:

```typescript
export const useOrganization = (id: number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.ORGANIZATION, id],
    queryFn: () => organizationsService.getOrganization(id),
    enabled: !!id,
  });
};
```

## Path Aliases

The project uses TypeScript path aliases for cleaner imports:

```typescript
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks';
import { authService } from '@/services';
import type { User } from '@/types';
```

## Error Handling

Errors are handled at multiple levels:

1. **API Level**: Axios interceptors catch and format errors
2. **Query Level**: React Query error states
3. **Component Level**: Error boundaries and error states

```typescript
const { data, error, isLoading } = useOrganizations();

if (error) {
  return <ErrorMessage message={getErrorMessage(error)} />;
}
```

## Best Practices

1. **Always use TypeScript** - No `any` types
2. **Use custom hooks** - Don't call services directly in components
3. **Proper loading states** - Show spinners during async operations
4. **Error handling** - Always handle error states
5. **Accessibility** - Use semantic HTML and ARIA attributes
6. **Responsive design** - Use Tailwind's responsive utilities
7. **Code splitting** - Use React.lazy() for large components
8. **Memoization** - Use React.memo() for expensive components

## Future Enhancements

- [ ] Add React Hook Form for complex forms
- [ ] Add Zod for runtime validation
- [ ] Implement real-time updates with WebSockets
- [ ] Add toast notification system
- [ ] Implement theme switching (dark/light mode)
- [ ] Add i18n support
- [ ] Implement PWA features
- [ ] Add analytics integration

## Contributing

1. Follow the existing code structure
2. Use TypeScript strictly
3. Write meaningful commit messages
4. Test your changes before committing
5. Keep components small and focused
6. Document complex logic

## License

Copyright © 2026 MSU Platform. All rights reserved.
