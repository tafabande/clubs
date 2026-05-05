"""
Health check endpoints for monitoring system status.

Provides various health check endpoints to verify:
- Overall system health
- Database connectivity
- Redis connectivity
- Celery worker status
- Storage system status
"""
import logging
from typing import Dict, Any

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """
    Basic health check endpoint.

    Returns 200 OK if the service is running.
    Useful for load balancers and monitoring systems.
    """
    return Response({
        'status': 'healthy',
        'service': 'MSU Platform API',
        'version': '1.0.0',
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_detailed(request: Request) -> Response:
    """
    Detailed health check with all service statuses.

    Checks:
    - Database connectivity
    - Redis cache
    - Celery workers
    - Storage system

    Returns overall status and individual component statuses.
    """
    health_status = {
        'status': 'healthy',
        'service': 'MSU Platform API',
        'version': '1.0.0',
        'checks': {}
    }

    # Check database
    db_status = _check_database()
    health_status['checks']['database'] = db_status

    # Check Redis cache
    cache_status = _check_redis()
    health_status['checks']['cache'] = cache_status

    # Check Celery
    celery_status = _check_celery()
    health_status['checks']['celery'] = celery_status

    # Check storage
    storage_status = _check_storage()
    health_status['checks']['storage'] = storage_status

    # Determine overall health
    all_healthy = all(
        check['status'] == 'healthy'
        for check in health_status['checks'].values()
    )

    if not all_healthy:
        health_status['status'] = 'degraded'
        return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(health_status, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_database(request: Request) -> Response:
    """
    Database connectivity check.

    Verifies that the application can connect to and query the database.
    """
    db_status = _check_database()

    response_status = (
        status.HTTP_200_OK
        if db_status['status'] == 'healthy'
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(db_status, status=response_status)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_redis(request: Request) -> Response:
    """
    Redis cache connectivity check.

    Verifies that the application can connect to Redis and perform operations.
    """
    cache_status = _check_redis()

    response_status = (
        status.HTTP_200_OK
        if cache_status['status'] == 'healthy'
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(cache_status, status=response_status)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_celery(request: Request) -> Response:
    """
    Celery worker status check.

    Verifies that Celery workers are running and responsive.
    """
    celery_status = _check_celery()

    response_status = (
        status.HTTP_200_OK
        if celery_status['status'] == 'healthy'
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(celery_status, status=response_status)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_storage(request: Request) -> Response:
    """
    Storage system check.

    Verifies that the storage system (S3 or local) is accessible.
    """
    storage_status = _check_storage()

    response_status = (
        status.HTTP_200_OK
        if storage_status['status'] == 'healthy'
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(storage_status, status=response_status)


def _check_database() -> Dict[str, Any]:
    """
    Check database connectivity.

    Returns:
        Dictionary with status and details
    """
    try:
        # Try to execute a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return {
            'status': 'healthy',
            'message': 'Database connection successful',
            'database': settings.DATABASES['default']['NAME'],
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}", exc_info=True)
        return {
            'status': 'unhealthy',
            'message': 'Database connection failed',
            'error': str(e),
        }


def _check_redis() -> Dict[str, Any]:
    """
    Check Redis cache connectivity.

    Returns:
        Dictionary with status and details
    """
    try:
        # Try to set and get a value from cache
        test_key = 'health_check_test'
        test_value = 'ok'

        cache.set(test_key, test_value, timeout=10)
        cached_value = cache.get(test_key)

        if cached_value == test_value:
            cache.delete(test_key)
            return {
                'status': 'healthy',
                'message': 'Redis connection successful',
            }
        else:
            return {
                'status': 'unhealthy',
                'message': 'Redis value mismatch',
            }
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}", exc_info=True)
        return {
            'status': 'unhealthy',
            'message': 'Redis connection failed',
            'error': str(e),
        }


def _check_celery() -> Dict[str, Any]:
    """
    Check Celery worker status.

    Returns:
        Dictionary with status and details
    """
    try:
        from config.celery import app as celery_app

        # Get active workers
        inspect = celery_app.control.inspect()
        active_workers = inspect.active()

        if active_workers:
            worker_count = len(active_workers)
            return {
                'status': 'healthy',
                'message': f'{worker_count} Celery worker(s) active',
                'workers': list(active_workers.keys()),
            }
        else:
            return {
                'status': 'unhealthy',
                'message': 'No active Celery workers found',
            }
    except Exception as e:
        logger.error(f"Celery health check failed: {str(e)}", exc_info=True)
        return {
            'status': 'unhealthy',
            'message': 'Celery check failed',
            'error': str(e),
        }


def _check_storage() -> Dict[str, Any]:
    """
    Check storage system status.

    Returns:
        Dictionary with status and details
    """
    try:
        from django.core.files.storage import default_storage

        # Check if storage is accessible
        # For S3, this will verify AWS credentials and bucket access
        # For local storage, this will verify directory access
        storage_available = default_storage.__class__.__name__

        # Try to list files (without actually reading them)
        try:
            # This is a lightweight check
            default_storage.exists('health_check_test.txt')

            return {
                'status': 'healthy',
                'message': 'Storage system accessible',
                'storage_backend': storage_available,
                'use_s3': settings.USE_S3,
            }
        except Exception as storage_error:
            return {
                'status': 'degraded',
                'message': 'Storage system partially accessible',
                'storage_backend': storage_available,
                'warning': str(storage_error),
            }

    except Exception as e:
        logger.error(f"Storage health check failed: {str(e)}", exc_info=True)
        return {
            'status': 'unhealthy',
            'message': 'Storage system check failed',
            'error': str(e),
        }


@api_view(['GET'])
@permission_classes([AllowAny])
def readiness_check(request: Request) -> Response:
    """
    Kubernetes readiness probe endpoint.

    Returns 200 if the service is ready to accept traffic.
    Checks critical services (database, cache).
    """
    db_status = _check_database()
    cache_status = _check_redis()

    ready = (
        db_status['status'] == 'healthy' and
        cache_status['status'] == 'healthy'
    )

    if ready:
        return Response({'ready': True}, status=status.HTTP_200_OK)
    else:
        return Response({
            'ready': False,
            'database': db_status,
            'cache': cache_status,
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def liveness_check(request: Request) -> Response:
    """
    Kubernetes liveness probe endpoint.

    Returns 200 if the service is alive and responding.
    This is a minimal check that doesn't verify dependencies.
    """
    return Response({
        'alive': True,
        'service': 'MSU Platform API',
    }, status=status.HTTP_200_OK)
