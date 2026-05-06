"""
URL configuration for users app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('logout-all/', views.logout_all, name='logout-all'),
    path('refresh/', views.CookieTokenRefreshView.as_view(), name='token-refresh'),

    # Email verification
    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),

    # Password reset
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset-confirm/', views.password_reset_confirm, name='password-reset-confirm'),

    # User info
    path('me/', views.me, name='me'),
]
