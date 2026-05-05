"""
Pytest configuration and fixtures for MSU Platform tests.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.core.tests.utils import (
    create_test_user,
    create_authenticated_client,
    create_test_club,
    create_test_church,
    create_test_sports_team,
    create_test_activity,
    create_test_post,
    create_test_comment,
)

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def user():
    """Create a test user."""
    return create_test_user()


@pytest.fixture
def user2():
    """Create a second test user."""
    return create_test_user(email="user2@msu.ac.zw")


@pytest.fixture
def user3():
    """Create a third test user."""
    return create_test_user(email="user3@msu.ac.zw")


@pytest.fixture
def authenticated_client(user):
    """Return an authenticated API client."""
    client, _ = create_authenticated_client(user)
    return client


@pytest.fixture
def authenticated_client_with_user():
    """Return an authenticated API client with user."""
    return create_authenticated_client()


@pytest.fixture
def admin_user():
    """Create an admin user."""
    return create_test_user(
        email="admin@msu.ac.zw",
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def club(user):
    """Create a test club."""
    return create_test_club(owner=user)


@pytest.fixture
def church(user):
    """Create a test church."""
    return create_test_church(owner=user)


@pytest.fixture
def sports_team(user):
    """Create a test sports team."""
    return create_test_sports_team(owner=user)


@pytest.fixture
def activity(club):
    """Create a test activity."""
    return create_test_activity(organization=club)


@pytest.fixture
def post(user, club):
    """Create a test post."""
    return create_test_post(author=user, organization=club)


@pytest.fixture
def comment(user, post):
    """Create a test comment."""
    return create_test_comment(author=user, post=post)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass


@pytest.fixture
def mock_s3(mocker):
    """Mock S3 storage operations."""
    mock = mocker.patch('apps.core.storage.MediaStorage.save')
    mock.return_value = 'test_file.jpg'
    return mock


@pytest.fixture
def mock_celery(mocker):
    """Mock Celery task execution."""
    return mocker.patch('celery.app.task.Task.apply_async')


@pytest.fixture
def mock_ffmpeg(mocker):
    """Mock FFmpeg for video processing."""
    return mocker.patch('subprocess.run')
