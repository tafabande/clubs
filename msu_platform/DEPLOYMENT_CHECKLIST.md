# MSU Platform - Deployment Checklist ✅

Use this checklist to ensure a smooth deployment.

---

## Pre-Deployment Checklist

### 1. Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Set `DEBUG=False`
- [ ] Generate and set strong `SECRET_KEY` (50+ characters)
- [ ] Configure `DATABASE_URL` for PostgreSQL
- [ ] Set `ALLOWED_HOSTS` with your domain(s)
- [ ] Configure email backend (SMTP settings)
- [ ] Set `SECURE_SSL_REDIRECT=True` for production

### 2. Database Setup
- [ ] PostgreSQL 15+ installed and running
- [ ] Database created: `CREATE DATABASE msu_platform;`
- [ ] Database user created with strong password
- [ ] User granted all privileges on database
- [ ] Database connection tested

### 3. Application Setup
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Static files collected: `python manage.py collectstatic`

### 4. Database Migrations
- [ ] Check migration status: `python manage.py showmigrations`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Verify all migrations applied
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Populate search index: `python manage.py populate_search_index`

### 5. Web Server Configuration
- [ ] Gunicorn installed and configured
- [ ] Systemd service file created (manual deployment)
- [ ] Nginx installed and configured
- [ ] Nginx site configuration created
- [ ] Static files directory permissions set
- [ ] Media files directory permissions set

### 6. SSL/HTTPS Setup
- [ ] Domain DNS configured
- [ ] SSL certificate obtained (Let's Encrypt recommended)
- [ ] Nginx SSL configuration updated
- [ ] HTTPS redirect enabled
- [ ] Security headers configured

### 7. Security Review
- [ ] SECRET_KEY changed from default
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Database password is strong
- [ ] Firewall configured (ufw or similar)
- [ ] SSH key-based authentication only
- [ ] fail2ban installed and configured
- [ ] Regular backups scheduled

### 8. Testing
- [ ] Admin panel accessible: `/admin`
- [ ] API root accessible: `/api`
- [ ] User registration works
- [ ] User login works
- [ ] Email verification works
- [ ] Password reset works
- [ ] Organization creation works
- [ ] Membership management works
- [ ] Post creation works
- [ ] Like/comment/share works
- [ ] Feed generation works
- [ ] Search functionality works

### 9. Monitoring & Logging
- [ ] Application logs configured
- [ ] Nginx access logs reviewed
- [ ] Nginx error logs reviewed
- [ ] PostgreSQL logs configured
- [ ] Error tracking setup (Sentry optional)
- [ ] Uptime monitoring setup (optional)

### 10. Backup Strategy
- [ ] Database backup script created
- [ ] Cron job for daily backups configured
- [ ] Backup retention policy set (7-30 days)
- [ ] Backup restoration tested
- [ ] Media files backup configured

---

## Docker Deployment Checklist

### 1. Pre-Deployment
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] `.env` file configured
- [ ] `DB_PASSWORD` set in `.env`
- [ ] `SECRET_KEY` set in `.env`
- [ ] `ALLOWED_HOSTS` set in `.env`

### 2. Build & Deploy
- [ ] Build images: `docker-compose build`
- [ ] Start services: `docker-compose up -d`
- [ ] Check service status: `docker-compose ps`
- [ ] View logs: `docker-compose logs -f`

### 3. Initial Setup
- [ ] Run migrations: `docker-compose exec web python manage.py migrate`
- [ ] Create superuser: `docker-compose exec web python manage.py createsuperuser`
- [ ] Populate search: `docker-compose exec web python manage.py populate_search_index`
- [ ] Collect static: `docker-compose exec web python manage.py collectstatic`

### 4. Verification
- [ ] Database service healthy
- [ ] Redis service healthy
- [ ] Web service healthy
- [ ] Nginx service healthy
- [ ] Application accessible via browser
- [ ] Admin panel accessible
- [ ] API endpoints working

