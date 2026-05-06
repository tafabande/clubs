@echo off
REM MSU Platform - One-Tap Launch
REM Automatically sets up and launches the complete MSU Platform
REM Created: May 5, 2026

setlocal enabledelayedexpansion

REM ================================================================================
REM CONFIGURATION
REM ================================================================================
set "ADMIN_EMAIL=admin@msu.ac.zw"
set "ADMIN_PASSWORD=admin123"
set "ADMIN_FIRST_NAME=Admin"
set "ADMIN_LAST_NAME=User"
set "DEFAULT_PORT=8000"

REM ================================================================================
REM HEADER
REM ================================================================================
color 0B
title MSU Platform - One-Tap Launch
:master_menu
cls
echo.
echo ================================================================================
echo        MSU PLATFORM - MASTER MENU
echo        Midlands State University Gweru Campus, Zimbabwe
echo ================================================================================
echo.
echo Please select an operation:
echo   1. Launch Platform (FAST - Recommended)
echo   2. Repair ^& Launch (Full Setup ^& Checks)
echo   3. Start Docker Services
echo   4. Stop All Services
echo   5. Exit
echo.
set /p MENU_CHOICE="Enter your choice (1-5) [1]: "
if "%MENU_CHOICE%"=="" set MENU_CHOICE=1

if "%MENU_CHOICE%"=="1" goto :fast_launch
if "%MENU_CHOICE%"=="2" goto :full_setup
if "%MENU_CHOICE%"=="3" goto :start_docker
if "%MENU_CHOICE%"=="4" goto :stop_all
if "%MENU_CHOICE%"=="5" exit /b 0

echo Invalid choice.
ping -n 2 127.0.0.1 >nul
goto :master_menu

:fast_launch
echo.
echo [INFO] Attempting Fast Launch...
if not exist "venv\Scripts\activate.bat" (
    echo [WARN] venv not found. Switching to Repair Mode...
    goto :full_setup
)
call venv\Scripts\activate.bat
python manage.py migrate --no-input >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Database check failed. Switching to Repair Mode...
    goto :full_setup
)
goto :start_services

:start_docker
echo [INFO] Starting Docker services...
docker-compose up -d --build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker services.
) else (
    echo [PASS] Docker services started.
    echo Platform: http://localhost:8000
)
pause
goto :master_menu

:stop_all
echo [INFO] Stopping all services...
taskkill /IM python.exe /F >nul 2>&1
taskkill /IM node.exe /F >nul 2>&1
echo [PASS] Local services stopped.
pause
goto :master_menu

:full_setup
echo.
echo ================================================================================
echo        REPAIR ^& FULL SETUP MODE
echo ================================================================================
echo.
REM Step 1: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python not in PATH.
    pause
    goto :master_menu
)

REM Step 2: Venv
if not exist "venv\" (
    echo [INFO] Creating venv...
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Step 3: Dependencies
echo [INFO] Installing dependencies...
python -m pip install -r requirements.txt --quiet
if exist "frontend\" (
    pushd frontend
    if not exist "node_modules\" call npm install --legacy-peer-deps --quiet
    popd
)

REM Step 4: DB
echo [INFO] Running migrations...
python manage.py migrate --no-input

REM Step 5: Admin
echo [INFO] Seeding admin...
python scripts/seed_admin.py

goto :start_services

:start_services
echo.
echo [INFO] Starting Backend...
start /B python manage.py runserver 0.0.0.0:%DEFAULT_PORT% > server.log 2>&1

if exist "frontend\" (
    echo [INFO] Starting Frontend...
    pushd frontend
    start /B npm run dev > ../frontend.log 2>&1
    popd
)

echo.
echo ================================================================================
echo                          MSU PLATFORM IS LIVE!
echo ================================================================================
echo   URL: http://localhost:5173
echo   API: http://localhost:%DEFAULT_PORT%
echo ================================================================================
echo.
echo Opening browser...
start "" "http://localhost:5173"

:show_logs
cls
echo ================================================================================
echo MSU PLATFORM - LIVE LOGS (Refreshing every 3s)
echo ================================================================================
if exist "server.log" (
    powershell -command "Get-Content server.log -Tail 15"
) else (
    echo Waiting for logs...
)
echo --------------------------------------------------------------------------------
ping -n 4 127.0.0.1 >nul
goto :show_logs
