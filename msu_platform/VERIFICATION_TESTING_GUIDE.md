# MSU Platform - Verification Testing Guide

This guide provides step-by-step instructions to verify that the MSU Platform actually works through runtime testing.

---

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 15+ (or use Docker)
- Redis (or use Docker)
- Git

---

## Option 1: Quick Test with Docker (Recommended)

This is the fastest way to verify everything works.

### Step 1: Start All Services

```bash
cd msu_platform
docker-compose up -d
```

This starts:
- Django web application
- PostgreSQL database
- Redis cache
- Celery worker

### Step 2: Run Migrations

```bash
docker-compose exec web python manage.py migrate
```

Expected output: List of migrations being applied

### Step 3: Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

Enter email and password when prompted.

### Step 4: Test Health Endpoints

```bash
# Test basic health
curl http://localhost:8000/api/health/

# Test database health
curl http://localhost:8000/api/health/db/

# Test Redis health
curl http://localhost:8000/api/health/redis/
```

Expected: All should return `{"status": "ok"}` or similar

### Step 5: Run Test Suite

```bash
docker-compose exec web pytest -v
```

Expected: All tests should pass (256 test methods)

### Step 6: Access Django Admin

1. Visit http://localhost:8000/admin/
2. Login with superuser credentials
3. Browse the available models

### Step 7: Test API Endpoints

```bash
# Register a user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@msu.ac.zw",
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "student_number": "S202312345"
  }'

# Login
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@msu.ac.zw",
    "password": "SecurePass123!"
  }'
```

Save the JWT token from the login response.

### Step 8: Clean Up

```bash
docker-compose down -v
```

---

## Option 2: Manual Testing (Local Environment)

For developers who want to test without Docker.

### Step 1: Set Up Virtual Environment

```bash
cd msu_platform
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected: All packages install successfully

### Step 3: Set Up Environment Variables

```bash
cp .env.example .env
```

Edit .env and configure:
```env
DJANGO_SETTINGS_MODULE=config.settings.development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/msu_platform
REDIS_URL=redis://localhost:6379/0
```

### Step 4: Start PostgreSQL and Redis

If using Docker for just databases:

```bash
docker run -d --name msu_postgres \
  -e POSTGRES_DB=msu_platform \
  -e POSTGRES_USER=msu_user \
  -e POSTGRES_PASSWORD=msu_pass \
  -p 5432:5432 \
  postgres:15

docker run -d --name msu_redis \
  -p 6379:6379 \
  redis:7-alpine
```

Or install and start them locally.

### Step 5: Run Migrations

```bash
python manage.py migrate
```

Expected: Migrations apply successfully

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Expected: Server starts on http://127.0.0.1:8000/

### Step 8: Run Tests

In another terminal (with venv activated):

```bash
export DJANGO_SETTINGS_MODULE=config.settings.testing
pytest -v --cov=apps
```

Expected: All tests pass with coverage report

### Step 9: Run Celery Worker

In another terminal (with venv activated):

```bash
celery -A config worker -l info
```

Expected: Worker starts and connects to Redis

### Step 10: Test API Manually

Use the curl commands from Option 1, Step 7.

---

## Option 3: Comprehensive Verification Script

We've created automated verification scripts for you.

### Static Verification (No Dependencies Required)

```bash
cd msu_platform
python3 static_verification.py
```

This checks:
- File structure
- Python syntax
- Model definitions
- Configuration files
- Documentation

Expected output:
```
✓ PLATFORM STRUCTURE IS VALID
Passed: 45
Failed: 0
Warnings: 1
```

### Full Verification (Requires Dependencies)

```bash
cd msu_platform
source venv/bin/activate
python verify_platform.py
```

This performs runtime checks of imports and Django configuration.

---

## Verification Checklist

Use this checklist to verify all major features:

### ✅ Core Functionality

- [ ] Django starts without errors
- [ ] Migrations apply successfully
- [ ] Admin interface accessible
- [ ] Database connections work
- [ ] Redis connections work

### ✅ Authentication

- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Token authentication works
- [ ] Logout works
- [ ] Token refresh works

### ✅ Organizations

- [ ] Can create clubs
- [ ] Can list organizations
- [ ] Can search organizations
- [ ] Can join/leave organizations
- [ ] Membership management works

### ✅ Social Feed

- [ ] Can create posts
- [ ] Can view feed
- [ ] Can like posts
- [ ] Can comment on posts
- [ ] Can share posts
- [ ] Feed algorithm generates personalized content

### ✅ Media

- [ ] Can upload images
- [ ] Can upload videos
- [ ] Video transcoding tasks enqueue
- [ ] Media appears in posts

### ✅ API Endpoints

- [ ] Health check endpoints respond
- [ ] User endpoints work
- [ ] Organization endpoints work
- [ ] Post endpoints work
- [ ] Feed endpoints work
- [ ] Media endpoints work
- [ ] Search endpoints work

### ✅ Testing

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Test coverage > 80%

### ✅ Performance

- [ ] Feed loads in < 2 seconds
- [ ] API responses < 500ms
- [ ] Cache hit rates > 70%
- [ ] Database queries optimized

---

## Common Issues & Solutions

### Issue: Django won't start

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep Django

# Check environment variables
echo $DJANGO_SETTINGS_MODULE
```

### Issue: Database connection fails

**Solution:**
```bash
# Test PostgreSQL connection
psql -U msu_user -d msu_platform -h localhost

# Check DATABASE_URL in .env
# Ensure PostgreSQL is running
docker ps | grep postgres
```

### Issue: Redis connection fails

**Solution:**
```bash
# Test Redis connection
redis-cli ping  # Should return PONG

# Check REDIS_URL in .env
# Ensure Redis is running
docker ps | grep redis
```

