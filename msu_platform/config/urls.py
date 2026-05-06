"""
URL configuration for MSU Platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import health

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),

    # Health check endpoints
    path('health/', health.health_check, name='health_check'),
    path('health/detailed/', health.health_check_detailed, name='health_check_detailed'),
    path('health/db/', health.health_check_database, name='health_check_database'),
    path('health/redis/', health.health_check_redis, name='health_check_redis'),
    path('health/celery/', health.health_check_celery, name='health_check_celery'),
    path('health/storage/', health.health_check_storage, name='health_check_storage'),
    path('ready/', health.readiness_check, name='readiness_check'),
    path('alive/', health.liveness_check, name='liveness_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
