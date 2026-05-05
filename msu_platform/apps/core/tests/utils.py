"""
Test utilities and fixtures for MSU Platform tests.
"""
import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_test_user(
    email: Optional[str] = None,
    password: str = "testpass123",
    first_name: str = "Test",
    last_name: str = "User",
    is_verified: bool = True,
    **extra_fields
) -> User:
    """
    Create a test user with default values.

    Args:
        email: User email (auto-generated if not provided)
        password: User password
        first_name: User first name
        last_name: User last name
        is_verified: Whether user email is verified
        **extra_fields: Additional fields for user creation

    Returns:
        User instance
    """
    if not email:
        email = f"test_{uuid.uuid4().hex[:8]}@msu.ac.zw"

    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'is_verified': is_verified,
        **extra_fields
    }

    user = User.objects.create_user(email=email, password=password, **user_data)
    return user


def create_authenticated_client(user: Optional[User] = None) -> tuple[APIClient, User]:
    """
    Create an authenticated API client with JWT token.

    Args:
        user: User instance (creates new user if not provided)

    Returns:
        Tuple of (APIClient, User)
    """
    if user is None:
        user = create_test_user()

    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    return client, user


def create_test_club(
    owner: Optional[User] = None,
    name: Optional[str] = None,
    **extra_fields
) -> Any:
    """
    Create a test club.

    Args:
        owner: Club owner (creates new user if not provided)
        name: Club name (auto-generated if not provided)
        **extra_fields: Additional fields for club creation

    Returns:
        Club instance
    """
    from apps.organizations.models import Club

    if owner is None:
        owner = create_test_user()

    if name is None:
        name = f"Test Club {uuid.uuid4().hex[:8]}"

    club_data = {
        'name': name,
        'description': 'Test club description',
        'category': 'academic',
        'owner': owner,
        **extra_fields
    }

    club = Club.objects.create(**club_data)
    return club


def create_test_church(
    owner: Optional[User] = None,
    name: Optional[str] = None,
    **extra_fields
) -> Any:
    """
    Create a test church.

    Args:
        owner: Church owner (creates new user if not provided)
        name: Church name (auto-generated if not provided)
        **extra_fields: Additional fields for church creation

    Returns:
        Church instance
    """
    from apps.organizations.models import Church

    if owner is None:
        owner = create_test_user()

    if name is None:
        name = f"Test Church {uuid.uuid4().hex[:8]}"

    church_data = {
        'name': name,
        'description': 'Test church description',
        'denomination': 'catholic',
        'owner': owner,
        **extra_fields
    }

    church = Church.objects.create(**church_data)
    return church


def create_test_sports_team(
    owner: Optional[User] = None,
    name: Optional[str] = None,
    **extra_fields
) -> Any:
    """
    Create a test sports team.

    Args:
        owner: Team owner (creates new user if not provided)
        name: Team name (auto-generated if not provided)
        **extra_fields: Additional fields for sports team creation

    Returns:
        SportsTeam instance
    """
    from apps.organizations.models import SportsTeam

    if owner is None:
        owner = create_test_user()

    if name is None:
        name = f"Test Team {uuid.uuid4().hex[:8]}"

    team_data = {
        'name': name,
        'description': 'Test sports team description',
        'sport_type': 'football',
        'owner': owner,
        **extra_fields
    }

    team = SportsTeam.objects.create(**team_data)
    return team


def create_test_activity(
    organization: Optional[Any] = None,
    title: Optional[str] = None,
    **extra_fields
) -> Any:
    """
    Create a test activity.

    Args:
        organization: Organization instance (creates club if not provided)
        title: Activity title (auto-generated if not provided)
        **extra_fields: Additional fields for activity creation

    Returns:
        Activity instance
    """
    from apps.organizations.models import Activity

    if organization is None:
        organization = create_test_club()

    if title is None:
        title = f"Test Activity {uuid.uuid4().hex[:8]}"

    activity_data = {
        'title': title,
        'description': 'Test activity description',
        'organization': organization,
        'start_time': timezone.now() + timedelta(days=7),
        'end_time': timezone.now() + timedelta(days=7, hours=2),
        'location': 'Test Location',
        **extra_fields
    }

    activity = Activity.objects.create(**activity_data)
    return activity


