"""
Development settings.
"""
from .base import *

DEBUG = True

try:
    import django_extensions  # noqa: F401
    INSTALLED_APPS += [
        'django_extensions',
    ]
except ImportError:
    pass

# Allow all hosts in development
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

# Disable HTTPS redirect in development
SECURE_SSL_REDIRECT = False

# Console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use local memory cache in development (no Redis required)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'msu-dev-cache',
        'KEY_PREFIX': 'msu_dev',
        'TIMEOUT': 300,
    }
}

# More verbose logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
