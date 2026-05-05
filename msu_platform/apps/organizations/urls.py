"""
URL configuration for organizations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClubViewSet, ChurchViewSet, SportsTeamViewSet, ActivityViewSet,
    PostViewSet, FeedViewSet, SearchViewSet
)

app_name = 'organizations'

router = DefaultRouter()
# Organization endpoints
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'churches', ChurchViewSet, basename='church')
router.register(r'sports-teams', SportsTeamViewSet, basename='sports-team')
router.register(r'activities', ActivityViewSet, basename='activity')

# Feed endpoints
router.register(r'posts', PostViewSet, basename='post')
router.register(r'feed', FeedViewSet, basename='feed')

# Search endpoint
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
