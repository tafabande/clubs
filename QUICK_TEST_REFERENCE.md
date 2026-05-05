# Quick Test Reference Card

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=apps
```

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -x` | Stop on first failure |
| `pytest -k "user"` | Run tests matching "user" |
| `pytest -m authentication` | Run authentication tests |
| `pytest --cov=apps` | Run with coverage |
| `pytest apps/users/` | Test specific app |
| `pytest --pdb` | Debug on failure |
| `pytest -n auto` | Parallel execution |

## 🏷️ Test Markers

```python
@pytest.mark.authentication  # Auth tests
@pytest.mark.permissions     # Permission tests
@pytest.mark.feed           # Feed tests
@pytest.mark.search         # Search tests
@pytest.mark.media          # Media tests
@pytest.mark.slow           # Slow tests
@pytest.mark.integration    # Integration tests
```

## 🔧 Common Fixtures

```python
def test_example(
    api_client,              # Unauthenticated client
    authenticated_client,    # Authenticated client
    user,                    # Test user
    admin_user,             # Admin user
    club,                   # Test club
    post,                   # Test post
    mock_s3,                # Mocked S3
):
    pass
```

## 🛠️ Test Utilities

```python
from apps.core.tests.utils import (
    create_test_user,
    create_authenticated_client,
    create_test_club,
    create_test_post,
    assert_paginated_response,
)

# Create user
user = create_test_user(email='test@msu.ac.zw')

# Get authenticated client
client, user = create_authenticated_client()

# Create club
club = create_test_club(owner=user)

# Assert pagination
assert_paginated_response(response.data)
```

## 📝 Test Template

```python
import pytest
from django.urls import reverse
from rest_framework import status
from apps.core.tests.utils import create_test_user


@pytest.mark.django_db
class TestFeature:
    """Test feature functionality."""

    def test_success(self, authenticated_client, user):
        """Test successful operation."""
        # Arrange
        url = reverse('endpoint-name')
        data = {'key': 'value'}

        # Act
        response = authenticated_client.post(url, data, format='json')

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['key'] == 'value'

    def test_failure(self, authenticated_client):
        """Test failure case."""
        url = reverse('endpoint-name')
        data = {'invalid': 'data'}

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
```

## 🎯 API Test Pattern

Test these for each endpoint:
1. ✅ Success (200/201)
2. ✅ Unauthorized (401)
3. ✅ Forbidden (403)
4. ✅ Not Found (404)
5. ✅ Bad Request (400)
6. ✅ Pagination
7. ✅ Filtering
8. ✅ Permissions

## 📊 Coverage Commands

```bash
# Generate coverage report
pytest --cov=apps --cov-report=html

# View HTML report
open htmlcov/index.html

# Terminal report
pytest --cov=apps --cov-report=term-missing

# Exclude files
pytest --cov=apps --cov-report=html --cov-config=.coveragerc
```

## 🐛 Debugging

```bash
# Show print statements
pytest -s

# Drop to debugger on failure
pytest --pdb

# Drop to debugger at start
pytest --pdb-trace

# Show slowest tests
pytest --durations=10
```

## 📁 Test Structure

```
apps/
├── users/tests/
│   ├── test_models.py          # Model tests
│   ├── test_views.py           # View/API tests
│   ├── test_authentication.py  # Auth tests
│   └── test_follow.py          # Follow tests
├── organizations/tests/
│   ├── test_models.py
│   ├── test_club_views.py
│   ├── test_feed_views.py
│   ├── test_feed_algorithm.py
│   └── test_search_views.py
├── media/tests/
│   ├── test_models.py
│   └── test_tasks.py
└── core/tests/
    ├── test_cache.py
    └── utils.py                # Shared utilities
```

## 🔍 Finding Tests

```bash
# List all tests
pytest --collect-only

# List tests in file
pytest apps/users/tests/test_models.py --collect-only

# Find tests by name
pytest -k "create_user"

# Find tests by marker
pytest -m authentication --collect-only
```

## ⚡ Performance

```bash
# Run tests in parallel (4 workers)
pytest -n 4

# Auto-detect CPU cores
pytest -n auto

# Show slowest tests
pytest --durations=10

# Profile tests
pytest --profile
```

## 📦 Mocking Examples

```python
# Mock S3
def test_upload(mock_s3):
    mock_s3.return_value = 'file.jpg'
    # Test code

# Mock Celery
def test_task(mock_celery):
    mock_celery.return_value = Mock(id='123')
    # Test code

# Mock FFmpeg
def test_video(mock_ffmpeg):
    mock_ffmpeg.return_value = Mock(returncode=0)
    # Test code

# Mock time
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
def test_with_time():
    # Time is frozen
    pass
```

## 🎨 Assertions

```python
# Status codes
assert response.status_code == 200
assert response.status_code == status.HTTP_200_OK

# Response data
assert 'id' in response.data
assert response.data['name'] == 'Test'

# Database
assert User.objects.filter(email='test@msu.ac.zw').exists()
assert User.objects.count() == 1

# Pagination
assert_paginated_response(response.data)

# Lists
assert len(response.data['results']) == 5
assert any(item['id'] == '123' for item in response.data['results'])
```

## 🚨 Common Errors

| Error | Solution |
|-------|----------|
| `ImportError` | Check PYTHONPATH, verify imports |
| `DatabaseError` | Use `@pytest.mark.django_db` |
| `FixtureNotFound` | Check conftest.py location |
| `Slow tests` | Run with `-n auto` for parallel |
| `Coverage low` | Add more assertions, test edge cases |

## 📚 Resources

- **Full Guide**: See `TESTING_GUIDE.md`
- **Summary**: See `TEST_SUITE_SUMMARY.md`
- **Implementation**: See `TEST_IMPLEMENTATION_SUMMARY.md`

## 🎓 Best Practices

1. ✅ Test success and failure cases
2. ✅ Use descriptive test names
3. ✅ One logical assertion per test
4. ✅ Mock external services
5. ✅ Keep tests independent
6. ✅ Use fixtures for setup
7. ✅ Test edge cases
8. ✅ Maintain >80% coverage
9. ✅ Run tests before commit
10. ✅ Write tests for new features

## 🆘 Quick Help

```bash
# Get help
pytest --help

# List fixtures
pytest --fixtures

# List markers
pytest --markers

# Show configuration
pytest --version
pytest --showlocals
```

## 💡 Tips

- Use `-v` for better output
- Use `-x` to stop on first failure
- Use `--pdb` to debug failures
- Use `-k` to filter tests
- Use `-m` to run by marker
- Use `--cov` for coverage
- Use `-n auto` for speed

---

**Keep this card handy! 📌**
