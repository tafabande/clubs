"""
Custom throttling classes for MSU Platform API.
"""
from rest_framework.throttling import SimpleRateThrottle


class APIThrottle(SimpleRateThrottle):
    """
    General API throttle: 500 requests per hour per user.
    """
    scope = 'api'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
