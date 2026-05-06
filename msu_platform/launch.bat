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
echo   1. Launch Platform (Local - 127.0.0.1)
echo   2. Launch Platform (LAN - Multi-Device)
echo   3. Repair ^& Launch (Full Setup ^& Checks)
echo   4. Start Docker Services
echo   5. Stop All Services
echo   6. Exit
echo.
set /p MENU_CHOICE="Enter your choice (1-6) [1]: "
if "%MENU_CHOICE%"=="" set MENU_CHOICE=1

if "%MENU_CHOICE%"=="1" goto :local_launch
if "%MENU_CHOICE%"=="2" goto :lan_launch
if "%MENU_CHOICE%"=="3" goto :full_setup
if "%MENU_CHOICE%"=="4" goto :start_docker
if "%MENU_CHOICE%"=="5" goto :stop_all
if "%MENU_CHOICE%"=="6" exit /b 0

echo Invalid choice.
ping -n 2 127.0.0.1 >nul
goto :master_menu

:local_launch
set "HOST_IP=127.0.0.1"
goto :fast_launch

:lan_launch
echo [INFO] Detecting Local IP...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "RAW_IP=%%a"
    set "HOST_IP=!RAW_IP: =!"
    REM We usually want the first one that isn't 127.0.0.1 or similar
    if not "!HOST_IP!"=="" (
        if not "!HOST_IP!"=="127.0.0.1" goto :ip_found
    )
)
:ip_found
if "%HOST_IP%"=="" (
    echo [WARN] Could not detect Local IP. Falling back to 127.0.0.1
    set "HOST_IP=127.0.0.1"
) else (
    echo [PASS] Detected LAN IP: %HOST_IP%
)
goto :fast_launch

:fast_launch
echo.
echo [INFO] MSU Platform Fast Launch (%HOST_IP%)...
if not exist "venv\Scripts\activate.bat" (
    echo [WARN] venv not found. Initializing...
    goto :full_setup
)
call venv\Scripts\activate.bat
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
if "%HOST_IP%"=="" set "HOST_IP=127.0.0.1"
echo.
echo ================================================================================
echo        REPAIR ^& FULL SETUP MODE (%HOST_IP%)
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
if "%HOST_IP%"=="" set "HOST_IP=127.0.0.1"
echo.
echo [INFO] Configuring Environment for %HOST_IP%...

REM Set environment variables for the current session
set "VITE_API_BASE_URL=http://%HOST_IP%:%DEFAULT_PORT%/api"
set "ALLOWED_HOSTS=localhost,127.0.0.1,%HOST_IP%"
set "CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://%HOST_IP%:5173"
set "CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://%HOST_IP%:5173"
set "FRONTEND_URL=http://%HOST_IP%:5173"

REM Create a temporary settings override for Django to handle dynamic ALLOWED_HOSTS if needed
REM But since we use environment variables and 'environ', setting the OS env var is enough.

echo [INFO] Starting Backend...
start /B python manage.py runserver 0.0.0.0:%DEFAULT_PORT% > server.log 2>&1
timeout /t 2 /nobreak > nul

REM Check if server started successfully
tasklist /FI "IMAGENAME eq python.exe" | findstr python.exe > nul
if %errorlevel% neq 0 (
    echo [FAIL] Backend failed to start. Running health checks...
    goto :full_setup
)

if exist "frontend\" (
    echo [INFO] Starting Frontend...
    pushd frontend
    REM Inject VITE_API_BASE_URL for the frontend process
    set "VITE_API_BASE_URL=http://%HOST_IP%:%DEFAULT_PORT%/api"
    REM For Vite to listen on all interfaces, we use --host 0.0.0.0
    start /B npm run dev -- --host 0.0.0.0 > ../frontend.log 2>&1
    popd
)

echo.
echo ================================================================================
echo                          MSU PLATFORM IS LIVE!
echo ================================================================================
echo   URL: http://%HOST_IP%:5173
echo   API: http://%HOST_IP%:%DEFAULT_PORT%
echo ================================================================================
echo.
echo Opening browser...
start "" "http://%HOST_IP%:5173"

:show_logs
cls
echo ================================================================================
echo MSU PLATFORM - LIVE LOGS (Refreshing every 3s)
echo ================================================================================
if exist "server.log" (
    echo --- BACKEND (server.log) ---
    powershell -command "Get-Content server.log -Tail 10"
)
if exist "frontend.log" (
    echo.
    echo --- FRONTEND (frontend.log) ---
    powershell -command "Get-Content frontend.log -Tail 5"
)
echo --------------------------------------------------------------------------------
ping -n 4 127.0.0.1 >nul
goto :show_logs
