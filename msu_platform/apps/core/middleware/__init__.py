"""Middleware package for MSU Platform."""
from .error_logging import ErrorLoggingMiddleware

__all__ = ['ErrorLoggingMiddleware']
