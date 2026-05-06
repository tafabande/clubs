"""Middleware package for MSU Platform."""
from .error_logging import ErrorLoggingMiddleware


class RLSMiddleware:
    """
    Set current user ID for PostgreSQL Row-Level Security (RLS) policies.
    Safely skips on non-PostgreSQL backends (e.g. SQLite).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            from django.db import connection
            if connection.vendor == 'postgresql':
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT set_config('app.current_user_id', %s, true)",
                        [str(request.user.id)]
                    )

        response = self.get_response(request)
        return response


__all__ = ['ErrorLoggingMiddleware', 'RLSMiddleware']
