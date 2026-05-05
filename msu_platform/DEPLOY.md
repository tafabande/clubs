# MSU Platform - Deployment Guide

Complete guide for deploying the MSU Platform to production.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Manual Deployment](#manual-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Post-Deployment Tasks](#post-deployment-tasks)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.11+**
- **PostgreSQL 15+** (recommended) or SQLite for development
- **Redis** (optional, for caching)
- **Docker & Docker Compose** (for Docker deployment)
- **Node.js 18+** (for frontend)
- **Git**

### Required Accounts

- Domain name (for production)
- Email service (SendGrid, AWS SES, etc.)
- Cloud hosting (AWS, DigitalOcean, etc.) - optional

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/msu-platform.git
cd msu-platform/msu_platform
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Populate Search Index

```bash
python manage.py populate_search_index
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

---

## Docker Deployment

The easiest way to deploy MSU Platform is using Docker Compose.

### 1. Install Docker

Follow instructions at https://docs.docker.com/get-docker/

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with production settings
```

**Important .env variables:**

```env
DEBUG=False
SECRET_KEY=your-secret-key-min-50-chars-random
DATABASE_URL=postgresql://msu_user:changeme123@db:5432/msu_platform
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_PASSWORD=strong-database-password
```

### 3. Build and Start Containers

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f web
```

### 4. Run Initial Setup

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Populate search index
docker-compose exec web python manage.py populate_search_index

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Verify Deployment

Visit `http://localhost` or your domain to see the application.

### Docker Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart [service_name]

# Run Django commands
docker-compose exec web python manage.py [command]

# Access Django shell
docker-compose exec web python manage.py shell

# Access database
docker-compose exec db psql -U msu_user -d msu_platform

# Backup database
docker-compose exec db pg_dump -U msu_user msu_platform > backup.sql

# Restore database
docker-compose exec -T db psql -U msu_user msu_platform < backup.sql
```

---

## Manual Deployment

For deployment without Docker (e.g., on shared hosting or VPS).

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx redis-server

# Install Node.js (for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Create Application User

```bash
sudo useradd -m -s /bin/bash msuapp
sudo su - msuapp
```

### 3. Clone and Setup Application

```bash
cd ~
git clone https://github.com/your-username/msu-platform.git
cd msu-platform/msu_platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with production settings
```

### 5. Setup Database

```bash
# Create PostgreSQL database and user
sudo -u postgres psql
postgres=# CREATE DATABASE msu_platform;
postgres=# CREATE USER msu_user WITH PASSWORD 'your_password';
postgres=# ALTER ROLE msu_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE msu_user SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE msu_user SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE msu_platform TO msu_user;
postgres=# \q
```

### 6. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py populate_search_index
```

### 7. Setup Gunicorn Service

Create `/etc/systemd/system/msu-platform.service`:

```ini
[Unit]
Description=MSU Platform Gunicorn Daemon
After=network.target

[Service]
User=msuapp
Group=www-data
WorkingDirectory=/home/msuapp/msu-platform/msu_platform
ExecStart=/home/msuapp/msu-platform/msu_platform/venv/bin/gunicorn \
          --access-logfile - \
          --workers 4 \
          --bind unix:/run/msu-platform.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start msu-platform
sudo systemctl enable msu-platform
sudo systemctl status msu-platform
```

### 8. Configure Nginx

Create `/etc/nginx/sites-available/msu-platform`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/msuapp/msu-platform/msu_platform/staticfiles/;
    }

    location /media/ {
        alias /home/msuapp/msu-platform/msu_platform/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/msu-platform.sock;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/msu-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Environment Configuration

### Critical Environment Variables

Create a `.env` file with these variables:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-change-this-to-random-50-chars
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_URL=postgresql://msu_user:password@localhost:5432/msu_platform

# Allowed Hosts
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@your-domain.com

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# File Storage (optional - for AWS S3)
USE_S3=False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

---

## Database Setup

### PostgreSQL Best Practices

1. **Enable Row-Level Security (automatic via migrations)**

```bash
python manage.py migrate organizations
```

2. **Create Database Backup Schedule**

```bash
# Create backup script
cat > /home/msuapp/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/msuapp/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U msu_user msu_platform > $BACKUP_DIR/backup_$TIMESTAMP.sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF

chmod +x /home/msuapp/backup-db.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /home/msuapp/backup-db.sh
```

3. **Performance Tuning**

Edit `/etc/postgresql/15/main/postgresql.conf`:

```conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free SSL)

1. **Install Certbot**

```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain Certificate**

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

3. **Auto-Renewal**

Certbot automatically sets up auto-renewal. Test it:

```bash
sudo certbot renew --dry-run
```

### Manual SSL Setup

If using a custom SSL certificate:

1. Place certificates in `/etc/nginx/ssl/`
2. Update nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # ... rest of config
}
```

---

## Post-Deployment Tasks

### 1. Create Initial Data

```bash
# Create superuser
python manage.py createsuperuser

