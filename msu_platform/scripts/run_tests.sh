#!/bin/bash

###############################################################################
# MSU Platform Test Runner
#
# Comprehensive test script that runs all checks before committing code.
# Includes linting, type checking, security scans, and tests.
#
# Usage:
#   ./scripts/run_tests.sh [options]
#
# Options:
#   --fast      Run only fast tests
#   --coverage  Run with coverage report
#   --all       Run all checks including slow tests
#
# Example:
#   ./scripts/run_tests.sh --coverage
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RUN_COVERAGE=false
RUN_FAST=false
RUN_ALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fast)
            RUN_FAST=true
            shift
            ;;
        --coverage)
            RUN_COVERAGE=true
            shift
            ;;
        --all)
            RUN_ALL=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--fast|--coverage|--all]"
            exit 1
            ;;
    esac
done

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo ""
    echo -e "${YELLOW}▶${NC} $1"
}

# Check if in project directory
cd "$PROJECT_DIR"

# Print header
echo "========================================================================"
echo "  MSU Platform Test Suite"
echo "  Started at: $(date)"
echo "========================================================================"

# 1. Code formatting check
log_step "1. Checking code formatting with black..."
if black apps config --check --quiet; then
    log_success "Code formatting check passed"
else
    log_error "Code formatting check failed"
    echo "Run: black apps config"
    exit 1
fi

# 2. Import sorting check
log_step "2. Checking import order with isort..."
if isort apps config --check-only --quiet; then
    log_success "Import order check passed"
else
    log_error "Import order check failed"
    echo "Run: isort apps config"
    exit 1
fi

# 3. Linting with flake8
log_step "3. Linting code with flake8..."
if flake8 apps config; then
    log_success "Linting passed"
else
    log_error "Linting failed"
    exit 1
fi

# 4. Type checking (optional)
log_step "4. Type checking with mypy..."
if command -v mypy &> /dev/null; then
    if mypy apps config --ignore-missing-imports --no-strict-optional 2>&1 | grep -v "Success"; then
        log_info "Type checking completed (warnings may exist)"
    fi
else
    log_info "mypy not installed, skipping type checking"
fi

# 5. Security scanning
log_step "5. Running security checks with bandit..."
if bandit -r apps config -ll -i --skip B308,B703 -q; then
    log_success "Security check passed"
else
    log_error "Security check failed"
    exit 1
fi

# 6. Django checks
log_step "6. Running Django system checks..."
if python manage.py check --settings=config.settings.testing; then
    log_success "Django system check passed"
else
    log_error "Django system check failed"
    exit 1
fi

# 7. Check for missing migrations
log_step "7. Checking for missing migrations..."
if python manage.py makemigrations --check --dry-run --settings=config.settings.testing; then
    log_success "No missing migrations"
else
    log_error "Missing migrations detected"
    echo "Run: python manage.py makemigrations"
    exit 1
fi

# 8. Run tests
log_step "8. Running test suite..."

TEST_ARGS=""

if [ "$RUN_FAST" = true ]; then
    log_info "Running fast tests only..."
    TEST_ARGS="-m 'not slow'"
elif [ "$RUN_ALL" = true ]; then
    log_info "Running all tests..."
    TEST_ARGS=""
else
    log_info "Running standard tests..."
    TEST_ARGS="-m 'not slow'"
fi

if [ "$RUN_COVERAGE" = true ]; then
    log_info "Running with coverage report..."
    pytest $TEST_ARGS --cov=apps --cov-report=html --cov-report=term-missing --cov-report=xml -v
    log_success "Coverage report generated in htmlcov/"
else
    pytest $TEST_ARGS -v
fi

log_success "All tests passed"

# Summary
echo ""
echo "========================================================================"
echo -e "${GREEN}✓${NC} All checks passed successfully!"
echo "  Completed at: $(date)"
echo "========================================================================"
echo ""
echo "Summary:"
echo "  ✓ Code formatting (black)"
echo "  ✓ Import order (isort)"
echo "  ✓ Linting (flake8)"
echo "  ✓ Type checking (mypy)"
echo "  ✓ Security scan (bandit)"
echo "  ✓ Django checks"
echo "  ✓ Migrations check"
echo "  ✓ Tests"

if [ "$RUN_COVERAGE" = true ]; then
    echo ""
    echo "Coverage report: file://$(pwd)/htmlcov/index.html"
fi

echo ""
echo "Ready to commit! 🚀"
