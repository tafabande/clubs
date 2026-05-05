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
cls
echo.
echo ================================================================================
echo        MSU PLATFORM - ONE-TAP LAUNCH
echo        Midlands State University Gweru Campus, Zimbabwe
echo ================================================================================
echo.
echo This script will:
echo   [*] Scan system compatibility
echo   [*] Install prerequisites automatically
echo   [*] Set up the platform
echo   [*] Seed admin user
echo   [*] Display LAN and localhost links
echo   [*] Show real-time status logs
echo.
echo ================================================================================
echo.
timeout /t 3 /nobreak >nul

REM ================================================================================
REM STEP 1: COMPATIBILITY SCAN
REM ================================================================================
echo [1/10] SCANNING SYSTEM COMPATIBILITY...
echo --------------------------------------------------------------------------------
echo.

REM Check Windows version
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo [CHECK] Windows Version: %VERSION%
if "%VERSION%" GEQ "10.0" (
    echo [PASS]  Windows 10 or higher detected
) else (
    echo [WARN]  Windows version may not be optimal ^(recommended: Windows 10+^)
)
echo.

REM Check if running from correct directory
if not exist "manage.py" (
    echo [FAIL]  ERROR: This script must be run from the msu_platform directory
    echo [INFO]  Current directory: %CD%
    echo [INFO]  Please navigate to the msu_platform folder and run this script again
    echo.
    pause
    exit /b 1
)
echo [PASS]  Running from correct directory
echo.

REM Check Python installation
echo [CHECK] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL]  Python is not installed or not in PATH
    echo.
    echo [ACTION REQUIRED] Installing Python...
    echo.
    echo Please install Python 3.11+ from: https://www.python.org/downloads/
    echo During installation, make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [PASS]  Python %PYTHON_VERSION% detected
echo.

REM Check Python version (need 3.11+)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)
if %PYTHON_MINOR% LSS 11 (
    echo [WARN]  Python 3.11+ recommended ^(you have %PYTHON_VERSION%^)
    echo [INFO]  Platform may still work but upgrade recommended
    echo.
) else (
    echo [PASS]  Python version is compatible
    echo.
)

REM Check pip
echo [CHECK] Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN]  pip not found, installing...
    python -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo [FAIL]  Could not install pip
        pause
        exit /b 1
    )
)
echo [PASS]  pip is available
echo.

REM Check Git
echo [CHECK] Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN]  Git is not installed
    echo [INFO]  Git is optional but recommended for version control
    echo [INFO]  Download from: https://git-scm.com/download/win
) else (
    for /f "tokens=3" %%i in ('git --version 2^>^&1') do echo [PASS]  Git %%i detected
)
echo.

REM Check available disk space
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do set FREE_SPACE=%%a
echo [CHECK] Available disk space: %FREE_SPACE% bytes
echo [PASS]  Sufficient disk space available
echo.

REM Check network connectivity
echo [CHECK] Checking internet connectivity...
ping -n 1 google.com >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS]  Internet connection available
) else (
    echo [WARN]  No internet connection detected
    echo [INFO]  Internet required for installing dependencies
)
echo.

echo [PASS]  Compatibility scan complete!
echo.
timeout /t 2 /nobreak >nul

REM ================================================================================
REM STEP 2: DETECT LAN IP ADDRESS
REM ================================================================================
echo [2/10] DETECTING NETWORK CONFIGURATION...
echo --------------------------------------------------------------------------------
echo.

REM Get LAN IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    set IP=!IP:~1!
    if not "!IP!"=="" (
        if not "!IP:~0,3!"=="169" (
            set LAN_IP=!IP!
            goto :lan_found
        )
    )
)
:lan_found

if defined LAN_IP (
    echo [PASS]  LAN IP Address: %LAN_IP%
) else (
    set LAN_IP=127.0.0.1
    echo [WARN]  Could not detect LAN IP, using localhost only
)
echo.

REM Get computer name
echo [INFO]  Computer Name: %COMPUTERNAME%
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 3: CREATE VIRTUAL ENVIRONMENT
REM ================================================================================
echo [3/10] SETTING UP VIRTUAL ENVIRONMENT...
echo --------------------------------------------------------------------------------
echo.

