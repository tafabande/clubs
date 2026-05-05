"""
Middleware for MSU Platform.
"""
from django.db import connection


class RLSMiddleware:
    """
    Set current user ID for PostgreSQL Row-Level Security (RLS) policies.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SET LOCAL app.current_user_id = %s",
                    [request.user.id]
                )

        response = self.get_response(request)
        return response
