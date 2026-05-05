#!/bin/bash

###############################################################################
# MSU Platform Health Check Script
#
# Monitors system health and reports status of all services.
# Can be used for monitoring, alerting, and debugging.
#
# Usage:
#   ./scripts/check_health.sh [options]
#
# Options:
#   --verbose   Show detailed output
#   --json      Output in JSON format
#   --url       Custom base URL (default: http://localhost:8000)
#
# Example:
#   ./scripts/check_health.sh --verbose
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BASE_URL="http://localhost:8000"
VERBOSE=false
JSON_OUTPUT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --url)
            BASE_URL="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--verbose] [--json] [--url URL]"
            exit 1
            ;;
    esac
done

# Logging functions
log_info() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

log_success() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo -e "${GREEN}[✓]${NC} $1"
    fi
}

log_error() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo -e "${RED}[✗]${NC} $1"
    fi
}

# Check endpoint
check_endpoint() {
    local endpoint=$1
    local name=$2

    if [ "$VERBOSE" = true ]; then
        log_info "Checking $name..."
    fi

    response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}" || echo "000")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$http_code" = "200" ]; then
        log_success "$name: OK"
        if [ "$VERBOSE" = true ]; then
            echo "$body" | jq '.' 2>/dev/null || echo "$body"
        fi
        return 0
    else
        log_error "$name: FAILED (HTTP $http_code)"
        if [ "$VERBOSE" = true ]; then
            echo "$body"
        fi
        return 1
    fi
}

# Main health check
main() {
    if [ "$JSON_OUTPUT" = false ]; then
        echo "========================================================================"
        echo "  MSU Platform Health Check"
        echo "  Base URL: $BASE_URL"
        echo "  Time: $(date)"
        echo "========================================================================"
        echo ""
    fi

    # Overall health
    OVERALL_HEALTHY=true

    # 1. Basic health check
    if check_endpoint "/health/" "Basic Health"; then
        HEALTH_STATUS="healthy"
    else
        HEALTH_STATUS="unhealthy"
        OVERALL_HEALTHY=false
    fi

    # 2. Database check
    if check_endpoint "/health/db/" "Database"; then
        DB_STATUS="healthy"
    else
        DB_STATUS="unhealthy"
        OVERALL_HEALTHY=false
    fi

    # 3. Redis check
    if check_endpoint "/health/redis/" "Redis Cache"; then
        REDIS_STATUS="healthy"
    else
        REDIS_STATUS="unhealthy"
        OVERALL_HEALTHY=false
    fi

    # 4. Celery check
    if check_endpoint "/health/celery/" "Celery Workers"; then
        CELERY_STATUS="healthy"
    else
        CELERY_STATUS="unhealthy"
        # Don't fail overall health for Celery (non-critical)
        log_info "Celery workers not running (non-critical)"
    fi

    # 5. Storage check
    if check_endpoint "/health/storage/" "Storage System"; then
        STORAGE_STATUS="healthy"
    else
        STORAGE_STATUS="unhealthy"
        # Don't fail overall health for storage (non-critical)
        log_info "Storage check failed (non-critical)"
    fi

    # 6. Readiness check
    if check_endpoint "/ready/" "Readiness"; then
        READY_STATUS="ready"
    else
        READY_STATUS="not_ready"
        OVERALL_HEALTHY=false
    fi

    # 7. Liveness check
    if check_endpoint "/alive/" "Liveness"; then
        ALIVE_STATUS="alive"
    else
        ALIVE_STATUS="not_alive"
        OVERALL_HEALTHY=false
    fi

    # Output summary
    if [ "$JSON_OUTPUT" = true ]; then
        # JSON output
        cat << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "base_url": "$BASE_URL",
  "overall_status": "$( [ "$OVERALL_HEALTHY" = true ] && echo "healthy" || echo "unhealthy" )",
  "checks": {
    "health": "$HEALTH_STATUS",
    "database": "$DB_STATUS",
    "redis": "$REDIS_STATUS",
    "celery": "$CELERY_STATUS",
    "storage": "$STORAGE_STATUS",
    "readiness": "$READY_STATUS",
    "liveness": "$ALIVE_STATUS"
  }
}
EOF
    else
        # Human-readable output
        echo ""
        echo "========================================================================"
        echo "  Health Check Summary"
        echo "========================================================================"
        echo ""
        echo "Overall Status: $( [ "$OVERALL_HEALTHY" = true ] && echo -e "${GREEN}HEALTHY${NC}" || echo -e "${RED}UNHEALTHY${NC}" )"
        echo ""
        echo "Component Status:"
        echo "  Health:      $HEALTH_STATUS"
        echo "  Database:    $DB_STATUS"
        echo "  Redis:       $REDIS_STATUS"
        echo "  Celery:      $CELERY_STATUS"
        echo "  Storage:     $STORAGE_STATUS"
        echo "  Readiness:   $READY_STATUS"
        echo "  Liveness:    $ALIVE_STATUS"
        echo ""
        echo "========================================================================"
    fi

    # Exit with appropriate code
    if [ "$OVERALL_HEALTHY" = true ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main
