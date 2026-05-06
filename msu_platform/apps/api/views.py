"""
API root views.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    API Root discovery endpoint.
    """
    return Response({
        'status': 'online',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'login': reverse('api:users:login', request=request, format=format),
                'register': reverse('api:users:register', request=request, format=format),
                'refresh': reverse('api:users:token-refresh', request=request, format=format),
            },
            'organizations': {
                'clubs': reverse('api:organizations:club-list', request=request, format=format),
                'churches': reverse('api:organizations:church-list', request=request, format=format),
                'sports-teams': reverse('api:organizations:sports-team-list', request=request, format=format),
                'activities': reverse('api:organizations:activity-list', request=request, format=format),
            },
            'feed': {
                'posts': reverse('api:organizations:post-list', request=request, format=format),
                'latest': reverse('api:organizations:feed-list', request=request, format=format),
            },
            'search': reverse('api:organizations:search-list', request=request, format=format),
        }
    })
