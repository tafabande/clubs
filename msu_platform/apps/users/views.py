"""
Authentication views for MSU Platform.
"""
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken as JWT_RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django_ratelimit.decorators import ratelimit
import secrets

from .models import User, RefreshToken, UserSession, EmailVerificationToken, PasswordResetToken
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Create email verification token
        token = secrets.token_urlsafe(32)
        EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(days=1)
        )

        # TODO: Send verification email
        # send_verification_email(user.email, token)

        return Response({
            'message': 'User registered successfully. Please check your email to verify your account.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/15m', method='POST', block=True)
def login(request):
    """User login."""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = JWT_RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Store refresh token
        RefreshToken.objects.create(
            user=user,
            token=refresh_token,
            expires_at=timezone.now() + timedelta(days=7)
        )

        # Create user session
        device_info = request.META.get('HTTP_USER_AGENT', '')
        ip_address = get_client_ip(request)
        UserSession.objects.create(
            user=user,
            session_key=secrets.token_hex(20),
            device_info=device_info,
            ip_address=ip_address,
            expires_at=timezone.now() + timedelta(days=7)
        )

        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        response = Response({
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

        # Set cookies
        response.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=15 * 60  # 15 minutes
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=7 * 24 * 60 * 60  # 7 days
        )

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """User logout - revoke refresh token."""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken.objects.filter(token=refresh_token, user=request.user).first()
            if token:
                token.revoked = True
                token.save()

        # Delete user session
        UserSession.objects.filter(user=request.user, ip_address=get_client_ip(request)).delete()

        response = Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_all(request):
    """Logout from all devices - revoke all refresh tokens."""
    RefreshToken.objects.filter(user=request.user).update(revoked=True)
    UserSession.objects.filter(user=request.user).delete()

    return Response({'message': 'Logged out from all devices.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='10/h', method='GET', block=True)
def verify_email(request, token):
    """Verify user email."""
    try:
        verification = EmailVerificationToken.objects.get(token=token)
        if verification.is_valid():
            verification.verified = True
            verification.save()

            user = verification.user
            user.is_verified = True
            user.save(update_fields=['is_verified'])

            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token expired or already used.'}, status=status.HTTP_400_BAD_REQUEST)
    except EmailVerificationToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='3/h', method='POST', block=True)
def password_reset_request(request):
    """Request password reset."""
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)

            # Create password reset token
            token = secrets.token_urlsafe(32)
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(hours=1)
            )

            # TODO: Send password reset email
            # send_password_reset_email(user.email, token)

            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Don't reveal if user exists
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Confirm password reset."""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_valid():
                user = reset_token.user
                user.set_password(password)
                user.save()

                reset_token.used = True
                reset_token.save()

                # Revoke all sessions
                RefreshToken.objects.filter(user=user).update(revoked=True)
                UserSession.objects.filter(user=user).delete()

                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Token expired or already used.'}, status=status.HTTP_400_BAD_REQUEST)
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Get current user information."""
    return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom TokenRefreshView that reads refresh token from cookie
    and sets new access token in cookie.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Inject refresh token into request data for the serializer
            data = request.data.copy()
            data['refresh'] = refresh_token
            request._full_data = data # Internal hack for DRF request.data

        try:
            response = super().post(request, *args, **kwargs)
        except (InvalidToken, TokenError) as e:
            # Clear cookies on invalid token
            response = Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        if response.status_code == 200:
            access_token = response.data.get('access')
            # If refresh token is rotated
            new_refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access_token',
                access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=15 * 60
            )

            if new_refresh_token:
                response.set_cookie(
                    'refresh_token',
                    new_refresh_token,
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    max_age=7 * 24 * 60 * 60
                )
            
            # Remove tokens from response body for security
            if 'access' in response.data:
                del response.data['access']
            if 'refresh' in response.data:
                del response.data['refresh']

        return response
