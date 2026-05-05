@echo off
REM MSU Platform - Start with Sample Data
REM This script starts the platform with MSU Gweru sample data pre-populated
REM Created: May 5, 2026

color 0A
echo ================================================================================
echo MSU Platform - Start with Sample Data
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

echo [1/10] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo      Python found!

echo.
echo [2/10] Checking for virtual environment...
if not exist "venv\" (
    echo      Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo      Virtual environment created!
) else (
    echo      Virtual environment found!
)

echo.
echo [3/10] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo      Activated!

echo.
echo [4/10] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo      Dependencies installed!

echo.
echo [5/10] Setting up environment...
if not exist ".env" (
    copy .env.example .env >nul
    echo      .env file created from template
)
echo      Environment ready!

echo.
echo [6/10] Running database migrations...
python manage.py migrate --no-input
if errorlevel 1 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)
echo      Migrations complete!

echo.
echo [7/10] Creating superuser...
python -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@msu.ac.zw').exists() or User.objects.create_superuser('admin@msu.ac.zw', 'admin123', first_name='Admin', last_name='User')" 2>nul
echo      Superuser ready!

echo.
echo [8/10] Populating search index...
python manage.py populate_search_index --clear
if errorlevel 1 (
    echo WARNING: Search index population had issues
)
echo      Search index ready!

echo.
echo [9/10] Populating with MSU Gweru sample data...
echo      This will create 50 students, 21 clubs, 7 churches, 9 sports teams...
python manage.py populate_sample_data
if errorlevel 1 (
    echo WARNING: Sample data population had issues
)
echo      Sample data loaded!

echo.
echo [10/10] Starting development server...
echo.
echo ================================================================================
echo MSU Platform is ready with sample data!
echo ================================================================================
echo.
echo     Local URL:  http://127.0.0.1:8000
echo     Admin URL:  http://127.0.0.1:8000/admin
echo.
echo     Superuser Credentials:
echo     Email:      admin@msu.ac.zw
echo     Password:   admin123
echo.
echo     Sample Data Loaded:
echo     - 50 MSU Gweru students
echo     - 21 clubs (Technology, Academic, Cultural, etc.)
echo     - 7 churches/religious groups
echo     - 9 sports teams
echo     - 10 campus activities
echo     - Posts, likes, comments, shares
echo.
echo     Press Ctrl+C to stop the server
echo ================================================================================
echo.

python manage.py runserver 0.0.0.0:8000

echo.
echo Server stopped.
pause
