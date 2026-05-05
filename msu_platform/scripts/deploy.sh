#!/bin/bash

###############################################################################
# MSU Platform Deployment Script
#
# This script handles deployment to production or staging environments.
# It performs health checks, runs migrations, collects static files, and
# restarts services with zero-downtime deployment.
#
# Usage:
#   ./scripts/deploy.sh [production|staging]
#
# Example:
#   ./scripts/deploy.sh production
###############################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT="${1:-staging}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${PROJECT_DIR}/backups"

# Logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print deployment header
print_header() {
    echo "========================================================================"
    echo "  MSU Platform Deployment - ${ENVIRONMENT^^}"
    echo "  Started at: $(date)"
    echo "========================================================================"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if environment is valid
    if [[ ! "$ENVIRONMENT" =~ ^(production|staging)$ ]]; then
        log_error "Invalid environment: $ENVIRONMENT"
        log_error "Usage: $0 [production|staging]"
        exit 1
    fi

    # Check if .env file exists
    if [ ! -f "${PROJECT_DIR}/.env" ]; then
        log_error ".env file not found in ${PROJECT_DIR}"
        exit 1
    fi

    # Check if required commands are available
    for cmd in python pip docker docker-compose git; do
        if ! command -v $cmd &> /dev/null; then
            log_error "$cmd is not installed or not in PATH"
            exit 1
        fi
    done

    log_success "Prerequisites check passed"
}

# Backup database
backup_database() {
    log_info "Creating database backup..."

    mkdir -p "$BACKUP_DIR"

    # Export environment variables
    source "${PROJECT_DIR}/.env"

    # Create backup filename
    BACKUP_FILE="${BACKUP_DIR}/db_backup_${ENVIRONMENT}_${TIMESTAMP}.sql"

    # Perform backup based on environment
    if [ "$ENVIRONMENT" == "production" ]; then
        python manage.py dumpdata --natural-foreign --natural-primary \
            -e contenttypes -e auth.Permission \
            --indent 2 > "${BACKUP_FILE}.json"
    else
        python manage.py dumpdata --natural-foreign --natural-primary \
            -e contenttypes -e auth.Permission \
            --indent 2 > "${BACKUP_FILE}.json"
    fi

    log_success "Database backup created: ${BACKUP_FILE}.json"
}

# Pull latest code
pull_code() {
    log_info "Pulling latest code from git..."

    cd "$PROJECT_DIR"

    # Get current branch
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

    # Determine target branch
    if [ "$ENVIRONMENT" == "production" ]; then
        TARGET_BRANCH="main"
    else
        TARGET_BRANCH="develop"
    fi

    # Checkout target branch if different
    if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
        log_warning "Switching from $CURRENT_BRANCH to $TARGET_BRANCH"
        git checkout "$TARGET_BRANCH"
    fi

    # Pull latest changes
    git pull origin "$TARGET_BRANCH"

    # Show current commit
    CURRENT_COMMIT=$(git rev-parse --short HEAD)
    log_success "Deployed commit: $CURRENT_COMMIT"
}

# Install dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."

    cd "$PROJECT_DIR"

    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    # Upgrade pip
    pip install --upgrade pip

    # Install requirements
    pip install -r requirements.txt

    log_success "Dependencies installed"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."

    cd "$PROJECT_DIR"

    # Check for pending migrations
    python manage.py showmigrations --plan | grep -q '\[ \]' && HAS_MIGRATIONS=true || HAS_MIGRATIONS=false

    if [ "$HAS_MIGRATIONS" = true ]; then
        log_warning "Pending migrations found, applying..."
        python manage.py migrate --noinput
        log_success "Migrations applied"
    else
        log_info "No pending migrations"
    fi
}

# Collect static files
collect_static() {
    log_info "Collecting static files..."

    cd "$PROJECT_DIR"

    python manage.py collectstatic --noinput --clear

    log_success "Static files collected"
}

# Run tests
run_tests() {
    log_info "Running test suite..."

    cd "$PROJECT_DIR"

    # Run critical tests only in production
    if [ "$ENVIRONMENT" == "production" ]; then
        pytest -m "not slow" --tb=short -q
    else
        pytest --tb=short -q
    fi

    log_success "Tests passed"
}

# Health check
health_check() {
    log_info "Performing health check..."

    # Wait for service to be ready
    max_attempts=30
    attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
            log_success "Health check passed"
            return 0
        fi

        attempt=$((attempt + 1))
        sleep 2
    done

    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Restart services
restart_services() {
    log_info "Restarting services..."

    cd "$PROJECT_DIR"

    if [ "$ENVIRONMENT" == "production" ]; then
        # Production: use systemd or supervisor
        if command -v systemctl &> /dev/null; then
            sudo systemctl restart msu-platform
            sudo systemctl restart celery-worker
            sudo systemctl restart celery-beat
        fi
    else
        # Staging: use docker-compose
        docker-compose restart web
        docker-compose restart celery
        docker-compose restart celery-beat
    fi

    log_success "Services restarted"
}

# Clear cache
clear_cache() {
    log_info "Clearing application cache..."

    cd "$PROJECT_DIR"

    python manage.py shell << EOF
from django.core.cache import cache
cache.clear()
print("Cache cleared successfully")
EOF

    log_success "Cache cleared"
}

# Send notification
send_notification() {
    local status=$1

    log_info "Sending deployment notification..."

    # You can integrate with Slack, Discord, email, etc.
    # Example: curl -X POST https://hooks.slack.com/...

    log_info "Notification sent (placeholder)"
}

# Main deployment flow
main() {
    print_header

    # Trap errors and send notification
    trap 'log_error "Deployment failed!"; send_notification "failed"; exit 1' ERR

    check_prerequisites
    backup_database
    pull_code
    install_dependencies
    run_migrations
    collect_static

    # Only run tests in staging
    if [ "$ENVIRONMENT" == "staging" ]; then
        run_tests
    fi

    restart_services
    sleep 5  # Wait for services to start
    health_check
    clear_cache

    log_success "Deployment completed successfully!"
    send_notification "success"

    echo "========================================================================"
    echo "  Deployment Summary"
    echo "  Environment: ${ENVIRONMENT^^}"
    echo "  Commit: $(git rev-parse --short HEAD)"
    echo "  Completed at: $(date)"
    echo "========================================================================"
}

# Run main function
main