def create_test_post(
    author: Optional[User] = None,
    organization: Optional[Any] = None,
    post_type: str = 'text',
    **extra_fields
) -> Any:
    """
    Create a test post.

    Args:
        author: Post author (creates new user if not provided)
        organization: Organization instance (creates club if not provided)
        post_type: Type of post (text, image, video, etc.)
        **extra_fields: Additional fields for post creation

    Returns:
        Post instance
    """
    from apps.organizations.models import Post

    if author is None:
        author = create_test_user()

    if organization is None:
        organization = create_test_club()

    post_data = {
        'author': author,
        'organization': organization,
        'post_type': post_type,
        'content': 'Test post content',
        **extra_fields
    }

    post = Post.objects.create(**post_data)
    return post


def create_test_comment(
    author: Optional[User] = None,
    post: Optional[Any] = None,
    content: str = "Test comment",
    parent: Optional[Any] = None,
    **extra_fields
) -> Any:
    """
    Create a test comment.

    Args:
        author: Comment author (creates new user if not provided)
        post: Post instance (creates new post if not provided)
        content: Comment content
        parent: Parent comment for replies
        **extra_fields: Additional fields for comment creation

    Returns:
        Comment instance
    """
    from apps.organizations.models import Comment

    if author is None:
        author = create_test_user()

    if post is None:
        post = create_test_post()

    comment_data = {
        'author': author,
        'post': post,
        'content': content,
        'parent': parent,
        **extra_fields
    }

    comment = Comment.objects.create(**comment_data)
    return comment


def create_test_video_job(**extra_fields) -> Any:
    """
    Create a test video transcoding job.

    Args:
        **extra_fields: Additional fields for job creation

    Returns:
        VideoTranscodingJob instance
    """
    from apps.media.models import VideoTranscodingJob

    job_data = {
        'source_url': 'https://example.com/test_video.mp4',
        'status': 'pending',
        **extra_fields
    }

    job = VideoTranscodingJob.objects.create(**job_data)
    return job


def get_auth_header(user: User) -> Dict[str, str]:
    """
    Get authentication header for user.

    Args:
        user: User instance

    Returns:
        Dictionary with Authorization header
    """
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}


def assert_response_keys(response_data: Dict, expected_keys: list):
    """
    Assert that response data contains expected keys.

    Args:
        response_data: Response data dictionary
        expected_keys: List of expected keys
    """
    assert set(expected_keys).issubset(set(response_data.keys())), \
        f"Missing keys: {set(expected_keys) - set(response_data.keys())}"


def assert_paginated_response(response_data: Dict):
    """
    Assert that response is properly paginated.

    Args:
        response_data: Response data dictionary
    """
    required_keys = ['count', 'next', 'previous', 'results']
    assert_response_keys(response_data, required_keys)
    assert isinstance(response_data['results'], list)


def create_refresh_token(user: User, revoked: bool = False) -> Any:
    """
    Create a refresh token for user.

    Args:
        user: User instance
        revoked: Whether token is revoked

    Returns:
        RefreshToken instance
    """
    from apps.users.models import RefreshToken as RefreshTokenModel

    token = RefreshToken.for_user(user)

    refresh_token = RefreshTokenModel.objects.create(
        user=user,
        token=str(token),
        expires_at=timezone.now() + timedelta(days=7),
        revoked=revoked
    )

    return refresh_token


def create_password_reset_token(user: User, used: bool = False) -> Any:
    """
    Create a password reset token for user.

    Args:
        user: User instance
        used: Whether token has been used

    Returns:
        PasswordResetToken instance
    """
    from apps.users.models import PasswordResetToken

    token = PasswordResetToken.objects.create(
        user=user,
        token=uuid.uuid4().hex,
        expires_at=timezone.now() + timedelta(hours=24),
        used=used
    )

    return token


def create_email_verification_token(user: User, verified: bool = False) -> Any:
    """
    Create an email verification token for user.

    Args:
        user: User instance
        verified: Whether token has been verified

    Returns:
        EmailVerificationToken instance
    """
    from apps.users.models import EmailVerificationToken

    token = EmailVerificationToken.objects.create(
        user=user,
        token=uuid.uuid4().hex,
        expires_at=timezone.now() + timedelta(days=7),
        verified=verified
    )

    return token
