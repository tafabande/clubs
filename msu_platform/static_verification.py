#!/usr/bin/env python3
"""
MSU Platform Static Verification
Comprehensive static analysis without requiring package installation
"""
import os
import re
import ast
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class StaticVerificationReport:
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
            details_lines = details.split('\n')
            for line in details_lines:
                if line.strip():
                    print(f"  → {line}")

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
            print(f"{GREEN}✓ PLATFORM STRUCTURE IS VALID{RESET}")
            print(f"{GREEN}{'='*80}{RESET}\n")
            return True
        else:
            print(f"{YELLOW}{'='*80}{RESET}")
            print(f"{YELLOW}⚠ PLATFORM HAS SOME ISSUES{RESET}")
            print(f"{YELLOW}{'='*80}{RESET}\n")
            return False

    def generate_report(self, output_file):
        """Generate markdown report"""
        with open(output_file, 'w') as f:
            f.write("# MSU Platform Final Verification Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**Type:** Static Code Analysis (No Runtime)\n\n")
            f.write("---\n\n")

            f.write("## Executive Summary\n\n")
            f.write(f"- **Total Checks:** {self.passed + self.failed + self.warnings}\n")
            f.write(f"- **Passed:** ✓ {self.passed}\n")
            f.write(f"- **Failed:** ✗ {self.failed}\n")
            f.write(f"- **Warnings:** ⚠ {self.warnings}\n\n")

            if self.failed == 0:
                f.write("### Verdict: ✓ CODE STRUCTURE VALID\n\n")
                f.write("All structural checks passed. Code is properly organized.\n\n")
                f.write("**Note:** This is a static analysis. Runtime testing requires:\n")
                f.write("- Installing dependencies: `pip install -r requirements.txt`\n")
                f.write("- Running Django checks: `python manage.py check`\n")
                f.write("- Running tests: `pytest`\n\n")
            else:
                f.write("### Verdict: ⚠ NEEDS ATTENTION\n\n")
                f.write("Some checks failed. Please review the issues below.\n\n")

            f.write("---\n\n")

            # Group by phase
            phases = defaultdict(list)
            for result in self.results:
                phases[result['phase']].append(result)

            for phase, checks in phases.items():
                f.write(f"## {phase}\n\n")
                for check in checks:
                    status_symbol = {'pass': '✓', 'fail': '✗', 'warn': '⚠'}[check['status']]
                    f.write(f"- {status_symbol} **{check['check']}**\n")
                    if check['details']:
                        for line in check['details'].split('\n'):
                            if line.strip():
                                f.write(f"  - {line}\n")
                f.write("\n")

            f.write("---\n\n")
            f.write("## Next Steps\n\n")
            f.write("### For Development\n")
            f.write("```bash\n")
            f.write("cd msu_platform\n")
            f.write("python -m venv venv\n")
            f.write("source venv/bin/activate\n")
            f.write("pip install -r requirements.txt\n")
            f.write("python manage.py migrate\n")
            f.write("python manage.py runserver\n")
            f.write("```\n\n")
            f.write("### For Testing\n")
            f.write("```bash\n")
            f.write("export DJANGO_SETTINGS_MODULE=config.settings.testing\n")
            f.write("pytest -v\n")
            f.write("```\n\n")
            f.write("### For Production Deployment\n")
            f.write("```bash\n")
            f.write("docker-compose up -d\n")
            f.write("docker-compose exec web python manage.py migrate\n")
            f.write("docker-compose exec web python manage.py collectstatic --noinput\n")
            f.write("```\n\n")

