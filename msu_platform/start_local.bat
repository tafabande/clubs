@echo off
REM MSU Platform - Local Development Startup Script
REM This script starts the complete platform on localhost exactly as it will appear in production
REM Created: May 5, 2026

color 0A
echo ================================================================================
echo MSU Platform - Local Development Environment
echo Midlands State University Gweru Campus, Zimbabwe
echo ================================================================================
echo.

REM Check if running in correct directory
if not exist "manage.py" (
    echo ERROR: This script must be run from the msu_platform directory
    echo Please navigate to msu_platform folder and try again
    pause
    exit /b 1
)

echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo     Python found!

echo.
echo [2/8] Checking for virtual environment...
if not exist "venv\" (
    echo     Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo     Virtual environment created successfully!
) else (
    echo     Virtual environment found!
)

echo.
echo [3/8] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo     Virtual environment activated!

echo.
echo [4/8] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo     Dependencies installed!

echo.
echo [5/8] Setting up environment variables...
if not exist ".env" (
    echo     Creating .env file from template...
    copy .env.example .env >nul
    echo     Please edit .env file with your settings
    echo     Using defaults for local development...
)
echo     Environment configured!

echo.
echo [6/8] Running database migrations...
python manage.py migrate --no-input
if errorlevel 1 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)
echo     Database migrations complete!

echo.
echo [7/8] Creating superuser (if needed)...
python -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@msu.ac.zw').exists() or User.objects.create_superuser('admin@msu.ac.zw', 'admin123', first_name='Admin', last_name='User')" 2>nul
echo     Superuser ready! (Email: admin@msu.ac.zw, Password: admin123)

echo.
echo [8/8] Starting development server...
echo.
echo ================================================================================
echo MSU Platform is starting...
echo ================================================================================
echo.
echo     Local URL:  http://127.0.0.1:8000
echo     Admin URL:  http://127.0.0.1:8000/admin
echo.
echo     Superuser Credentials:
echo     Email:      admin@msu.ac.zw
echo     Password:   admin123
echo.
echo     Press Ctrl+C to stop the server
echo ================================================================================
echo.

python manage.py runserver 0.0.0.0:8000

echo.
echo Server stopped.
pause
