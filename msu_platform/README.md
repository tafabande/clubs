# MSU Platform

Enterprise-grade Django platform for managing Midlands State University (MSU) Gweru Campus organizations (clubs, churches, sports teams, activities) with social feed functionality and full-text search.

**Specifically designed for Midlands State University Gweru Campus, Zimbabwe**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

### Organization Management
- **4 Organization Types**: Clubs, Churches, Sports Teams, Activities
- **Membership Management**: Join, approve, assign roles
- **Approval Workflows**: Admin approval for new organizations
- **Profile Customization**: Logos, banners, descriptions
- **Capacity Limits**: Max members per organization

### Social Feed
- **Facebook-like Posts**: 6 post types (announcements, events, achievements, media, etc.)
- **Engagement**: Likes, comments (with nested replies), shares
- **Multiple Media**: Attach multiple images/videos per post
- **Visibility Control**: Public, members-only, or private posts
- **Pinned Posts**: Important updates stay at the top
- **Personalized Feeds**: Relevant content based on memberships

### Search & Discovery
- **Full-Text Search**: PostgreSQL-powered fast search
- **Weighted Results**: Name > description > category > tags
- **Category Filtering**: Search within specific organization types
- **Trending Searches**: See what others are looking for
- **Search Suggestions**: Auto-complete as you type

### Authentication & Security
- **JWT Authentication**: Secure token-based auth
- **Multi-Device Sessions**: Track and manage user sessions
- **Email Verification**: Verify user emails
- **Password Reset**: Secure password reset flow
- **Row-Level Security**: Database-level access control
- **RBAC**: 23+ permissions, 13+ roles
- **Argon2 Password Hashing**: Industry-standard security

### User Experience
- **Theme Support**: Light, dark, and system modes
- **Responsive Design**: Mobile, tablet, desktop, wide screens
- **Accessibility**: WCAG 2.1 Level AA compliance
- **API-First**: Complete REST API with 56+ endpoints

---

## 🚀 Quick Start

### One-Tap Launch (Windows - Easiest!) 🌟

**The absolute easiest way to run the platform on Windows:**

```batch
launch.bat
```

Just double-click `launch.bat` and it will:
- ✅ Scan system compatibility
- ✅ Install all prerequisites automatically
- ✅ Set up database and migrations
- ✅ Create admin user (admin@msu.ac.zw / admin123)
- ✅ Display localhost AND LAN links
- ✅ Show live status logs

**Perfect for:**
- First-time users
- Quick demos
- Non-technical users
- LAN/network access

**See [LAUNCH_GUIDE.md](LAUNCH_GUIDE.md) for complete documentation.**

---

### Docker (Recommended for Production)

```bash
# Clone the repository
git clone https://github.com/tafabande/clubs.git
cd clubs/msu_platform

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Populate search index
docker-compose exec web python manage.py populate_search_index

# (Optional) Populate with MSU Gweru sample data
docker-compose exec web python manage.py populate_sample_data

# Visit http://localhost
```

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate search index
python manage.py populate_search_index

# (Optional) Populate with MSU Gweru sample data
python manage.py populate_sample_data

# Run development server
python manage.py runserver

# Visit http://localhost:8000
```

---

## 📊 Architecture

### Backend Stack
- **Framework**: Django 5.0.6
- **API**: Django REST Framework 3.15.1
- **Auth**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 15+ (or SQLite for dev)
- **Caching**: Redis (optional)
- **Server**: Gunicorn + Nginx

### Frontend Stack
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.1.0
- **Language**: TypeScript 5.2.2
- **Styling**: Tailwind CSS 3.4.1
- **State Management**: Zustand 4.5.0
- **Data Fetching**: TanStack React Query 5.17.19
- **HTTP Client**: Axios 1.6.5

### Database Models
- **26 Total Models**:
  - 5 User models
  - 4 Permission models
  - 9 Organization models
  - 6 Feed models
  - 2 Search models

### API Endpoints
- **56+ Total Endpoints**:
  - 8 Authentication endpoints
  - 32 Organization endpoints
  - 12 Feed endpoints
  - 4 Search endpoints

---

## 📁 Project Structure

```
msu_platform/
├── apps/
│   ├── core/               # Core functionality, middleware
│   ├── users/              # User management, authentication
│   ├── permissions/        # RBAC system
│   └── organizations/      # Organizations, feed, search
│       ├── models/         # Database models
│       │   ├── base.py
│       │   ├── club.py
│       │   ├── church.py
│       │   ├── sports.py
│       │   ├── activity.py
│       │   ├── feed.py     # Social feed models
│       │   ├── search.py   # Search models
│       │   └── history.py
│       ├── views/          # API views
│       │   ├── club.py
│       │   ├── church.py
│       │   ├── sports.py
│       │   ├── activity.py
│       │   ├── feed.py     # Feed endpoints
│       │   └── search.py   # Search endpoints
│       ├── serializers/    # API serializers
│       │   ├── feed.py
│       │   └── search.py
│       ├── migrations/     # Database migrations
│       │   ├── 0001_initial.py
│       │   ├── 0002_enable_rls.py
│       │   ├── 0003_feed_and_search.py      # NEW
│       │   └── 0004_add_search_vector.py    # NEW
│       └── management/     # Management commands
│           └── commands/
│               └── populate_search_index.py  # NEW
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── frontend/               # React application
├── staticfiles/            # Collected static files
├── media/                  # User uploads
├── nginx/                  # Nginx configuration
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker services
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── DEPLOY.md               # Deployment guide
└── README.md               # This file
```

---

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example` for full list):

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-change-this
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/msu_platform

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECURE_SSL_REDIRECT=True

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-api-key
DEFAULT_FROM_EMAIL=noreply@your-domain.com
```

---

## 📚 API Documentation

### Authentication Endpoints

```
POST   /api/users/register/         # Register new user
POST   /api/users/login/            # Login
POST   /api/users/logout/           # Logout
POST   /api/users/logout-all/       # Logout all devices
POST   /api/users/refresh/          # Refresh access token
POST   /api/users/verify-email/     # Verify email
POST   /api/users/password-reset/   # Request password reset
GET    /api/users/me/               # Get current user
```

### Organization Endpoints

```
# Clubs
GET    /api/clubs/                  # List clubs
POST   /api/clubs/                  # Create club
GET    /api/clubs/{id}/             # Get club details
PUT    /api/clubs/{id}/             # Update club
DELETE /api/clubs/{id}/             # Delete club
POST   /api/clubs/{id}/join/        # Join club
POST   /api/clubs/{id}/leave/       # Leave club
GET    /api/clubs/{id}/members/     # List members
POST   /api/clubs/{id}/approve_member/ # Approve member

