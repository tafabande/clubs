@echo off
REM MSU Platform - Full Stack Startup (Production Simulation)
REM This script starts the COMPLETE platform including all services (Django, Redis, Celery)
REM Simulates the exact production environment on localhost
REM Created: May 5, 2026

color 0A
echo ================================================================================
echo MSU Platform - Full Stack Production Simulation
echo Midlands State University Gweru Campus, Zimbabwe
echo ================================================================================
echo.
echo This script will start ALL services:
echo   - Django Web Server (port 8000)
echo   - Redis Cache Server (port 6379)
echo   - Celery Worker (background tasks)
echo   - Celery Beat (scheduled tasks)
echo.
echo This simulates the EXACT production environment!
echo.
pause

REM Check if Docker is available
echo [1/3] Checking for Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Docker not found!
    echo.
    echo You have two options:
    echo.
    echo   Option 1: Install Docker Desktop
    echo     Download from: https://www.docker.com/products/docker-desktop
    echo     Then run: start_docker.bat
    echo.
    echo   Option 2: Manual setup (without Docker)
    echo     - Install Redis manually
    echo     - Run start_local.bat in one terminal
    echo     - Run start_celery.bat in another terminal
    echo.
    pause
    exit /b 1
)
echo     Docker found!

echo.
echo [2/3] Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose not found
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)
echo     Docker Compose found!

echo.
echo [3/3] Starting all services with Docker Compose...
echo.

docker-compose up -d

if errorlevel 1 (
    echo ERROR: Failed to start services
    echo Please check Docker Desktop is running
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo Waiting for services to start...
echo ================================================================================
timeout /t 10 /nobreak >nul

echo.
echo [4/6] Running database migrations...
docker-compose exec -T web python manage.py migrate --no-input

echo.
echo [5/6] Creating superuser...
docker-compose exec -T web python -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@msu.ac.zw').exists() or User.objects.create_superuser('admin@msu.ac.zw', 'admin123', first_name='Admin', last_name='User')" 2>nul

echo.
echo [6/6] Populating sample data...
docker-compose exec -T web python manage.py populate_sample_data

echo.
echo ================================================================================
echo MSU Platform - Full Stack is RUNNING!
echo ================================================================================
echo.
echo     Production Simulation URL:  http://localhost
echo     Django Admin URL:           http://localhost/admin
echo     Direct Django URL:          http://localhost:8000
echo.
echo     Superuser Credentials:
echo     Email:      admin@msu.ac.zw
echo     Password:   admin123
echo.
echo     Services Running:
echo     - PostgreSQL Database (port 5432)
echo     - Redis Cache (port 6379)
echo     - Django Web Server (port 8000)
echo     - Nginx Reverse Proxy (port 80)
echo     - Celery Worker (background tasks)
echo     - Celery Beat (scheduled tasks)
echo.
echo     View Logs:
echo     docker-compose logs -f web
echo.
echo     Stop All Services:
echo     docker-compose down
echo.
echo ================================================================================
echo.
echo Press any key to view logs (Ctrl+C to exit logs)...
pause >nul

docker-compose logs -f
