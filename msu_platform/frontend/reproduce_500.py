import os
import sys
import django
import uuid

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
sys.path.append(os.getcwd())
django.setup()

from apps.users.models import User
from apps.organizations.models import Post, Club
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIRequestFactory, force_authenticate
from apps.organizations.views.feed import PostViewSet

def reproduce():
    # Create test user
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    user = User.objects.create_user(username=username, email=email, password="password")
    
    # Create test organization
    club = Club.objects.create(
        name="Test Club",
        email="club@test.com",
        created_by=user
    )
    
    # Create test post
    ct = ContentType.objects.get_for_model(Club)
    post = Post.objects.create(
        content_type=ct,
        object_id=club.id,
        author=user,
        content="Test Content",
        visibility="public"
    )
    
    factory = APIRequestFactory()
    view = PostViewSet.as_view({'get': 'list'})
    request = factory.get('/api/orgs/posts/')
    force_authenticate(request, user=user)
    
    try:
        response = view(request)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.data}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
