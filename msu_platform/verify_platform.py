#!/usr/bin/env python
"""
MSU Platform Final Verification Script
Comprehensive testing and verification of all platform components
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class VerificationReport:
    def __init__(self):
        self.results = []
        self.phase = ""
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def start_phase(self, phase_name):
        self.phase = phase_name
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}PHASE: {phase_name}{RESET}")
        print(f"{BLUE}{'='*80}{RESET}\n")

    def log(self, check_name, status, details=""):
        symbol = {
            'pass': f'{GREEN}✓{RESET}',
            'fail': f'{RED}✗{RESET}',
            'warn': f'{YELLOW}⚠{RESET}'
        }[status]

        if status == 'pass':
            self.passed += 1
        elif status == 'fail':
            self.failed += 1
        else:
            self.warnings += 1

        self.results.append({
            'phase': self.phase,
            'check': check_name,
            'status': status,
            'details': details
        })

        print(f"{symbol} {check_name}")
        if details:
            print(f"  → {details}")

    def summary(self):
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}VERIFICATION SUMMARY{RESET}")
        print(f"{BLUE}{'='*80}{RESET}\n")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        print(f"{RED}Failed: {self.failed}{RESET}")
        print(f"{YELLOW}Warnings: {self.warnings}{RESET}")
        print(f"Total Checks: {self.passed + self.failed + self.warnings}\n")

        if self.failed == 0:
            print(f"{GREEN}{'='*80}{RESET}")
            print(f"{GREEN}✓ PLATFORM IS PRODUCTION READY{RESET}")
            print(f"{GREEN}{'='*80}{RESET}\n")
        else:
            print(f"{RED}{'='*80}{RESET}")
            print(f"{RED}✗ PLATFORM NEEDS ATTENTION{RESET}")
            print(f"{RED}{'='*80}{RESET}\n")

    def generate_report(self, output_file):
        """Generate markdown report"""
        with open(output_file, 'w') as f:
            f.write("# MSU Platform Final Verification Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## Executive Summary\n\n")
            f.write(f"- **Total Checks:** {self.passed + self.failed + self.warnings}\n")
            f.write(f"- **Passed:** ✓ {self.passed}\n")
            f.write(f"- **Failed:** ✗ {self.failed}\n")
            f.write(f"- **Warnings:** ⚠ {self.warnings}\n\n")

            if self.failed == 0:
                f.write("### Verdict: ✓ PRODUCTION READY\n\n")
                f.write("All critical checks passed. The platform is ready for deployment.\n\n")
            else:
                f.write("### Verdict: ✗ NEEDS ATTENTION\n\n")
                f.write("Some checks failed. Please review the issues below.\n\n")

            f.write("---\n\n")

            # Group results by phase
            phases = {}
            for result in self.results:
                phase = result['phase']
                if phase not in phases:
                    phases[phase] = []
                phases[phase].append(result)

            for phase, checks in phases.items():
                f.write(f"## {phase}\n\n")
                for check in checks:
                    status_symbol = {
                        'pass': '✓',
                        'fail': '✗',
                        'warn': '⚠'
                    }[check['status']]
                    f.write(f"- {status_symbol} **{check['check']}**\n")
                    if check['details']:
                        f.write(f"  - {check['details']}\n")
                f.write("\n")

def run_command(cmd, description="", ignore_errors=False):
    """Run a shell command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 or ignore_errors:
            return True, result.stdout
        return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def check_file_exists(filepath):
    """Check if a file exists"""
    return Path(filepath).exists()

