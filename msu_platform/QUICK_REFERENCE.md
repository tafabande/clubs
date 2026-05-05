# MSU Platform - Quick Reference Card

Essential commands and endpoints for daily operations.

---

## 🚀 Quick Start

```bash
# Docker
docker-compose up -d

# Local
source venv/bin/activate && python manage.py runserver
```

---

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Django shell
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec db psql -U msu_user -d msu_platform

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Populate search
docker-compose exec web python manage.py populate_search_index

# Restart web
docker-compose restart web

# Backup database
docker-compose exec db pg_dump -U msu_user msu_platform > backup.sql
```

---

## 🛠️ Django Management Commands

```bash
# Migrations
python manage.py migrate                    # Run all migrations
python manage.py makemigrations             # Create new migrations
python manage.py showmigrations             # Show migration status

# User management
python manage.py createsuperuser            # Create admin user

# Search index
python manage.py populate_search_index      # Populate search index
python manage.py populate_search_index --clear  # Clear and repopulate

# Static files
python manage.py collectstatic              # Collect static files
python manage.py collectstatic --noinput    # Non-interactive

# Development
python manage.py runserver                  # Start dev server
python manage.py runserver 0.0.0.0:8000    # Accessible externally

# Shell access
python manage.py shell                      # Django shell
python manage.py dbshell                    # Database shell
```

---

## 🔐 API Endpoints

### Base URL
```
Development: http://localhost:8000/api
Production:  https://your-domain.com/api
```

### Authentication
```bash
# Register
POST /api/users/register/
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}

# Login
POST /api/users/login/
{
  "email": "user@example.com",
  "password": "securepassword"
}
# Returns: { "access": "...", "refresh": "..." }

# Get current user
GET /api/users/me/
Headers: Authorization: Bearer <access_token>

# Refresh token
POST /api/users/refresh/
{
  "refresh": "<refresh_token>"
}
```

### Organizations
```bash
# List clubs
GET /api/clubs/

# Create club
POST /api/clubs/
Headers: Authorization: Bearer <access_token>
{
  "name": "Tech Club",
  "description": "Technology enthusiasts",
  "category": "technology",
  "email": "tech@msu.ac.zw"
}

# Get club details
GET /api/clubs/{id}/

# Join club
POST /api/clubs/{id}/join/

# Leave club
POST /api/clubs/{id}/leave/

# Get members
GET /api/clubs/{id}/members/
```

### Feed (NEW)
```bash
# List posts
GET /api/posts/

# Create post
POST /api/posts/
{
  "content_type": 1,  # ContentType ID for Club
  "object_id": "club-uuid",
  "post_type": "announcement",
  "title": "Meeting Tomorrow",
  "content": "Don't forget our meeting!",
  "visibility": "public"
}

# Like post
POST /api/posts/{id}/like/

# Comment on post
POST /api/posts/{id}/comment/
{
  "content": "Great announcement!"
}

# Get comments
GET /api/posts/{id}/comments/

# Share post
POST /api/posts/{id}/share/
{
  "comment": "Check this out!"
}

# Get user feed
GET /api/feed/

# Generate feed
POST /api/feed/generate/

# Mark as read
POST /api/feed/{id}/mark_read/

# Unread count
GET /api/feed/unread_count/
```

### Search (NEW)
```bash
# Search organizations
GET /api/search/?q=tech&type=club

# Trending searches
GET /api/search/trending/

# Search suggestions
GET /api/search/suggestions/?q=te

# Get categories
GET /api/search/categories/?type=club
```

---

## 🗄️ Database

### PostgreSQL Commands
```bash
# Connect to database
psql -U msu_user -d msu_platform

# List tables
\dt

# Describe table
\d posts

# List indexes
\di

# Database size
SELECT pg_size_pretty(pg_database_size('msu_platform'));

# Table sizes
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::text))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::text) DESC;

# Vacuum database
VACUUM ANALYZE;

# Exit
\q
```

### Backup & Restore
```bash
# Backup
pg_dump -U msu_user msu_platform > backup_$(date +%Y%m%d).sql

# Restore
psql -U msu_user -d msu_platform < backup.sql

# Docker backup
docker-compose exec db pg_dump -U msu_user msu_platform > backup.sql

# Docker restore
docker-compose exec -T db psql -U msu_user msu_platform < backup.sql
```

---

## 📝 Logs

### View Logs
```bash
# Docker logs
docker-compose logs -f web            # Web service
docker-compose logs -f db             # Database
docker-compose logs -f nginx          # Nginx
docker-compose logs --tail=100 web    # Last 100 lines

# System logs (manual deployment)
sudo journalctl -u msu-platform -f    # Application
sudo tail -f /var/log/nginx/access.log  # Nginx access
sudo tail -f /var/log/nginx/error.log   # Nginx errors
sudo tail -f /var/log/postgresql/postgresql-15-main.log  # PostgreSQL
```

---

## 🔧 Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U msu_user -d msu_platform -c "SELECT 1;"
```

### Gunicorn Won't Start
```bash
# Check logs
sudo journalctl -u msu-platform -n 50

# Test manually
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

### Permission Errors
```bash
sudo chown -R msuapp:www-data /path/to/project
sudo chmod -R 755 /path/to/project
sudo chmod -R 775 media/
```

---

## 🔐 Security

### Generate Secret Key
```python
import secrets
print(secrets.token_urlsafe(50))
```

### Change Database Password
```sql
ALTER USER msu_user WITH PASSWORD 'new_strong_password';
```

### SSL Certificate (Let's Encrypt)
```bash
sudo certbot --nginx -d your-domain.com
sudo certbot renew --dry-run  # Test renewal
```

---

## 📊 Monitoring

### Check Service Status
```bash
# Docker
docker-compose ps

# Systemd
sudo systemctl status msu-platform
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis
```

### Resource Usage
```bash
# CPU and Memory
htop

# Disk space
df -h

# Database connections
psql -U msu_user -d msu_platform -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## 🎯 Common Tasks

### Add New Organization Type
1. Create model in `apps/organizations/models/`
2. Create serializer
3. Create viewset
4. Add to URLs
5. Run makemigrations
6. Run migrate
7. Update search index

### Add New Post Type
1. Add to POST_TYPES in `models/feed.py`
2. Run makemigrations
3. Run migrate

### Update Search Index
```bash
python manage.py populate_search_index --clear
```

### Create Test Data
```python
# Django shell
python manage.py shell

from apps.users.models import User
from apps.organizations.models import Club

# Create test user
user = User.objects.create_user(
    email='test@msu.ac.zw',
    password='testpass123',
    first_name='Test',
    last_name='User'
)

# Create test club
club = Club.objects.create(
    name='Test Club',
    description='A test club',
    category='academic',
    email='testclub@msu.ac.zw',
    created_by=user,
    is_approved=True
)
```

---

## 📞 Quick Links

- **Admin Panel**: http://localhost:8000/admin
- **API Root**: http://localhost:8000/api
- **Swagger Docs**: http://localhost:8000/api/docs (if configured)
- **Django Admin**: http://localhost:8000/admin

---

## 🆘 Emergency Commands

### Restart Everything
```bash
# Docker
docker-compose restart

# Systemd
sudo systemctl restart msu-platform nginx postgresql redis
```

### Emergency Database Backup
```bash
docker-compose exec db pg_dump -U msu_user msu_platform | gzip > emergency_backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Rollback Migration
```bash
python manage.py migrate organizations 0002_enable_rls
```

### Clear All Sessions
```bash
python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> Session.objects.all().delete()
```

---

**Last Updated:** May 5, 2026
**Version:** 2.0