# Similar endpoints for churches, sports-teams, activities
```

### Feed Endpoints (NEW)

```
# Posts
GET    /api/posts/                  # List posts
POST   /api/posts/                  # Create post
GET    /api/posts/{id}/             # Get post
PUT    /api/posts/{id}/             # Update post
DELETE /api/posts/{id}/             # Delete post
POST   /api/posts/{id}/like/        # Like/unlike post
POST   /api/posts/{id}/comment/     # Add comment
GET    /api/posts/{id}/comments/    # List comments
POST   /api/posts/{id}/share/       # Share post
DELETE /api/posts/{id}/unshare/     # Remove share

# Feed
GET    /api/feed/                   # Get user's feed
POST   /api/feed/generate/          # Generate/refresh feed
POST   /api/feed/{id}/mark_read/    # Mark feed item as read
GET    /api/feed/unread_count/      # Get unread count
```

### Search Endpoints (NEW)

```
GET    /api/search/?q=query         # Search organizations
GET    /api/search/trending/        # Get trending searches
GET    /api/search/suggestions/?q=  # Get search suggestions
GET    /api/search/categories/      # Get available categories
```

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

---

## 🗄️ Database Migrations

### Run Migrations

```bash
# Check migration status
python manage.py showmigrations

# Run all migrations
python manage.py migrate

# Run specific app migrations
python manage.py migrate organizations

# Create new migration
python manage.py makemigrations
```

### Migration Files

- **0001_initial.py**: Base models (users, organizations)
- **0002_enable_rls.py**: Row-Level Security policies
- **0003_feed_and_search.py**: Social feed and search models (8 tables, 18 indexes)
- **0004_add_search_vector.py**: PostgreSQL full-text search (search_vector + GIN index)

For migration details, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest apps/organizations/tests/test_feed.py

# Run with coverage
pytest --cov=apps --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 📈 Performance

### Expected Performance

| Environment | Post Queries | Search Queries | Feed Queries |
|-------------|--------------|----------------|--------------|
| **SQLite (Dev)** | < 50ms | < 100ms (LIKE) | < 50ms |
| **PostgreSQL (Prod)** | < 10ms | < 20ms (full-text) | < 10ms |

### Optimizations

- **18 Database Indexes**: Fast lookups for common queries
- **PostgreSQL Full-Text Search**: GIN index for sub-20ms searches
- **Relevance Scoring**: Smart feed generation
- **Query Optimization**: Select/prefetch related data
- **Static File Caching**: 30-day cache for static assets

---

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Row-Level Security**: PostgreSQL RLS policies (30+)
- **RBAC**: Fine-grained permissions (23+)
- **Argon2 Password Hashing**: Industry-standard
- **CORS Configuration**: Controlled cross-origin requests
- **Rate Limiting**: Prevent abuse
- **CSRF Protection**: Built-in Django protection
- **SQL Injection Protection**: Django ORM
- **XSS Protection**: Template auto-escaping

---

## 📝 Management Commands

```bash
# Populate search index
python manage.py populate_search_index

# Clear and repopulate search index
python manage.py populate_search_index --clear

# Populate with MSU Gweru sample data (50 users, clubs, churches, teams, activities, posts)
python manage.py populate_sample_data

# Populate with 100 users and clear existing sample data
python manage.py populate_sample_data --clear --users 100

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Database shell
python manage.py dbshell

# Django shell
python manage.py shell
```

---

## 🚀 Deployment

For production deployment instructions, see [DEPLOY.md](DEPLOY.md).

### Quick Deploy with Docker

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Django Framework
- Django REST Framework
- PostgreSQL
- React
- All contributors and supporters

---

## 📞 Support

- **MSU Gweru Sample Data**: [MSU_GWERU_SAMPLE_DATA.md](MSU_GWERU_SAMPLE_DATA.md)
- **Documentation**: [PROJECT_STATUS.md](PROJECT_STATUS.md)
- **Deployment Guide**: [DEPLOY.md](DEPLOY.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Feature Guide**: [ENHANCED_FEATURES_GUIDE.md](ENHANCED_FEATURES_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/tafabande/clubs/issues)

---

**Built with ❤️ for Midlands State University Gweru Campus, Zimbabwe**

*Last Updated: May 5, 2026 | Version: 2.0*