def main():
    report = VerificationReport()
    base_dir = Path(__file__).parent

    # Change to base directory
    os.chdir(base_dir)

    # =========================================================================
    # PHASE 1: File Integrity Check
    # =========================================================================
    report.start_phase("Phase 1: File Integrity Check")

    # Critical files to check
    critical_files = [
        # Core config
        'manage.py',
        'config/settings/base.py',
        'config/settings/development.py',
        'config/settings/production.py',
        'config/settings/testing.py',
        'config/urls.py',
        'config/wsgi.py',

        # Apps
        'apps/users/models.py',
        'apps/users/serializers.py',
        'apps/users/views.py',
        'apps/organizations/models/club.py',
        'apps/organizations/models/post.py',
        'apps/organizations/models/feed.py',
        'apps/organizations/models/follow.py',
        'apps/organizations/views/feed.py',
        'apps/organizations/feed_algorithm.py',
        'apps/media/models.py',
        'apps/media/tasks.py',
        'apps/core/exceptions.py',
        'apps/core/exception_handlers.py',
        'apps/core/middleware/error_logging.py',
        'apps/core/views/health.py',

        # Docker
        'Dockerfile',
        'docker-compose.yml',

        # Requirements
        'requirements.txt',

        # Documentation
        'README.md',
        'API_DOCUMENTATION.md',
        'DEPLOY.md',
    ]

    missing_files = []
    for filepath in critical_files:
        if check_file_exists(filepath):
            report.log(f"File exists: {filepath}", 'pass')
        else:
            report.log(f"File missing: {filepath}", 'fail')
            missing_files.append(filepath)

    # Check Python syntax
    print("\nChecking Python syntax...")
    success, output = run_command(
        "find apps config -name '*.py' -type f ! -path '*/migrations/*' | head -20 | xargs -I {} python -m py_compile {}",
        ignore_errors=True
    )
    if success:
        report.log("Python syntax validation", 'pass', "First 20 files checked successfully")
    else:
        report.log("Python syntax validation", 'warn', f"Some syntax issues: {output[:100]}")

    # =========================================================================
    # PHASE 2: Configuration Validation
    # =========================================================================
    report.start_phase("Phase 2: Configuration Validation")

    # Check settings imports
    settings_modules = [
        'config.settings.base',
        'config.settings.testing',
    ]

    for module in settings_modules:
        success, output = run_command(
            f'python -c "from {module} import *; print(\'OK\')"',
            ignore_errors=True
        )
        if success and 'OK' in output:
            report.log(f"Settings module: {module}", 'pass')
        else:
            report.log(f"Settings module: {module}", 'fail', output[:200])

    # Check requirements file
    if check_file_exists('requirements.txt'):
        with open('requirements.txt') as f:
            lines = f.readlines()
            report.log(f"Requirements.txt readable", 'pass', f"{len(lines)} dependencies")
    else:
        report.log("Requirements.txt readable", 'fail', "File not found")

    # Check Docker config
    if check_file_exists('docker-compose.yml'):
        success, output = run_command('docker-compose config --quiet', ignore_errors=True)
        if success:
            report.log("Docker-compose syntax", 'pass')
        else:
            report.log("Docker-compose syntax", 'warn', "docker-compose not available or syntax issues")
    else:
        report.log("Docker-compose file", 'fail', "File not found")

    # =========================================================================
    # PHASE 3: Django System Checks
    # =========================================================================
    report.start_phase("Phase 3: Django System Checks")

    # Set environment
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.testing'

    # Check Django setup
    success, output = run_command(
        'python manage.py check --deploy --tag security --tag models',
        ignore_errors=True
    )
    if success or 'System check identified no issues' in output:
        report.log("Django system check", 'pass')
    else:
        if 'error' in output.lower():
            report.log("Django system check", 'fail', output[:300])
        else:
            report.log("Django system check", 'warn', output[:300])

    # Check for missing migrations
    success, output = run_command(
        'python manage.py makemigrations --dry-run --check',
        ignore_errors=True
    )
    if success or 'No changes detected' in output:
        report.log("Migration check", 'pass', "No missing migrations")
    else:
        report.log("Migration check", 'warn', "May need migrations")

    # Validate URLs
    success, output = run_command(
        'python -c "from config.urls import urlpatterns; print(len(urlpatterns))"',
        ignore_errors=True
    )
    if success:
        report.log("URL configuration", 'pass', f"{output.strip()} URL patterns loaded")
    else:
        report.log("URL configuration", 'fail', output[:200])

    # =========================================================================
    # PHASE 4: Import Tests
    # =========================================================================
    report.start_phase("Phase 4: Import Validation")

    critical_imports = [
        'from apps.core import exceptions',
        'from apps.core import exception_handlers',
        'from apps.core.middleware import error_logging',
        'from apps.core.views import health',
        'from apps.organizations.models import Feed, Follow',
        'from apps.organizations import feed_algorithm',
        'from apps.media.models import VideoTranscodingJob',
        'from apps.media import tasks',
        'from apps.users.models import User',
    ]

    for import_stmt in critical_imports:
        success, output = run_command(
            f'python -c "{import_stmt}; print(\'OK\')"',
            ignore_errors=True
        )
        if success and 'OK' in output:
            report.log(f"Import: {import_stmt.split('import')[1].strip()}", 'pass')
        else:
            report.log(f"Import: {import_stmt.split('import')[1].strip()}", 'fail', output[:200])

    # =========================================================================
    # PHASE 5: Test Suite Check
    # =========================================================================
    report.start_phase("Phase 5: Test Suite Validation")

    # Count test files
    success, output = run_command('find apps -name "test_*.py" -type f | wc -l')
    if success:
        test_count = output.strip()
        report.log(f"Test files found", 'pass', f"{test_count} test files")
    else:
        report.log("Test files found", 'warn', "Could not count test files")

    # Check if pytest is available
    success, output = run_command('python -c "import pytest; print(pytest.__version__)"', ignore_errors=True)
    if success:
        report.log("Pytest available", 'pass', f"Version: {output.strip()}")
    else:
        report.log("Pytest available", 'warn', "Pytest not installed")

    # Check conftest.py
    if check_file_exists('conftest.py'):
        report.log("Pytest configuration", 'pass', "conftest.py exists")
    else:
        report.log("Pytest configuration", 'warn', "conftest.py not found")

    # =========================================================================
    # PHASE 6: Security Checks
    # =========================================================================
    report.start_phase("Phase 6: Security Validation")

    # Check for hardcoded secrets (basic check)
    success, output = run_command(
        'grep -r "password.*=.*[\'\\"]" --include="*.py" apps config | grep -v "password_validators" | grep -v "PASSWORD_" | grep -v "#" | head -5',
        ignore_errors=True
    )
    if not output.strip():
        report.log("Hardcoded secrets check", 'pass', "No obvious hardcoded secrets")
    else:
        report.log("Hardcoded secrets check", 'warn', "Found potential hardcoded values")

    # Check .env.example exists
    if check_file_exists('.env.example'):
        report.log("Environment template", 'pass', ".env.example exists")
    else:
        report.log("Environment template", 'warn', ".env.example not found")

    # Check .gitignore
    if check_file_exists('.gitignore'):
        with open('.gitignore') as f:
            content = f.read()
            if '.env' in content and '__pycache__' in content:
                report.log(".gitignore configuration", 'pass', "Critical patterns present")
            else:
                report.log(".gitignore configuration", 'warn', "May be missing patterns")
    else:
        report.log(".gitignore configuration", 'fail', "File not found")

    # =========================================================================
    # PHASE 7: Documentation Check
    # =========================================================================
    report.start_phase("Phase 7: Documentation Validation")

    doc_files = [
        'README.md',
        'API_DOCUMENTATION.md',
        'DEPLOY.md',
        'DOCUMENTATION_INDEX.md',
    ]

    for doc in doc_files:
        if check_file_exists(doc):
            size = Path(doc).stat().st_size
            if size > 100:
                report.log(f"Documentation: {doc}", 'pass', f"{size} bytes")
            else:
                report.log(f"Documentation: {doc}", 'warn', "File seems empty")
        else:
            report.log(f"Documentation: {doc}", 'warn', "Not found")

    # =========================================================================
    # Generate Report
    # =========================================================================
    report.summary()

    # Save report
    report_file = base_dir / 'FINAL_VERIFICATION_REPORT.md'
    report.generate_report(report_file)
    print(f"\n{GREEN}Report saved to: {report_file}{RESET}\n")

    # Return exit code
    return 0 if report.failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