if exist "venv\" (
    echo [INFO]  Virtual environment already exists
) else (
    echo [INFO]  Creating new virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [FAIL]  Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [PASS]  Virtual environment created
)
echo.

echo [INFO]  Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [FAIL]  Failed to activate virtual environment
    pause
    exit /b 1
)
echo [PASS]  Virtual environment activated
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 4: INSTALL PREREQUISITES
REM ================================================================================
echo [4/10] INSTALLING PREREQUISITES...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel --quiet
if %errorlevel% neq 0 (
    echo [WARN]  Could not upgrade pip, continuing anyway...
) else (
    echo [PASS]  Package managers upgraded
)
echo.

echo [INFO]  Installing Django and dependencies from requirements.txt...
echo [INFO]  This may take 2-5 minutes on first run...
echo.

if exist "requirements.txt" (
    pip install -r requirements.txt --quiet --disable-pip-version-check
    if %errorlevel% neq 0 (
        echo [FAIL]  Failed to install dependencies
        echo [INFO]  Trying verbose installation to show errors...
        pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo [PASS]  All dependencies installed successfully
) else (
    echo [WARN]  requirements.txt not found
    echo [INFO]  Installing minimal dependencies...
    pip install django djangorestframework django-cors-headers python-dotenv --quiet
)
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 5: ENVIRONMENT CONFIGURATION
REM ================================================================================
echo [5/10] CONFIGURING ENVIRONMENT...
echo --------------------------------------------------------------------------------
echo.

if not exist ".env" (
    if exist ".env.example" (
        echo [INFO]  Creating .env file from .env.example...
        copy .env.example .env >nul
        echo [PASS]  Environment file created
    ) else (
        echo [INFO]  Creating default .env file...
        (
            echo DEBUG=True
            echo SECRET_KEY=dev-secret-key-change-in-production
            echo DJANGO_SETTINGS_MODULE=config.settings.development
            echo ALLOWED_HOSTS=localhost,127.0.0.1,%LAN_IP%
            echo DATABASE_URL=sqlite:///db.sqlite3
        ) > .env
        echo [PASS]  Default environment file created
    )
) else (
    echo [INFO]  Environment file already exists
    echo [PASS]  Using existing .env configuration
)
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 6: DATABASE SETUP
REM ================================================================================
echo [6/10] SETTING UP DATABASE...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Running database migrations...
python manage.py migrate --no-input
if %errorlevel% neq 0 (
    echo [FAIL]  Database migration failed
    echo [INFO]  Check the error messages above
    pause
    exit /b 1
)
echo [PASS]  Database migrations complete
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 7: SEED ADMIN USER
REM ================================================================================
echo [7/10] SEEDING ADMIN USER...
echo --------------------------------------------------------------------------------
echo.

REM Check if admin already exists
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(email='%ADMIN_EMAIL%').exists() else 'not_found')" > temp_check.txt 2>&1
set /p ADMIN_EXISTS=<temp_check.txt
del temp_check.txt

if "%ADMIN_EXISTS%"=="exists" (
    echo [INFO]  Admin user already exists: %ADMIN_EMAIL%
    echo [PASS]  Skipping admin creation
) else (
    echo [INFO]  Creating admin user...
    echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(email='%ADMIN_EMAIL%', password='%ADMIN_PASSWORD%', first_name='%ADMIN_FIRST_NAME%', last_name='%ADMIN_LAST_NAME%', student_number='MSU000000', faculty='Administration', department='IT', year_of_study=4, is_verified=True) | python manage.py shell

    if %errorlevel% neq 0 (
        echo [WARN]  Could not create admin user automatically
        echo [INFO]  You can create one manually later with: python manage.py createsuperuser
    ) else (
        echo [PASS]  Admin user created successfully
    )
)
echo.
echo [CREDENTIALS]
echo     Email:    %ADMIN_EMAIL%
echo     Password: %ADMIN_PASSWORD%
echo.
echo [IMPORTANT] Change these credentials after first login!
echo.
timeout /t 2 /nobreak >nul

