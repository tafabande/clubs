# Frontend Directory Structure

```
msu_platform/frontend/
├── public/
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── ui/                          # Reusable UI Components
│   │   │   ├── Avatar.tsx              # User avatar with fallback
│   │   │   ├── Badge.tsx               # Status badges (5 variants)
│   │   │   ├── Button.tsx              # Button (5 variants, 3 sizes)
│   │   │   ├── Card.tsx                # Card container with glassmorphism
│   │   │   ├── Input.tsx               # Form input with validation
│   │   │   ├── Modal.tsx               # Animated modal dialog
│   │   │   ├── Spinner.tsx             # Loading spinner (3 sizes)
│   │   │   └── index.ts                # UI exports
│   │   │
│   │   ├── layout/                      # Layout Components
│   │   │   ├── Footer.tsx              # Site footer
│   │   │   ├── Layout.tsx              # Main layout wrapper
│   │   │   ├── Navbar.tsx              # Navigation bar
│   │   │   ├── ProtectedRoute.tsx      # Auth route wrapper
│   │   │   └── index.ts                # Layout exports
│   │   │
│   │   └── features/                    # Feature Components
│   │       ├── LoginForm.tsx           # Login form with validation
│   │       ├── RegisterForm.tsx        # Registration form
│   │       ├── OrganizationCard.tsx    # Organization display card
│   │       ├── PostCard.tsx            # Post/feed item
│   │       └── index.ts                # Feature exports
│   │
│   ├── pages/                           # Route-level Pages
│   │   ├── Home.tsx                    # Landing page
│   │   ├── Login.tsx                   # Login page
│   │   ├── Register.tsx                # Registration page
│   │   ├── Dashboard.tsx               # User dashboard
│   │   ├── Organizations.tsx           # Browse organizations
│   │   ├── OrganizationDetail.tsx      # Single organization view
│   │   ├── Profile.tsx                 # User profile
│   │   └── NotFound.tsx                # 404 error page
│   │
│   ├── hooks/                           # Custom React Hooks
│   │   ├── useAuth.ts                  # Authentication hook
│   │   ├── useOrganizations.ts         # Organizations queries/mutations
│   │   ├── usePosts.ts                 # Posts queries/mutations
│   │   └── index.ts                    # Hook exports
│   │
│   ├── services/                        # API Service Layer
│   │   ├── api.ts                      # Axios instance with interceptors
│   │   ├── auth.service.ts             # Authentication API calls
│   │   ├── organizations.service.ts    # Organizations API calls
│   │   ├── posts.service.ts            # Posts API calls
│   │   └── index.ts                    # Service exports
│   │
│   ├── types/                           # TypeScript Definitions
│   │   ├── api.ts                      # API types (User, Org, Post, etc.)
│   │   └── index.ts                    # Type exports
│   │
│   ├── utils/                           # Utility Functions
│   │   ├── cn.ts                       # ClassName utility (clsx + tw-merge)
│   │   ├── constants.ts                # App constants & endpoints
│   │   └── queryClient.ts              # React Query configuration
│   │
│   ├── contexts/                        # React Contexts (future)
│   │   └── (reserved for global state)
│   │
│   ├── assets/                          # Static Assets
│   │   └── react.svg
│   │
│   ├── App.tsx                         # Main app component
│   ├── main.tsx                        # App entry point
│   ├── router.tsx                      # Route configuration
│   ├── index.css                       # Global styles
│   └── vite-env.d.ts                   # Vite type definitions
│
├── .env.example                         # Environment variables template
├── .env                                # Environment variables (gitignored)
├── index.html                          # HTML template
├── package.json                        # Dependencies
├── package-lock.json                   # Dependency lock file
├── tsconfig.json                       # TypeScript config
├── tsconfig.app.json                   # App TypeScript config
├── tsconfig.node.json                  # Node TypeScript config
├── vite.config.ts                      # Vite configuration
├── tailwind.config.js                  # Tailwind CSS config
├── postcss.config.js                   # PostCSS config
├── eslint.config.js                    # ESLint config
└── README.md                           # Documentation
```

## Component Counts

- **UI Components:** 7 files
- **Layout Components:** 4 files  
- **Feature Components:** 4 files
- **Pages:** 8 files
- **Custom Hooks:** 3 files
- **Services:** 4 files
- **Type Definitions:** 2 files
- **Utils:** 3 files

**Total TypeScript Files:** 35+ files
**Total Project Size:** 3,745 lines added

## Key Technologies

- React 18
- TypeScript
- Vite
- React Router v6
- TanStack Query (React Query)
- Axios
- Tailwind CSS
- Framer Motion
- date-fns
- Lucide React (icons)
