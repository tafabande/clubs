# MSU Platform Testing Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Running Tests](#running-tests)
3. [Test Structure](#test-structure)
4. [Writing Tests](#writing-tests)
5. [Test Utilities](#test-utilities)
6. [Coverage Reports](#coverage-reports)
7. [CI/CD Integration](#cicd-integration)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

1. **Install Development Dependencies:**
```bash
pip install -r requirements-dev.txt
```

This includes:
- pytest & pytest-django
- pytest-cov (coverage)
- pytest-mock (mocking)
- factory-boy (test data)
- faker (fake data generation)

2. **Verify Installation:**
```bash
pytest --version
```

### Configuration

Tests are configured via:
- **pytest.ini** - Main pytest configuration
- **config/settings/testing.py** - Django test settings
- **conftest.py** - Shared fixtures

## Running Tests

### Basic Commands

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest apps/users/tests/test_models.py
```

**Run specific test class:**
```bash
pytest apps/users/tests/test_models.py::TestUserModel
```

**Run specific test method:**
```bash
pytest apps/users/tests/test_models.py::TestUserModel::test_create_user
```

**Run by marker:**
```bash
pytest -m authentication  # Only authentication tests
pytest -m feed           # Only feed tests
pytest -m "not slow"     # Skip slow tests
```

### Test Markers

Available markers:
- `@pytest.mark.authentication` - Authentication tests
- `@pytest.mark.permissions` - Permission tests
- `@pytest.mark.feed` - Feed algorithm tests
- `@pytest.mark.search` - Search functionality tests
- `@pytest.mark.media` - Media processing tests
- `@pytest.mark.slow` - Slow tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.unit` - Unit tests

### Parallel Testing

Run tests in parallel for faster execution:
```bash
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 workers
```

### Stop on First Failure

```bash
pytest -x  # Stop on first failure
pytest --maxfail=3  # Stop after 3 failures
```

### Filtering Tests

**By keyword:**
```bash
pytest -k "user"  # Run tests with "user" in name
pytest -k "not integration"  # Skip integration tests
```

**By app:**
```bash
pytest apps/users/
pytest apps/organizations/
pytest apps/media/
```

## Test Structure

```
msu_platform/
├── apps/
│   ├── users/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       ├── test_authentication.py
│   │       └── test_follow.py
│   ├── organizations/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_club_views.py
│   │       ├── test_feed_views.py
│   │       ├── test_feed_algorithm.py
│   │       └── test_search_views.py
│   ├── media/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       └── test_tasks.py
│   └── core/
│       └── tests/
│           ├── __init__.py
│           ├── test_cache.py
│           └── utils.py  # Shared test utilities
├── conftest.py
└── pytest.ini
```

## Writing Tests

### Basic Test Structure

```python
import pytest
from django.contrib.auth import get_user_model
from apps.core.tests.utils import create_test_user

User = get_user_model()


@pytest.mark.django_db
class TestUserFeature:
    """Test user feature functionality."""

    def test_feature_success(self, authenticated_client, user):
        """Test successful feature execution."""
        # Arrange
        url = '/api/endpoint/'
        data = {'key': 'value'}

        # Act
        response = authenticated_client.post(url, data, format='json')

        # Assert
        assert response.status_code == 200
        assert response.data['key'] == 'value'

    def test_feature_failure(self, authenticated_client):
        """Test feature failure case."""
        url = '/api/endpoint/'
        data = {'invalid': 'data'}

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == 400
```

### Using Fixtures

**Available fixtures (from conftest.py):**

```python
def test_with_fixtures(
    api_client,              # Unauthenticated client
    authenticated_client,    # Authenticated client
    user,                    # Test user
    user2,                   # Second test user
    admin_user,             # Admin user
    club,                   # Test club
    church,                 # Test church
    sports_team,            # Test sports team
    activity,               # Test activity
    post,                   # Test post
    comment,                # Test comment
    mock_s3,                # Mocked S3
    mock_celery,            # Mocked Celery
    mock_ffmpeg,            # Mocked FFmpeg
):
    # Your test code
    pass
```

### Using Test Utilities

```python
from apps.core.tests.utils import (
    create_test_user,
    create_authenticated_client,
    create_test_club,
    assert_paginated_response,
)

def test_example():
    # Create users
    user = create_test_user(email='test@msu.ac.zw')
    admin = create_test_user(is_staff=True, is_superuser=True)

    # Get authenticated client
    client, user = create_authenticated_client()

    # Create organizations
    club = create_test_club(owner=user, name='Tech Club')

    # Assert pagination
    response = client.get('/api/clubs/')
    assert_paginated_response(response.data)
```

### Mocking External Services

**Mock S3:**
```python
def test_upload(authenticated_client, mock_s3):
    """Test file upload with mocked S3."""
    mock_s3.return_value = 'test_file.jpg'

    # Your test code
    # S3 operations will be mocked
```

**Mock Celery:**
```python
def test_async_task(mock_celery):
    """Test Celery task with mock."""
    mock_celery.return_value = Mock(id='task-id')

    # Your test code
    # Celery tasks won't actually run
```

**Mock FFmpeg:**
```python
def test_video_processing(mock_ffmpeg):
    """Test video processing with mocked FFmpeg."""
    mock_ffmpeg.return_value = Mock(returncode=0)

    # Your test code
    # FFmpeg won't actually run
```

### Testing API Endpoints

**Complete endpoint test pattern:**

```python
@pytest.mark.django_db
class TestClubEndpoint:
    """Test Club API endpoint."""

    def test_list_success(self, authenticated_client):
        """Test successful list."""
        response = authenticated_client.get('/api/clubs/')
        assert response.status_code == 200

    def test_list_unauthenticated(self, api_client):
        """Test list without authentication."""
        response = api_client.get('/api/clubs/')
        assert response.status_code == 401

    def test_create_success(self, authenticated_client):
        """Test successful creation."""
        data = {'name': 'Test Club'}
        response = authenticated_client.post('/api/clubs/', data)
        assert response.status_code == 201

    def test_create_invalid_data(self, authenticated_client):
        """Test creation with invalid data."""
        data = {'name': ''}
        response = authenticated_client.post('/api/clubs/', data)
        assert response.status_code == 400

    def test_update_owner(self, authenticated_client, user):
        """Test update by owner."""
        club = create_test_club(owner=user)
        data = {'name': 'Updated'}
        response = authenticated_client.patch(f'/api/clubs/{club.id}/', data)
        assert response.status_code == 200

    def test_update_non_owner(self, authenticated_client):
        """Test update by non-owner."""
        other_user = create_test_user()
        club = create_test_club(owner=other_user)
        data = {'name': 'Hacked'}
        response = authenticated_client.patch(f'/api/clubs/{club.id}/', data)
        assert response.status_code == 403

    def test_delete_owner(self, authenticated_client, user):
        """Test deletion by owner."""
        club = create_test_club(owner=user)
        response = authenticated_client.delete(f'/api/clubs/{club.id}/')
        assert response.status_code == 204

    def test_not_found(self, authenticated_client):
        """Test 404 for non-existent resource."""
        response = authenticated_client.get('/api/clubs/invalid-id/')
        assert response.status_code == 404
```

## Test Utilities

### Creating Test Data

**Users:**
```python
from apps.core.tests.utils import create_test_user

# Basic user
user = create_test_user()

# Custom user
user = create_test_user(
    email='custom@msu.ac.zw',
    first_name='John',
    last_name='Doe',
    faculty='science',
    year_of_study=3,
    is_verified=True
)

# Admin user
admin = create_test_user(is_staff=True, is_superuser=True)
```

**Organizations:**
```python
from apps.core.tests.utils import (
    create_test_club,
    create_test_church,
    create_test_sports_team,
)

# Club
club = create_test_club(
    owner=user,
    name='Tech Club',
    category='academic'
)

# Church
church = create_test_church(
    owner=user,
    denomination='catholic'
)

# Sports team
team = create_test_sports_team(
    owner=user,
    sport_type='football'
)
```

**Content:**
```python
from apps.core.tests.utils import (
    create_test_post,
    create_test_comment,
    create_test_activity,
)

# Post
post = create_test_post(
    author=user,
    organization=club,
    post_type='text',
    content='Test post'
)

# Comment
comment = create_test_comment(
    author=user,
    post=post,
    content='Great post!'
)

# Activity
activity = create_test_activity(
    organization=club,
    title='Workshop',
    capacity=50
)
```

### Assertions

**Paginated response:**
```python
from apps.core.tests.utils import assert_paginated_response

response = client.get('/api/clubs/')
assert_paginated_response(response.data)
# Checks for: count, next, previous, results
```

**Response keys:**
```python
from apps.core.tests.utils import assert_response_keys

assert_response_keys(response.data, ['id', 'name', 'description'])
```

## Coverage Reports

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=apps

# Generate HTML report
pytest --cov=apps --cov-report=html

# Generate terminal report
pytest --cov=apps --cov-report=term-missing

# Combined
pytest --cov=apps --cov-report=html --cov-report=term-missing
```

### View HTML Coverage Report

```bash
# After generating HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Configuration

Coverage is configured in `pytest.ini`:
```ini
[pytest]
addopts =
    --cov=apps
    --cov-report=html
    --cov-report=term-missing:skip-covered
```

### Coverage Thresholds

Aim for:
- **Overall**: >80%
- **Critical paths**: >95%
- **New code**: 100%

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        run: |
          pytest --cov=apps --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running tests..."
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Troubleshooting

### Common Issues

**1. Database errors:**
```bash
# Reset test database
pytest --create-db
```

**2. Import errors:**
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**3. Fixtures not found:**
```bash
# Verify conftest.py is in correct location
ls msu_platform/conftest.py
```

**4. Slow tests:**
```bash
# Run with duration report
pytest --durations=10

# Skip slow tests
pytest -m "not slow"
```

**5. Permission errors:**
```bash
# Check file permissions
chmod +x manage.py
```

### Debug Mode

**Run with debugging:**
```bash
pytest -vv  # Very verbose
pytest -s   # Show print statements
pytest --pdb  # Drop to debugger on failure
pytest --pdb-trace  # Drop to debugger at start
```

**Use pytest-ipdb:**
```python
def test_example():
    import ipdb; ipdb.set_trace()
    # Debug from here
```

### Performance Issues

**Identify slow tests:**
```bash
pytest --durations=0  # Show all durations
pytest --durations=20  # Show slowest 20
```

**Profile tests:**
```bash
pytest --profile
pytest --profile-svg  # Generate SVG profile
```

## Best Practices

1. **One assertion per test** (when possible)
2. **Use descriptive test names**
3. **Follow AAA pattern** (Arrange, Act, Assert)
4. **Test both success and failure cases**
5. **Mock external dependencies**
6. **Keep tests independent**
7. **Use fixtures for common setup**
8. **Test edge cases**
9. **Maintain >80% coverage**
10. **Run tests before committing**

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Django Testing Guide](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [DRF Testing Guide](https://www.django-rest-framework.org/api-guide/testing/)

## Support

For issues or questions:
1. Check this guide
2. Review test examples
3. Check pytest/Django documentation
4. Ask the team

---

**Happy Testing! 🧪**
