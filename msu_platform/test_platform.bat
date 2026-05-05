@echo off
REM MSU Platform - Run Tests
REM Run the complete test suite to verify everything works
REM Created: May 5, 2026

color 0B
title MSU Platform - Testing

echo ================================================================================
echo MSU Platform - Test Suite
echo Midlands State University Gweru Campus, Zimbabwe
echo ================================================================================
echo.

REM Check if running in correct directory
if not exist "manage.py" (
    echo ERROR: This script must be run from the msu_platform directory
    pause
    exit /b 1
)

echo [1/5] Activating virtual environment...
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run start_local.bat first
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo     Activated!

echo.
echo [2/5] Installing test dependencies...
pip install -q pytest pytest-django pytest-cov pytest-mock factory-boy faker
echo     Installed!

echo.
echo [3/5] Setting test environment...
set DJANGO_SETTINGS_MODULE=config.settings.testing
echo     Environment set!

echo.
echo [4/5] Running database migrations for tests...
python manage.py migrate --no-input
echo     Migrations complete!

echo.
echo [5/5] Running test suite...
echo.
echo ================================================================================

pytest -v --tb=short --maxfail=10

echo.
echo ================================================================================
echo.
echo Test run complete!
echo.
echo For detailed coverage report, run:
echo pytest --cov=apps --cov-report=html
echo.
pause
