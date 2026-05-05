"""
Storage backends for MSU Platform.

Provides S3 and local filesystem storage with automatic fallback.
Supports CDN integration for media delivery.
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    """
    S3 storage backend for user-uploaded media (images, videos, documents).

    Features:
    - Public read access for media files
    - Automatic CDN integration
    - File organization by type
    """

    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = settings.AWS_CLOUDFRONT_DOMAIN if hasattr(settings, 'AWS_CLOUDFRONT_DOMAIN') else None

    def __init__(self, *args, **kwargs):
        """Initialize storage with fallback to local storage if S3 is not configured."""
        try:
            # Check if AWS credentials are configured
            if not settings.USE_S3:
                raise ValueError("S3 is not configured")
            super().__init__(*args, **kwargs)
            logger.info("Initialized S3 media storage")
        except Exception as e:
            logger.warning(f"S3 storage initialization failed: {e}. Falling back to local storage.")
            # Fallback to local storage
            self._fallback_to_local()

    def _fallback_to_local(self):
        """Fallback to local filesystem storage."""
        self.__class__ = LocalMediaStorage


class StaticStorage(S3Boto3Storage):
    """
    S3 storage backend for static files (CSS, JS, fonts).

    Features:
    - Long-term caching headers
    - Gzip compression
    - CDN integration
    """

    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    custom_domain = settings.AWS_CLOUDFRONT_DOMAIN if hasattr(settings, 'AWS_CLOUDFRONT_DOMAIN') else None

    # Cache static files for 1 year
    object_parameters = {
        'CacheControl': 'max-age=31536000',
    }


class LocalMediaStorage(FileSystemStorage):
    """
    Local filesystem storage for development and fallback.

    Use this when S3 is not available or for local development.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.MEDIA_ROOT
        kwargs['base_url'] = settings.MEDIA_URL
        super().__init__(*args, **kwargs)
        logger.info("Using local filesystem for media storage")


class PrivateMediaStorage(S3Boto3Storage):
    """
    Private S3 storage for sensitive files (documents, private videos).

    Features:
    - Private access (requires signed URLs)
    - Time-limited access links
    - Secure file organization
    """

    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = None  # Don't use CDN for private files

    # Set expiry time for signed URLs (1 hour)
    querystring_auth = True
    querystring_expire = 3600

    def __init__(self, *args, **kwargs):
        """Initialize storage with fallback to local storage if S3 is not configured."""
        try:
            if not settings.USE_S3:
                raise ValueError("S3 is not configured")
            super().__init__(*args, **kwargs)
            logger.info("Initialized S3 private storage")
        except Exception as e:
            logger.warning(f"S3 private storage initialization failed: {e}. Falling back to local storage.")
            self._fallback_to_local()

    def _fallback_to_local(self):
        """Fallback to local filesystem storage."""
        self.__class__ = LocalPrivateStorage


class LocalPrivateStorage(FileSystemStorage):
    """
    Local filesystem storage for private files in development.
    """

    def __init__(self, *args, **kwargs):
        import os
        private_root = os.path.join(settings.MEDIA_ROOT, 'private')
        kwargs['location'] = private_root
        kwargs['base_url'] = f"{settings.MEDIA_URL}private/"
        super().__init__(*args, **kwargs)
        logger.info("Using local filesystem for private storage")


def get_media_storage():
    """
    Get the appropriate media storage backend.

    Returns:
        Storage instance (S3 or local filesystem)
    """
    if settings.USE_S3:
        return MediaStorage()
    return LocalMediaStorage()


def get_private_storage():
    """
    Get the appropriate private storage backend.

    Returns:
        Storage instance (S3 or local filesystem)
    """
    if settings.USE_S3:
        return PrivateMediaStorage()
    return LocalPrivateStorage()