# Populate search index
python manage.py populate_search_index

# Create sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 2. Test All Features

- [ ] User registration and login
- [ ] Organization creation (clubs, churches, teams, activities)
- [ ] Membership management
- [ ] Post creation and engagement (likes, comments, shares)
- [ ] Search functionality
- [ ] Feed generation
- [ ] Email verification
- [ ] Password reset

### 3. Configure Email Templates

Customize email templates in `apps/users/templates/emails/`:
- `verification_email.html`
- `password_reset_email.html`

### 4. Setup Monitoring

Consider using:
- **Sentry** for error tracking
- **New Relic** or **DataDog** for APM
- **UptimeRobot** for uptime monitoring

---

## Monitoring & Maintenance

### Regular Maintenance Tasks

**Daily:**
- Check application logs
- Monitor server resources
- Review error reports

**Weekly:**
- Update search index: `python manage.py populate_search_index`
- Review user feedback
- Check database size

**Monthly:**
- Update dependencies
- Review and optimize slow queries
- Backup rotation check

### Logs Location

```bash
# Application logs
docker-compose logs -f web  # Docker
sudo journalctl -u msu-platform -f  # Systemd

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Database Maintenance

```bash
# Vacuum database
psql -U msu_user -d msu_platform -c "VACUUM ANALYZE;"

# Check database size
psql -U msu_user -d msu_platform -c "SELECT pg_size_pretty(pg_database_size('msu_platform'));"

# List largest tables
psql -U msu_user -d msu_platform -c "
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
"
```

---

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

```bash
# Collect static files again
python manage.py collectstatic --noinput --clear

# Check nginx has read permissions
sudo chown -R www-data:www-data /home/msuapp/msu-platform/msu_platform/staticfiles/
```

#### 2. Database Connection Errors

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
psql -U msu_user -d msu_platform -c "SELECT 1;"

# Check DATABASE_URL in .env
```

#### 3. Permission Errors

```bash
# Fix ownership
sudo chown -R msuapp:www-data /home/msuapp/msu-platform/
sudo chmod -R 755 /home/msuapp/msu-platform/

# Fix media directory
sudo chown -R msuapp:www-data media/
sudo chmod -R 775 media/
```

#### 4. Gunicorn Won't Start

```bash
# Check logs
sudo journalctl -u msu-platform -n 50

# Test gunicorn manually
cd /home/msuapp/msu-platform/msu_platform
source venv/bin/activate
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

#### 5. Migrations Fail

```bash
# Check migration status
python manage.py showmigrations

# Fake a migration if needed (CAREFUL!)
python manage.py migrate organizations 0003_feed_and_search --fake

# Run migrations again
python manage.py migrate
```

### Performance Issues

```bash
# Check slow queries
tail -f /var/log/postgresql/postgresql-15-main.log | grep "duration"

# Analyze query performance
python manage.py shell
>>> from django.db import connection
>>> from django.db import reset_queries
>>> # Run your query
>>> print(connection.queries)

# Check server resources
htop
df -h
free -m
```

---

## Security Checklist

Before going to production:

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable SSL/HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Set up firewall (ufw)
- [ ] Disable root SSH login
- [ ] Set up fail2ban
- [ ] Configure database backups
- [ ] Enable security headers
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Review all environment variables

---

## Scaling Considerations

### Horizontal Scaling

1. **Database**: Use PostgreSQL with read replicas
2. **Application**: Run multiple Gunicorn workers behind load balancer
3. **Static Files**: Use CDN (CloudFront, CloudFlare)
4. **Media Files**: Use S3 or similar object storage
5. **Caching**: Use Redis for session/cache storage

### Load Balancer Setup

Use nginx or HAProxy to distribute traffic across multiple app servers.

---

## Support & Resources

- **Documentation**: https://github.com/your-username/msu-platform/wiki
- **Issues**: https://github.com/your-username/msu-platform/issues
- **Email**: support@your-domain.com

---

**Last Updated:** May 5, 2026
**Version:** 1.0
