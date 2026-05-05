# MSU Campus Organizations Platform

Enterprise-grade Django platform for Midlands State University supporting clubs, churches, sports teams, and campus activities with comprehensive security (RLS, RBAC, JWT) and multi-device authentication.

## Features

- **Multi-Organization Support**: Clubs, Churches, Sports Teams, and Activities
- **Secure Authentication**: JWT with refresh tokens, multi-device sessions
- **Role-Based Access Control (RBAC)**: Fine-grained permissions system
- **Row-Level Security (RLS)**: PostgreSQL-based data access control
- **Audit Logging**: Complete audit trail of all actions
- **REST API**: Comprehensive API with Django REST Framework
- **React Frontend**: Modern SPA with authentication

## Tech Stack

- **Backend**: Django 5.0.6, Django REST Framework
- **Database**: PostgreSQL with RLS
- **Authentication**: JWT (simplejwt)
- **Security**: Argon2 password hashing, CORS, rate limiting
- **Frontend**: React (to be implemented)

## Project Structure

```
msu_platform/
├── config/                     # Django configuration
│   ├── settings/
│   │   ├── base.py            # Base settings
│   │   ├── development.py     # Development settings
│   │   ├── production.py      # Production settings
│   │   └── test.py            # Test settings
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI application
├── apps/
│   ├── users/                 # User management & authentication
│   ├── permissions/           # RBAC system
│   ├── organizations/         # Clubs, churches, sports, activities
│   ├── audit/                 # Audit logging
│   ├── api/                   # API endpoints
│   └── core/                  # Core utilities
├── scripts/
│   └── migrate_flask_data.py  # Data migration from Flask
└── manage.py

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip and virtualenv

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb msu_platform
createuser msu_user

# Grant privileges
psql -c "ALTER USER msu_user WITH PASSWORD 'secure_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE msu_platform TO msu_user;"

# Enable pgcrypto extension
psql msu_platform -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
```

### 3. Application Setup

```bash
# Clone repository
cd msu_platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and set your values

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed permissions and roles
python manage.py seed_permissions

# Create superuser
python manage.py createsuperuser

# Migrate Flask data (optional)
python scripts/migrate_flask_data.py

# Run development server
python manage.py runserver
```

### 4. Access the Application

- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/
- API Documentation: http://localhost:8000/api/docs/ (to be added)

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/logout-all/` - Logout from all devices
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/verify-email/<token>/` - Verify email
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset-confirm/` - Confirm password reset
- `GET /api/auth/me/` - Get current user

### Organizations (to be implemented)

- `/api/clubs/` - Club CRUD operations
- `/api/churches/` - Church CRUD operations
- `/api/sports-teams/` - Sports team CRUD operations
- `/api/activities/` - Activity CRUD operations

## Security Features

### JWT Authentication

- **Access Token**: 15 minutes lifetime
- **Refresh Token**: 7 days lifetime
- **Rotation**: Tokens rotate on refresh
- **Blacklisting**: Old tokens are blacklisted

### Password Security

- Argon2 hashing
- Minimum 8 characters
- Password validation (complexity, common passwords, etc.)

### Rate Limiting

- API: 500 requests/hour per user
- Auth: 10 requests/minute per user

### CORS

- Configurable allowed origins
- Credentials support for cookies

### Row-Level Security (RLS)

- PostgreSQL RLS policies enforce data access
- Users can only see approved organizations
- Admins can manage their own organizations
- Platform admins bypass RLS

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Seeding Data

```bash
python manage.py seed_permissions
python scripts/migrate_flask_data.py
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Configure production database
- [ ] Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure email backend
- [ ] Set up HTTPS
- [ ] Configure CORS allowed origins
- [ ] Set up static/media file storage
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Enable database backups

### Deploy with Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## License

MIT License

## Contributors

- System Team
