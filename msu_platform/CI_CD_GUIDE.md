# CI/CD Guide - MSU Platform

This guide covers the Continuous Integration and Continuous Deployment pipeline for the MSU Platform project.

## Table of Contents

- [Overview](#overview)
- [Pipeline Architecture](#pipeline-architecture)
- [Local Development Workflow](#local-development-workflow)
- [Pre-commit Hooks](#pre-commit-hooks)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Deployment Process](#deployment-process)
- [Monitoring and Alerts](#monitoring-and-alerts)
- [Troubleshooting](#troubleshooting)

## Overview

The MSU Platform uses a comprehensive CI/CD pipeline that includes:

- **Automated Testing**: Unit tests, integration tests, and coverage reports
- **Code Quality**: Linting, formatting, and type checking
- **Security Scanning**: Vulnerability detection and security audits
- **Docker Builds**: Containerized deployment
- **Health Checks**: Automated service monitoring

### Pipeline Stages

1. **Lint** - Code quality checks (black, isort, flake8)
2. **Security** - Security scanning (bandit, safety)
3. **Test** - Run test suite with coverage
4. **Build** - Build Docker images
5. **Integration Test** - End-to-end testing
6. **Deploy** - Automated deployment (production/staging)

## Pipeline Architecture

```
┌─────────────┐
│   Push/PR   │
└──────┬──────┘
       │
       ├─────────────┬─────────────┬─────────────┐
       │             │             │             │
       ▼             ▼             ▼             ▼
  ┌────────┐   ┌──────────┐  ┌───────┐    ┌─────────┐
  │  Lint  │   │ Security │  │ Tests │    │  Build  │
  └────┬───┘   └────┬─────┘  └───┬───┘    └────┬────┘
       │            │            │             │
       └────────────┴────────────┴─────────────┘
                    │
                    ▼
           ┌──────────────────┐
           │ Integration Test │
           └────────┬─────────┘
                    │
                    ▼
              ┌──────────┐
              │  Deploy  │
              └──────────┘
```

## Local Development Workflow

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/msu-platform.git
   cd msu-platform/msu_platform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

### Daily Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and write tests**
   - Write code
   - Write tests for new functionality
   - Update documentation

3. **Run tests locally**
   ```bash
   ./scripts/run_tests.sh
   ```

4. **Run fast tests only**
   ```bash
   ./scripts/run_tests.sh --fast
   ```

5. **Run with coverage**
   ```bash
   ./scripts/run_tests.sh --coverage
   ```

6. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```
   - Pre-commit hooks will run automatically
   - If hooks fail, fix issues and commit again

7. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create Pull Request**
   - Go to GitHub
   - Create PR from your branch to `develop`
   - Wait for CI checks to pass
   - Request review

## Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality.

### Installed Hooks

1. **General Checks**
   - Trailing whitespace removal
   - End-of-file fixer
   - YAML/JSON validation
   - Large file detection
   - Private key detection

2. **Python Code Quality**
   - **Black**: Code formatting
   - **isort**: Import sorting
   - **flake8**: Linting
   - **mypy**: Type checking
   - **bandit**: Security scanning
   - **pyupgrade**: Python syntax upgrade

3. **Django-specific**
   - Django system checks
   - Migration checks
   - Fast tests (on push)

### Manual Execution

Run all hooks manually:
```bash
pre-commit run --all-files
```

Run specific hook:
```bash
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

Update hooks:
```bash
pre-commit autoupdate
```

Skip hooks (not recommended):
```bash
git commit --no-verify -m "message"
```

## GitHub Actions Workflow

### Trigger Events

The CI pipeline triggers on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Jobs

#### 1. Lint Job

Runs code quality checks:
```yaml
- flake8 (linting)
- isort (import order)
- black (formatting)
```

**Duration**: ~2 minutes

#### 2. Security Job

Runs security audits:
```yaml
- safety (dependency vulnerabilities)
- bandit (code security issues)
```

**Duration**: ~3 minutes

Artifacts:
- `bandit-report.json` (30 days retention)

#### 3. Test Job

Runs comprehensive test suite:
```yaml
Services:
- PostgreSQL 15
- Redis Alpine

Steps:
1. Install system dependencies (FFmpeg)
2. Install Python dependencies
3. Create .env file
4. Run migrations
5. Collect static files
6. Run tests with coverage
7. Upload coverage to Codecov
```

**Duration**: ~8 minutes

Artifacts:
- `coverage-report` (HTML, 30 days retention)
- `test-results` (30 days retention)

Coverage uploaded to [Codecov](https://codecov.io)

#### 4. Build Job

Builds Docker image:
```yaml
Conditions:
- Only on main/develop branches
- After lint, test, security pass

Steps:
1. Set up Docker Buildx
2. Login to Docker Hub
3. Build and push image
4. Tag with branch name and commit SHA
```

**Duration**: ~10 minutes

#### 5. Integration Test Job

Tests Docker deployment:
```yaml
Steps:
1. Start services with docker-compose
2. Wait for services to be ready
3. Run health checks
4. Run API endpoint tests
5. Show logs on failure
```

**Duration**: ~5 minutes

### Required Secrets

Configure in GitHub repository settings:

```yaml
CODECOV_TOKEN          # Codecov upload token
DOCKER_USERNAME        # Docker Hub username
DOCKER_PASSWORD        # Docker Hub password
```

### Branch Protection

Recommended branch protection rules for `main`:

- Require pull request before merging
- Require status checks to pass:
  - `lint`
  - `security`
  - `test`
- Require branches to be up to date
- Require conversation resolution
- Require signed commits (optional)

## Deployment Process

### Staging Deployment

Automatic deployment to staging on push to `develop`:

```bash
# Automatically triggers after CI passes
git push origin develop
```

### Production Deployment

Manual deployment to production:

```bash
# Method 1: Using script
cd msu_platform
./scripts/deploy.sh production

# Method 2: Using Docker
docker-compose -f docker-compose.prod.yml up -d

# Method 3: Manual steps
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart msu-platform
```

### Deployment Checklist

Before deploying to production:

- [ ] All tests passing in CI
- [ ] Code reviewed and approved
- [ ] Database migrations tested
- [ ] Environment variables updated
- [ ] Backup created
- [ ] Rollback plan ready
- [ ] Monitoring configured
- [ ] Team notified

### Rollback Procedure

If deployment fails:

```bash
# 1. Switch to previous version
git checkout <previous-commit>

# 2. Restore database backup
python manage.py loaddata backups/db_backup_TIMESTAMP.json

# 3. Restart services
sudo systemctl restart msu-platform

# 4. Verify health
./scripts/check_health.sh
```

## Monitoring and Alerts

### Health Checks

Available health check endpoints:

```bash
# Basic health
curl http://your-domain.com/health/

# Detailed health (all services)
curl http://your-domain.com/health/detailed/

# Individual services
curl http://your-domain.com/health/db/
curl http://your-domain.com/health/redis/
curl http://your-domain.com/health/celery/
curl http://your-domain.com/health/storage/

# Kubernetes probes
curl http://your-domain.com/ready/    # Readiness
curl http://your-domain.com/alive/    # Liveness
```

### Monitoring Script

Run health checks locally:

```bash
# Basic check
./scripts/check_health.sh

# Verbose output
./scripts/check_health.sh --verbose

# JSON output
./scripts/check_health.sh --json

# Custom URL
./scripts/check_health.sh --url https://api.msu.ac.zw
```

### Logging

Logs are stored in:
```
logs/
├── general.log       # All application logs
├── errors.log        # Error logs only
├── security.log      # Security-related logs
└── performance.log   # Performance metrics
```

View logs:
```bash
# Tail error logs
tail -f logs/errors.log

# Search logs
grep "ERROR" logs/general.log

# View last 100 lines
tail -n 100 logs/general.log
```

### Sentry Integration

For production error tracking:

1. Sign up at [sentry.io](https://sentry.io)
2. Create a new project
3. Add DSN to `.env`:
   ```bash
   SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
   ```
4. Errors will be automatically reported to Sentry

## Troubleshooting

### Common Issues

#### 1. Pre-commit hooks failing

**Issue**: Hooks fail with import errors

**Solution**:
```bash
# Reinstall pre-commit
pip install --upgrade pre-commit
pre-commit clean
pre-commit install
```

#### 2. Tests failing locally but passing in CI

**Issue**: Different environments

**Solution**:
```bash
# Use same settings as CI
export DJANGO_SETTINGS_MODULE=config.settings.testing
pytest
```

#### 3. Docker build failing

**Issue**: Cache issues or dependencies

**Solution**:
```bash
# Clear Docker cache
docker system prune -a
docker-compose build --no-cache
```

#### 4. Migration conflicts

**Issue**: Multiple migration files

**Solution**:
```bash
# Merge migrations
python manage.py makemigrations --merge
```

#### 5. Coverage below threshold

**Issue**: Test coverage insufficient

**Solution**:
```bash
# Check uncovered lines
pytest --cov=apps --cov-report=term-missing

# View HTML report
pytest --cov=apps --cov-report=html
open htmlcov/index.html
```

### Getting Help

1. Check logs: `logs/errors.log`
2. Run health checks: `./scripts/check_health.sh --verbose`
3. Check CI logs in GitHub Actions
4. Review Sentry error reports
5. Contact DevOps team

## Best Practices

### Commit Messages

Follow conventional commits:

```bash
feat: add user registration
fix: correct login validation
docs: update API documentation
test: add integration tests
refactor: improve code structure
perf: optimize database queries
chore: update dependencies
```

### Testing

- Write tests for all new features
- Aim for >80% code coverage
- Use meaningful test names
- Test edge cases
- Mock external services

### Code Quality

- Run `./scripts/run_tests.sh` before committing
- Fix all linting errors
- Keep functions small and focused
- Write docstrings for public APIs
- Follow PEP 8 style guide

### Security

- Never commit secrets
- Use environment variables
- Review security scan results
- Update dependencies regularly
- Follow OWASP guidelines

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Pre-commit Documentation](https://pre-commit.com/)

---

**Last Updated**: May 5, 2026
**Version**: 1.0
