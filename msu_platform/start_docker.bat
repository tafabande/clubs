@echo off
REM MSU Platform - Docker Quick Start
REM Simplest way to run the complete platform (recommended)
REM Created: May 5, 2026

color 0A
title MSU Platform - Docker Startup

echo ================================================================================
echo MSU Platform - Docker Quick Start
echo Midlands State University Gweru Campus, Zimbabwe
echo ================================================================================
echo.

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed!
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed!
    pause
    exit /b 1
)

echo Docker and Docker Compose detected!
echo.
echo Starting MSU Platform...
echo.

REM Start services
docker-compose up -d

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start services
    echo.
    echo Make sure Docker Desktop is running!
    echo.
    pause
    exit /b 1
)

echo.
echo Waiting for services to initialize (15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo Running initial setup...
docker-compose exec -T web python manage.py migrate --no-input
docker-compose exec -T web python manage.py createsuperuser --noinput --email admin@msu.ac.zw 2>nul || echo Superuser already exists

echo.
echo ================================================================================
echo SUCCESS! MSU Platform is now running!
echo ================================================================================
echo.
echo     Main URL:    http://localhost
echo     Admin URL:   http://localhost/admin
echo     Direct:      http://localhost:8000
echo.
echo     Login:       admin@msu.ac.zw
echo     Password:    admin123
echo.
echo     To add sample data, run:
echo     docker-compose exec web python manage.py populate_sample_data
echo.
echo     To stop:
echo     docker-compose down
echo.
echo     To view logs:
echo     docker-compose logs -f
echo.
echo ================================================================================
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost

echo.
echo Platform is running in the background.
echo Press any key to view live logs (Ctrl+C to exit)...
pause >nul

docker-compose logs -f web