def parse_python_file(filepath):
    """Parse a Python file and return AST"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return ast.parse(content, filename=str(filepath))
    except SyntaxError as e:
        return f"SyntaxError: {e}"
    except Exception as e:
        return f"Error: {e}"

def check_file_exists(filepath):
    """Check if file exists"""
    return Path(filepath).exists()

def count_files(pattern, base_path="."):
    """Count files matching pattern"""
    return len(list(Path(base_path).rglob(pattern)))

def find_files(pattern, base_path="."):
    """Find files matching pattern"""
    return list(Path(base_path).rglob(pattern))

def check_imports_in_file(filepath):
    """Extract imports from a Python file"""
    try:
        tree = parse_python_file(filepath)
        if isinstance(tree, str):
            return None

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    except:
        return None

def check_class_definitions(filepath):
    """Extract class definitions from file"""
    try:
        tree = parse_python_file(filepath)
        if isinstance(tree, str):
            return []

        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return classes
    except:
        return []

def main():
    report = StaticVerificationReport()
    base_dir = Path(__file__).parent
    os.chdir(base_dir)

    # =========================================================================
    # PHASE 1: Project Structure Validation
    # =========================================================================
    report.start_phase("Phase 1: Project Structure Validation")

    # Check directory structure
    required_dirs = [
        'apps',
        'apps/users',
        'apps/organizations',
        'apps/media',
        'apps/core',
        'config',
        'config/settings',
    ]

    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            report.log(f"Directory exists: {dir_path}", 'pass')
        else:
            report.log(f"Directory missing: {dir_path}", 'fail')

    # Count Python files
    py_files = count_files("*.py", "apps")
    if py_files > 50:
        report.log(f"Python files in apps/", 'pass', f"{py_files} files found")
    else:
        report.log(f"Python files in apps/", 'warn', f"Only {py_files} files found")

    # =========================================================================
    # PHASE 2: Critical Files Check
    # =========================================================================
    report.start_phase("Phase 2: Critical Files Check")

    critical_files = {
        'Core Configuration': [
            'manage.py',
            'config/__init__.py',
            'config/settings/base.py',
            'config/settings/development.py',
            'config/settings/production.py',
            'config/settings/testing.py',
            'config/urls.py',
            'config/wsgi.py',
            'config/asgi.py',
        ],
        'User App': [
            'apps/users/__init__.py',
            'apps/users/models.py',
            'apps/users/views.py',
            'apps/users/serializers.py',
            'apps/users/urls.py',
        ],
        'Organizations App': [
            'apps/organizations/__init__.py',
            'apps/organizations/models/__init__.py',
            'apps/organizations/models/club.py',
            'apps/organizations/models/feed.py',
            'apps/organizations/models/follow.py',
            'apps/organizations/views/feed.py',
            'apps/organizations/serializers.py',
            'apps/organizations/feed_algorithm.py',
        ],
        'Media App': [
            'apps/media/__init__.py',
            'apps/media/models.py',
            'apps/media/views.py',
            'apps/media/serializers.py',
            'apps/media/tasks.py',
        ],
        'Core App': [
            'apps/core/__init__.py',
            'apps/core/exceptions.py',
            'apps/core/exception_handlers.py',
            'apps/core/middleware/error_logging.py',
            'apps/core/views/health.py',
        ],
    }

    for category, files in critical_files.items():
        missing = []
        for filepath in files:
            if not check_file_exists(filepath):
                missing.append(filepath)

        if not missing:
            report.log(f"{category} files", 'pass', f"All {len(files)} files present")
        else:
            report.log(f"{category} files", 'fail', f"Missing: {', '.join(missing)}")

    # =========================================================================
    # PHASE 3: Python Syntax Validation
    # =========================================================================
    report.start_phase("Phase 3: Python Syntax Validation")

    # Check key files for syntax errors
    key_files = [
        'apps/users/models.py',
        'apps/organizations/models/club.py',
        'apps/organizations/models/feed.py',
        'apps/organizations/feed_algorithm.py',
        'apps/media/models.py',
        'apps/core/exceptions.py',
        'config/settings/base.py',
    ]

    syntax_errors = []
    for filepath in key_files:
        if check_file_exists(filepath):
            result = parse_python_file(filepath)
            if isinstance(result, str):
                syntax_errors.append(f"{filepath}: {result}")
                report.log(f"Syntax check: {filepath}", 'fail', result)
            else:
                report.log(f"Syntax check: {filepath}", 'pass')
        else:
            report.log(f"Syntax check: {filepath}", 'warn', "File not found")

    # =========================================================================
    # PHASE 4: Model Definitions Check
    # =========================================================================
    report.start_phase("Phase 4: Model Definitions Check")

    model_files = {
        'User model': 'apps/users/models.py',
        'Club model': 'apps/organizations/models/club.py',
        'Post model': 'apps/organizations/models/feed.py',
        'Feed model': 'apps/organizations/models/feed.py',
        'Follow model': 'apps/organizations/models/follow.py',
    }

    for model_name, filepath in model_files.items():
        if check_file_exists(filepath):
            classes = check_class_definitions(filepath)
            expected_class = model_name.split()[0]
            if expected_class in classes or any(expected_class.lower() in c.lower() for c in classes):
                report.log(f"{model_name} defined", 'pass', f"Found in {filepath}")
            else:
                report.log(f"{model_name} defined", 'warn', f"Not found in {filepath}, found: {', '.join(classes)}")
        else:
            report.log(f"{model_name} defined", 'fail', f"File not found: {filepath}")

    # =========================================================================
    # PHASE 5: Test Files Check
    # =========================================================================
    report.start_phase("Phase 5: Test Files Check")

    test_files = find_files("test_*.py", "apps")
    if test_files:
        report.log("Test files found", 'pass', f"{len(test_files)} test files")

        # Check a few test files for structure
        sample_tests = test_files[:3]
        for test_file in sample_tests:
            classes = check_class_definitions(test_file)
            if classes:
                report.log(f"Test file structure: {test_file.name}", 'pass', f"{len(classes)} test classes")
            else:
                report.log(f"Test file structure: {test_file.name}", 'warn', "No test classes found")
    else:
        report.log("Test files found", 'warn', "No test files found")

    # Check conftest.py
    if check_file_exists('conftest.py'):
        report.log("Pytest configuration", 'pass', "conftest.py exists")
    else:
        report.log("Pytest configuration", 'warn', "conftest.py not found")

    # =========================================================================
    # PHASE 6: Configuration Files Check
    # =========================================================================
    report.start_phase("Phase 6: Configuration Files Check")

    # Check settings files
    settings_files = [
        'config/settings/base.py',
        'config/settings/development.py',
        'config/settings/production.py',
        'config/settings/testing.py',
    ]

    for settings_file in settings_files:
        if check_file_exists(settings_file):
            # Check for critical settings
            with open(settings_file, 'r') as f:
                content = f.read()
                has_installed_apps = 'INSTALLED_APPS' in content
                has_middleware = 'MIDDLEWARE' in content
                has_databases = 'DATABASES' in content

                if settings_file.endswith('base.py'):
                    if all([has_installed_apps, has_middleware, has_databases]):
                        report.log(f"Settings file: {settings_file}", 'pass', "All critical settings present")
                    else:
                        missing = []
                        if not has_installed_apps: missing.append('INSTALLED_APPS')
                        if not has_middleware: missing.append('MIDDLEWARE')
                        if not has_databases: missing.append('DATABASES')
                        report.log(f"Settings file: {settings_file}", 'warn', f"Missing: {', '.join(missing)}")
                else:
                    report.log(f"Settings file: {settings_file}", 'pass', "File exists")
        else:
            report.log(f"Settings file: {settings_file}", 'fail', "File not found")

    # =========================================================================
    # PHASE 7: Docker Configuration Check
    # =========================================================================
    report.start_phase("Phase 7: Docker Configuration Check")

    docker_files = {
        'Dockerfile': ['FROM', 'WORKDIR', 'COPY', 'RUN', 'CMD'],
        'docker-compose.yml': ['version', 'services', 'web', 'db'],
    }

    for filename, required_terms in docker_files.items():
        if check_file_exists(filename):
            with open(filename, 'r') as f:
                content = f.read().lower()
                missing_terms = [term for term in required_terms if term.lower() not in content]

                if not missing_terms:
                    report.log(f"Docker file: {filename}", 'pass', "All required directives present")
                else:
                    report.log(f"Docker file: {filename}", 'warn', f"Missing: {', '.join(missing_terms)}")
        else:
            report.log(f"Docker file: {filename}", 'warn', "File not found")

    # =========================================================================
    # PHASE 8: Security Checks
    # =========================================================================
    report.start_phase("Phase 8: Security Checks")

    # Check .gitignore
    if check_file_exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            critical_patterns = ['.env', '__pycache__', '*.pyc', 'db.sqlite3', 'venv']
            missing_patterns = [p for p in critical_patterns if p not in gitignore_content]

            if not missing_patterns:
                report.log(".gitignore configuration", 'pass', "All critical patterns present")
            else:
                report.log(".gitignore configuration", 'warn', f"Missing patterns: {', '.join(missing_patterns)}")
    else:
        report.log(".gitignore configuration", 'fail', "File not found")

    # Check for .env.example
    if check_file_exists('.env.example'):
        report.log("Environment template", 'pass', ".env.example exists")
    else:
        report.log("Environment template", 'warn', ".env.example not found")

    # Check for hardcoded secrets (basic check)
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret_key\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
    ]

    py_files_to_check = list(Path('apps').rglob('*.py'))[:20]
    hardcoded_secrets = []

    for py_file in py_files_to_check:
        try:
            with open(py_file, 'r') as f:
                content = f.read()
                for pattern in secret_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        # Exclude false positives
                        if 'SECRET_KEY' not in content and 'environ' not in content:
                            hardcoded_secrets.append(str(py_file))
                            break
        except:
            pass

    if not hardcoded_secrets:
        report.log("Hardcoded secrets check", 'pass', "No obvious hardcoded secrets")
    else:
        report.log("Hardcoded secrets check", 'warn', f"Check these files: {', '.join(hardcoded_secrets[:3])}")

    # =========================================================================
    # PHASE 9: Documentation Check
    # =========================================================================
    report.start_phase("Phase 9: Documentation Check")

    doc_files = {
        'README.md': 500,
        'API_DOCUMENTATION.md': 500,
        'DEPLOY.md': 500,
        'DOCUMENTATION_INDEX.md': 200,
    }

    for doc_file, min_size in doc_files.items():
        if check_file_exists(doc_file):
            size = Path(doc_file).stat().st_size
            if size >= min_size:
                report.log(f"Documentation: {doc_file}", 'pass', f"{size} bytes")
            else:
                report.log(f"Documentation: {doc_file}", 'warn', f"Only {size} bytes (expected >{min_size})")
        else:
            report.log(f"Documentation: {doc_file}", 'warn', "File not found")

    # =========================================================================
    # PHASE 10: Code Quality Metrics
    # =========================================================================
    report.start_phase("Phase 10: Code Quality Metrics")

    # Count total lines of code
    total_lines = 0
    py_files = list(Path('apps').rglob('*.py'))

    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                total_lines += len(f.readlines())
        except:
            pass

    report.log("Lines of code", 'pass', f"{total_lines:,} lines in {len(py_files)} files")

    # Check for __init__.py files in apps
    app_dirs = [d for d in Path('apps').iterdir() if d.is_dir() and not d.name.startswith('_')]
    missing_init = []

    for app_dir in app_dirs:
        init_file = app_dir / '__init__.py'
        if not init_file.exists():
            missing_init.append(app_dir.name)

    if not missing_init:
        report.log("App initialization files", 'pass', "All apps have __init__.py")
    else:
        report.log("App initialization files", 'warn', f"Missing in: {', '.join(missing_init)}")

    # Check migrations
    migration_dirs = list(Path('apps').rglob('migrations'))
    if migration_dirs:
        report.log("Migration directories", 'pass', f"{len(migration_dirs)} apps have migrations")
    else:
        report.log("Migration directories", 'warn', "No migration directories found")

    # =========================================================================
    # Generate Final Report
    # =========================================================================
    success = report.summary()

    # Save report
    report_file = base_dir / 'FINAL_VERIFICATION_REPORT.md'
    report.generate_report(report_file)
    print(f"{GREEN}Report saved to: {report_file}{RESET}\n")

    return 0 if success else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
