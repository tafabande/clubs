#!/usr/bin/env python
"""
Verification script for MSU Platform test suite.
Checks that all test files, configuration, and utilities are in place.
"""
import os
import sys
from pathlib import Path


def check_file(path, description):
    """Check if a file exists."""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} - NOT FOUND")
        return False


def check_directory(path, description):
    """Check if a directory exists."""
    if os.path.isdir(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} - NOT FOUND")
        return False


def count_tests_in_file(filepath):
    """Count test functions in a file."""
    if not os.path.exists(filepath):
        return 0

    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip().startswith('def test_'):
                count += 1
    return count


def main():
    """Run verification checks."""
    print("=" * 70)
    print("MSU Platform Test Suite Verification")
    print("=" * 70)
    print()

    base_path = Path(__file__).parent
    checks_passed = 0
    checks_total = 0

    # Check configuration files
    print("📋 Configuration Files")
    print("-" * 70)

    config_files = [
        ('pytest.ini', 'Pytest configuration'),
        ('requirements-dev.txt', 'Development requirements'),
        ('msu_platform/config/settings/testing.py', 'Testing settings'),
        ('msu_platform/conftest.py', 'Pytest fixtures'),
    ]

    for filepath, description in config_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, description):
            checks_passed += 1

    print()

    # Check test utilities
    print("🔧 Test Utilities")
    print("-" * 70)

    util_files = [
        ('msu_platform/apps/core/tests/__init__.py', 'Core tests init'),
        ('msu_platform/apps/core/tests/utils.py', 'Test utilities'),
    ]

    for filepath, description in util_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, description):
            checks_passed += 1

    print()

    # Check user tests
    print("👤 User Tests")
    print("-" * 70)

    user_test_files = [
        'msu_platform/apps/users/tests/__init__.py',
        'msu_platform/apps/users/tests/test_models.py',
        'msu_platform/apps/users/tests/test_views.py',
        'msu_platform/apps/users/tests/test_authentication.py',
        'msu_platform/apps/users/tests/test_follow.py',
    ]

    user_test_count = 0
    for filepath in user_test_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, f"User test: {filepath.split('/')[-1]}"):
            checks_passed += 1
            user_test_count += count_tests_in_file(full_path)

    print(f"   Total test functions: {user_test_count}")
    print()

    # Check organization tests
    print("🏢 Organization Tests")
    print("-" * 70)

    org_test_files = [
        'msu_platform/apps/organizations/tests/__init__.py',
        'msu_platform/apps/organizations/tests/test_models.py',
        'msu_platform/apps/organizations/tests/test_club_views.py',
        'msu_platform/apps/organizations/tests/test_feed_views.py',
        'msu_platform/apps/organizations/tests/test_feed_algorithm.py',
        'msu_platform/apps/organizations/tests/test_search_views.py',
    ]

    org_test_count = 0
    for filepath in org_test_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, f"Org test: {filepath.split('/')[-1]}"):
            checks_passed += 1
            org_test_count += count_tests_in_file(full_path)

    print(f"   Total test functions: {org_test_count}")
    print()

    # Check media tests
    print("🎬 Media Tests")
    print("-" * 70)

    media_test_files = [
        'msu_platform/apps/media/tests/__init__.py',
        'msu_platform/apps/media/tests/test_models.py',
        'msu_platform/apps/media/tests/test_tasks.py',
    ]

    media_test_count = 0
    for filepath in media_test_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, f"Media test: {filepath.split('/')[-1]}"):
            checks_passed += 1
            media_test_count += count_tests_in_file(full_path)

    print(f"   Total test functions: {media_test_count}")
    print()

    # Check core tests
    print("⚙️  Core Tests")
    print("-" * 70)

    core_test_files = [
        'msu_platform/apps/core/tests/test_cache.py',
    ]

    core_test_count = 0
    for filepath in core_test_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, f"Core test: {filepath.split('/')[-1]}"):
            checks_passed += 1
            core_test_count += count_tests_in_file(full_path)

    print(f"   Total test functions: {core_test_count}")
    print()

    # Check documentation
    print("📚 Documentation")
    print("-" * 70)

    doc_files = [
        ('TESTING_GUIDE.md', 'Testing guide'),
        ('TEST_SUITE_SUMMARY.md', 'Test suite summary'),
        ('TEST_IMPLEMENTATION_SUMMARY.md', 'Implementation summary'),
        ('QUICK_TEST_REFERENCE.md', 'Quick reference'),
    ]

    for filepath, description in doc_files:
        full_path = base_path / filepath
        checks_total += 1
        if check_file(full_path, description):
            checks_passed += 1

    print()

    # Summary
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"Checks passed: {checks_passed}/{checks_total}")
    print(f"Success rate: {(checks_passed/checks_total)*100:.1f}%")
    print()

    total_tests = user_test_count + org_test_count + media_test_count + core_test_count
    print(f"Total test functions found: {total_tests}")
    print()

    if checks_passed == checks_total:
        print("✅ All checks passed! Test suite is ready.")
        print()
        print("Next steps:")
        print("  1. Install dependencies: pip install -r requirements-dev.txt")
        print("  2. Run tests: pytest")
        print("  3. Check coverage: pytest --cov=apps")
        print("  4. Read TESTING_GUIDE.md for more information")
        return 0
    else:
        print("❌ Some checks failed. Please review the output above.")
        print(f"   Missing: {checks_total - checks_passed} files")
        return 1


if __name__ == '__main__':
    sys.exit(main())