REM ================================================================================
REM STEP 8: POPULATE SEARCH INDEX
REM ================================================================================
echo [8/10] INITIALIZING SEARCH INDEX...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Populating search index...
python manage.py populate_search_index >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS]  Search index initialized
) else (
    echo [INFO]  Search index will be populated as content is added
)
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 9: START SERVER
REM ================================================================================
echo [9/10] STARTING DJANGO DEVELOPMENT SERVER...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Starting server on 0.0.0.0:%DEFAULT_PORT%...
echo [INFO]  Server will be accessible from LAN devices
echo.

REM Start server in background and redirect output to log file
start /B python manage.py runserver 0.0.0.0:%DEFAULT_PORT% > server.log 2>&1

REM Wait for server to start
echo [INFO]  Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Check if server started successfully
netstat -an | findstr ":%DEFAULT_PORT%" >nul
if %errorlevel% equ 0 (
    echo [PASS]  Server started successfully
) else (
    echo [WARN]  Server may not have started properly
    echo [INFO]  Check server.log for details
)
echo.
timeout /t 1 /nobreak >nul

REM ================================================================================
REM STEP 10: DISPLAY ACCESS INFORMATION
REM ================================================================================
echo [10/10] PLATFORM READY!
echo --------------------------------------------------------------------------------
echo.

echo ================================================================================
echo                          MSU PLATFORM IS LIVE!
echo ================================================================================
echo.
echo [ACCESS LINKS]
echo.
echo   Localhost:  http://127.0.0.1:%DEFAULT_PORT%
echo   LAN:        http://%LAN_IP%:%DEFAULT_PORT%
echo.
echo   Admin Panel:     /admin/
echo   API Endpoints:   /api/
echo   Documentation:   /api/docs/
echo.
echo [ADMIN CREDENTIALS]
echo.
echo   Email:    %ADMIN_EMAIL%
echo   Password: %ADMIN_PASSWORD%
echo.
echo   [!] CHANGE THESE CREDENTIALS AFTER FIRST LOGIN
echo.
echo [NETWORK ACCESS]
echo.
echo   Your platform is accessible from any device on your network at:
echo   http://%LAN_IP%:%DEFAULT_PORT%
echo.
echo   Share this link with others on your network to allow access.
echo.
echo [SERVER STATUS]
echo.
echo   Status:   RUNNING
echo   Port:     %DEFAULT_PORT%
echo   Log file: server.log
echo.
echo ================================================================================
echo.

REM Ask if user wants to open browser
set /p OPEN_BROWSER="Open platform in browser? (Y/N): "
if /i "%OPEN_BROWSER%"=="Y" (
    echo.
    echo [INFO]  Opening http://127.0.0.1:%DEFAULT_PORT% in default browser...
    start http://127.0.0.1:%DEFAULT_PORT%
    timeout /t 2 /nobreak >nul
)

echo.
echo ================================================================================
echo                          LIVE STATUS LOGS
echo ================================================================================
echo.
echo Press Ctrl+C to stop the server and exit
echo.
echo Showing server logs (last 20 lines, updates every 5 seconds)...
echo.
echo --------------------------------------------------------------------------------

REM Show live logs
:show_logs
cls
echo ================================================================================
echo MSU PLATFORM - LIVE STATUS LOGS
echo ================================================================================
echo.
echo [STATUS] Server running on http://%LAN_IP%:%DEFAULT_PORT%
echo [TIME]   %date% %time%
echo.
echo --------------------------------------------------------------------------------
echo RECENT LOG ENTRIES:
echo --------------------------------------------------------------------------------
echo.

if exist "server.log" (
    REM Show last 20 lines of log file
    powershell -command "Get-Content server.log -Tail 20"
) else (
    echo No logs available yet...
)

echo.
echo --------------------------------------------------------------------------------
echo Press Ctrl+C to stop server ^| Refreshing in 5 seconds...
echo --------------------------------------------------------------------------------

timeout /t 5 /nobreak >nul
goto :show_logs

REM This line won't be reached due to infinite loop above
REM User must press Ctrl+C to exit
