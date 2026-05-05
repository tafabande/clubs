@echo off
REM MSU Platform - Stop All Services
REM Safely stops all running services
REM Created: May 5, 2026

color 0C
title MSU Platform - Stop Services

echo ================================================================================
echo MSU Platform - Stopping All Services
echo ================================================================================
echo.

REM Check if Docker services are running
docker-compose ps >nul 2>&1
if not errorlevel 1 (
    echo Stopping Docker services...
    docker-compose down
    echo.
    echo Docker services stopped!
) else (
    echo No Docker services running.
)

echo.
echo All MSU Platform services have been stopped.
echo.
pause