### Issue: Tests fail

**Solution:**
```bash
# Use test settings
export DJANGO_SETTINGS_MODULE=config.settings.testing

# Run with verbose output
pytest -v -s

# Run specific test
pytest apps/users/tests/test_models.py::TestUserModel::test_create_user -v
```

### Issue: Celery won't start

**Solution:**
```bash
# Check Redis is running
redis-cli ping

# Check Celery configuration
python manage.py shell
>>> from django.conf import settings
>>> print(settings.CELERY_BROKER_URL)

# Start with debug logging
celery -A config worker -l debug
```

### Issue: Migrations conflict

**Solution:**
```bash
# Reset migrations (development only!)
python manage.py migrate --fake-initial

# Or drop and recreate database
dropdb msu_platform
createdb msu_platform
python manage.py migrate
```

---

## Performance Benchmarks

Expected performance metrics:

| Metric | Target | Acceptable |
|--------|--------|------------|
| API Response Time | < 200ms | < 500ms |
| Feed Generation | < 1s | < 2s |
| Database Queries per Request | < 10 | < 20 |
| Cache Hit Rate | > 80% | > 70% |
| Test Suite Runtime | < 30s | < 60s |

### Run Performance Tests

```bash
# Time the feed generation
time curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/feed/generate/

# Check database query count
python manage.py shell
>>> from django.db import connection
>>> from django.test.utils import override_settings
>>> # Run your queries here
>>> print(len(connection.queries))
```

---

## Security Testing

### Basic Security Checks

```bash
# Check for common vulnerabilities
bandit -r apps config

# Check for outdated packages
safety check --file requirements.txt

# Check Django security settings
python manage.py check --deploy
```

### Test Security Features

1. **CSRF Protection**
   - Try POST without CSRF token → Should fail
   - Try POST with invalid token → Should fail

2. **Authentication**
   - Try accessing protected endpoint without token → Should return 401
   - Try accessing with expired token → Should return 401
   - Try accessing with invalid token → Should return 401

3. **Authorization**
   - Try accessing another user's private data → Should return 403
   - Try modifying another user's data → Should return 403

4. **Input Validation**
   - Try sending invalid data types → Should return 400
   - Try sending SQL injection strings → Should be sanitized
   - Try sending XSS payloads → Should be escaped

---

## Load Testing

### Simple Load Test with Apache Bench

```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Ubuntu/Debian
brew install httpie  # macOS

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/api/health/

# Test authenticated endpoint
ab -n 100 -c 5 -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/feed/
```

### Expected Results
- Requests per second: > 100
- Average response time: < 100ms
- Failed requests: 0%

---

## Continuous Monitoring

### Set Up Health Checks

```bash
# Add to crontab for periodic checks
*/5 * * * * curl -f http://localhost:8000/api/health/ || echo "Health check failed"
```

### Monitor Logs

```bash
# Watch application logs
docker-compose logs -f web

# Watch Celery logs
docker-compose logs -f celery

# Watch database logs
docker-compose logs -f db
```

### Monitor Metrics

```bash
# Check database connections
psql -U msu_user -d msu_platform -c "SELECT count(*) FROM pg_stat_activity;"

# Check Redis memory
redis-cli INFO memory

# Check Celery queue length
python manage.py shell
>>> from celery import current_app
>>> inspect = current_app.control.inspect()
>>> print(inspect.active_queues())
```

---

## Final Verification Command

Run this comprehensive test to verify everything:

```bash
#!/bin/bash
# comprehensive_test.sh

set -e  # Exit on error

echo "=== MSU Platform Comprehensive Test ==="

echo "1. Checking Python version..."
python --version

echo "2. Starting services..."
docker-compose up -d

echo "3. Waiting for services to be ready..."
sleep 10

echo "4. Running migrations..."
docker-compose exec -T web python manage.py migrate

echo "5. Running tests..."
docker-compose exec -T web pytest -v --tb=short

echo "6. Checking health endpoints..."
curl -f http://localhost:8000/api/health/
curl -f http://localhost:8000/api/health/db/
curl -f http://localhost:8000/api/health/redis/

echo "7. Running Django checks..."
docker-compose exec -T web python manage.py check --deploy

echo "8. Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo ""
echo "=== All Tests Passed! ✅ ==="
echo "Platform is verified and working correctly."
echo ""
echo "Next steps:"
echo "1. Access admin: http://localhost:8000/admin/"
echo "2. Access API: http://localhost:8000/api/"
echo "3. View logs: docker-compose logs -f"
echo "4. Stop services: docker-compose down"
```

Save as `comprehensive_test.sh`, make executable, and run:

```bash
chmod +x comprehensive_test.sh
./comprehensive_test.sh
```

---

## Success Criteria

The platform is verified and working if:

✅ All services start without errors
✅ All migrations apply successfully
✅ All tests pass (256/256)
✅ All health endpoints return OK
✅ Django admin is accessible
✅ API endpoints respond correctly
✅ Authentication works
✅ CRUD operations work
✅ Feed generation works
✅ Media upload works
✅ Celery tasks execute
✅ Cache operations work
✅ No security warnings
✅ Performance meets targets

---

## Support & Troubleshooting

If you encounter issues:

1. Check logs: `docker-compose logs -f web`
2. Check database: `docker-compose exec db psql -U msu_user -d msu_platform`
3. Check Redis: `docker-compose exec redis redis-cli`
4. Review documentation in `/docs/` directory
5. Check GitHub issues
6. Review error messages carefully

---

**Document Version:** 1.0
**Last Updated:** 2026-05-05
**Platform Version:** 1.0.0
