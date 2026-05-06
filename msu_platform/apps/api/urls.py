"""
API URL configuration.
"""
from django.urls import path, include

app_name = 'api'

from .views import api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('auth/', include('apps.users.urls')),
    path('orgs/', include('apps.organizations.urls')),
]