### 5. SSL Setup (Production)
- [ ] Update nginx config for HTTPS
- [ ] Mount SSL certificates
- [ ] Restart nginx: `docker-compose restart nginx`
- [ ] Test HTTPS access

---

## Post-Deployment Checklist

### 1. Immediate Tasks (Day 1)
- [ ] Verify all services running
- [ ] Check application logs for errors
- [ ] Test all critical user flows
- [ ] Monitor server resources (CPU, memory, disk)
- [ ] Set up alerts for service downtime

### 2. First Week
- [ ] Review error logs daily
- [ ] Monitor database performance
- [ ] Check disk space usage
- [ ] Review user feedback
- [ ] Optimize slow queries (if any)

### 3. Ongoing Maintenance
- [ ] Weekly: Update search index
- [ ] Weekly: Review logs and errors
- [ ] Monthly: Security updates
- [ ] Monthly: Dependency updates
- [ ] Quarterly: Performance review
- [ ] Quarterly: Security audit

---

## Performance Optimization Checklist

### Database
- [ ] Indexes reviewed and optimized
- [ ] Query performance analyzed
- [ ] Connection pooling configured
- [ ] Database vacuumed regularly
- [ ] Statistics up to date

### Application
- [ ] Static files served via CDN (optional)
- [ ] Media files served via CDN (optional)
- [ ] Caching enabled (Redis)
- [ ] Gunicorn workers optimized
- [ ] Query count minimized (select_related, prefetch_related)

### Web Server
- [ ] Gzip compression enabled
- [ ] Static file caching configured
- [ ] Browser caching headers set
- [ ] Connection keep-alive enabled

---

## Troubleshooting Guide

### Service Won't Start
1. Check logs: `docker-compose logs` or `journalctl -u msu-platform`
2. Verify environment variables in `.env`
3. Check database connection
4. Verify port availability

### Database Connection Errors
1. Check PostgreSQL is running
2. Verify DATABASE_URL in `.env`
3. Test connection manually: `psql -U msu_user -d msu_platform`
4. Check firewall rules

### Static Files Not Loading
1. Run: `python manage.py collectstatic --noinput`
2. Check nginx static files configuration
3. Verify file permissions
4. Clear browser cache

### 502 Bad Gateway
1. Check Gunicorn is running
2. Verify socket file permissions
3. Check nginx configuration
4. Review Gunicorn logs

---

## Emergency Procedures

### Application Crash
1. Check logs immediately
2. Restart service: `docker-compose restart web` or `systemctl restart msu-platform`
3. Verify database connectivity
4. Check disk space
5. Review recent changes

### Database Issues
1. Check PostgreSQL status
2. Review database logs
3. Check disk space
4. Verify connection limits
5. Consider read replica if needed

### High Load
1. Check resource usage: `htop`
2. Review slow queries
3. Increase Gunicorn workers
4. Enable caching
5. Consider horizontal scaling

---

## Rollback Procedure

If deployment fails:

1. **Immediate rollback:**
   ```bash
   # Stop current deployment
   docker-compose down
   
   # Restore previous database backup
   docker-compose exec db psql -U msu_user msu_platform < last_backup.sql
   
   # Checkout previous version
   git checkout previous-tag
   
   # Rebuild and start
   docker-compose build
   docker-compose up -d
   ```

2. **Verify rollback:**
   - Check application is accessible
   - Test critical functionality
   - Review logs for errors

3. **Investigate issue:**
   - Review deployment logs
   - Identify root cause
   - Fix and test locally
   - Deploy again when ready

---

## Success Criteria

Deployment is successful when:

- ✅ All services are running
- ✅ Application is accessible via HTTPS
- ✅ Admin panel accessible
- ✅ User registration works
- ✅ Authentication works
- ✅ Organizations can be created
- ✅ Feed posts work
- ✅ Search functionality works
- ✅ No critical errors in logs
- ✅ Database backups running
- ✅ Monitoring in place

---

**Ready to deploy? Follow this checklist step by step!**

*Last Updated: May 5, 2026*
*Version: 2.0*
