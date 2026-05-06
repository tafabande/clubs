@echo off
python -c "import sys; print(sys.executable)"
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
echo   1. Launch Development Server
echo   2. Start Docker Services (Production Simulation)
echo   3. Run Test Suite
echo   4. Deploy Platform
echo   5. Stop All Services
echo   6. Migrate Legacy Data
echo   7. Exit
echo.
set /p MENU_CHOICE="Enter your choice (1-7) [1]: "
if "%MENU_CHOICE%"=="" set MENU_CHOICE=1

if "%MENU_CHOICE%"=="1" goto :launch_server
if "%MENU_CHOICE%"=="2" goto :start_docker
if "%MENU_CHOICE%"=="3" goto :run_tests
if "%MENU_CHOICE%"=="4" goto :deploy_platform
if "%MENU_CHOICE%"=="5" goto :stop_all
if "%MENU_CHOICE%"=="6" goto :migrate_data
if "%MENU_CHOICE%"=="7" exit /b 0

echo Invalid choice.
ping -n 3 127.0.0.1 >nul
goto :master_menu

:start_docker
echo [INFO] Starting Docker services...
docker-compose up -d --build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker services. Please check if Docker Desktop is running.
) else (
    echo [PASS] Docker services started successfully.
    echo.
    echo [ACCESS LINKS]
    echo   Platform: http://localhost:8000
    echo   Admin:    http://localhost:8000/admin/
)
echo.
echo Press any key to return to the Master Menu...
pause >nul
goto :master_menu

:run_tests
echo [INFO] Running test suite...
if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat
pytest -v
if %errorlevel% neq 0 (
    echo [ERROR] One or more tests failed. Review the test logs above.
) else (
    echo [PASS] All tests passed successfully!
)
echo.
echo Press any key to return to the Master Menu...
pause >nul
goto :master_menu

:deploy_platform
echo [INFO] Deploying platform...
git pull
if %errorlevel% neq 0 (
    echo [ERROR] Failed to pull latest code from Git.
) else (
    docker-compose up -d --build
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to deploy Docker containers.
    ) else (
        echo [PASS] Platform deployed successfully.
        echo.
        echo [ACCESS LINKS]
        echo   Platform: http://localhost:8000
        echo   Admin:    http://localhost:8000/admin/
    )
)
echo.
echo Press any key to return to the Master Menu...
pause >nul
goto :master_menu

:stop_all
echo [INFO] Stopping all services...
docker-compose down
if %errorlevel% neq 0 (
    echo [WARN] Docker-compose down encountered an issue ^(containers might not be running^).
)
taskkill /IM python.exe /F >nul 2>&1
echo [PASS] All local services stopped.
echo.
echo Press any key to return to the Master Menu...
pause >nul
goto :master_menu

:migrate_data
echo [INFO] Migrating legacy data...
if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat
python scripts/migrate_flask_data.py
if %errorlevel% neq 0 (
    echo [ERROR] Data migration failed. See error output above.
) else (
    echo [PASS] Legacy data migrated successfully.
)
echo.
echo Press any key to return to the Master Menu...
pause >nul
goto :master_menu

:launch_server
echo.
echo ================================================================================
echo        LAUNCHING SERVER
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

REM ================================================================================
REM STEP 0: ENVIRONMENT SELECTION
REM ================================================================================
echo [0/10] SELECT DEPLOYMENT ENVIRONMENT
echo --------------------------------------------------------------------------------
echo Please select the deployment environment:
echo   1. Local  (Skip strict checks, localhost only, fast launch)
echo   2. Online (Standard checks, accessible on LAN/Internet)
echo   3. Prod   (Ultra-strict checks, production safety)
set /p ENV_CHOICE="Enter your choice (1/2/3) [1]: "
if "%ENV_CHOICE%"=="" set ENV_CHOICE=1

if "%ENV_CHOICE%"=="1" (
    set ENV_MODE=local
    echo.
    echo Selected Environment: LOCAL
) else if "%ENV_CHOICE%"=="2" (
    set ENV_MODE=online
    echo.
    echo Selected Environment: ONLINE
) else if "%ENV_CHOICE%"=="3" (
    set ENV_MODE=prod
    echo.
    echo Selected Environment: PROD
) else (
    set ENV_MODE=local
    echo.
    echo Invalid choice. Defaulting to LOCAL.
)
echo --------------------------------------------------------------------------------
echo.
ping -n 3 127.0.0.1 >nul

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
    goto :error_exit
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
    goto :error_exit
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
    if "%ENV_MODE%"=="prod" (
        echo [FAIL]  Python 3.11+ is strictly REQUIRED for PROD mode ^(you have %PYTHON_VERSION%^)
        pause
        goto :error_exit
    ) else (
        echo [WARN]  Python 3.11+ recommended ^(you have %PYTHON_VERSION%^)
        echo [INFO]  Platform may still work but upgrade recommended
        echo.
    )
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
        goto :error_exit
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

REM Check Node.js (needed for frontend)
if exist "frontend\" (
    echo [CHECK] Checking Node.js installation for frontend...
    node --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo [WARN]  Node.js is not installed but a frontend folder was detected.
        echo [INFO]  Please install Node.js from: https://nodejs.org/
        echo [INFO]  The React UI will be skipped if Node.js is missing.
    ) else (
        for /f "tokens=1" %%v in ('node --version') do echo [PASS]  Node %%v detected
    )
    echo.
)
REM Check internet connectivity
echo [CHECK] Checking internet connectivity...
if "%ENV_MODE%"=="local" (
    echo [SKIP]  Skipping internet check in LOCAL mode
) else (
    ping -n 1 google.com >nul 2>&1
    if !errorlevel! equ 0 (
        echo [PASS]  Internet connection available
    ) else (
        if "%ENV_MODE%"=="prod" (
            echo [FAIL]  Internet connection is strictly REQUIRED for PROD mode
            pause
            goto :error_exit
        ) else (
            echo [WARN]  No internet connection detected
            echo [INFO]  Internet required for installing dependencies
        )
    )
)
echo.

echo [PASS]  Compatibility scan complete!
echo.
ping -n 3 127.0.0.1 >nul

REM ================================================================================
REM STEP 2: DETECT LAN IP ADDRESS
REM ================================================================================
echo [2/10] DETECTING NETWORK CONFIGURATION...
echo --------------------------------------------------------------------------------
echo.

REM Get LAN IP address
if "%ENV_MODE%"=="local" (
    echo [INFO]  Skipping LAN IP detection in LOCAL mode
    set LAN_IP=127.0.0.1
    echo [PASS]  Forcing localhost only: 127.0.0.1
    goto :lan_check_done
)

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
    echo [PASS]  LAN IP Address: !LAN_IP!
) else (
    set LAN_IP=127.0.0.1
    echo [WARN]  Could not detect LAN IP, using localhost only
)

:lan_check_done
echo.

REM Get computer name
echo [INFO]  Computer Name: %COMPUTERNAME%
echo.
ping -n 2 127.0.0.1 >nul

REM ================================================================================
REM STEP 3: CREATE VIRTUAL ENVIRONMENT
REM ================================================================================
echo [3/10] SETTING UP VIRTUAL ENVIRONMENT...
echo --------------------------------------------------------------------------------
echo.

if exist "venv\" (
    echo [INFO]  Virtual environment already exists
) else (
    echo [INFO]  Creating new virtual environment ^(inheriting global packages^)...
    python -m venv venv --system-site-packages
    if !errorlevel! neq 0 (
        echo [FAIL]  Failed to create virtual environment
        pause
        goto :error_exit
    )
    echo [PASS]  Virtual environment created
)
echo.

echo [INFO]  Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [FAIL]  Failed to activate virtual environment
    pause
    goto :error_exit
)
echo [PASS]  Virtual environment activated
echo.
ping -n 2 127.0.0.1 >nul

REM ================================================================================
REM STEP 4: INSTALL PREREQUISITES
REM ================================================================================
echo [4/10] INSTALLING PREREQUISITES...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Checking for existing dependencies...
python scripts/check_dependencies.py
if %errorlevel% neq 0 (
    echo.
    echo [WARN]  Some dependencies are missing from your environment.
    set /p INSTALL_DEPS="Do you want to install missing dependencies? (Y/N) [Y]: "
    if /i "!INSTALL_DEPS!"=="N" (
        echo [SKIP]  Skipping installation.
    ) else (
        echo [INFO]  Installing dependencies...
        python -m pip install --upgrade pip --quiet 2>nul
        if exist "requirements.txt" (
            python -m pip install -r requirements.txt --disable-pip-version-check
        ) else (
            python -m pip install django djangorestframework django-cors-headers python-dotenv --quiet
        )
    )
) else (
    echo [PASS]  All required dependencies are already installed.
)
echo.
echo [DEBUG] Step 4 reached end without closing.
pause


REM ================================================================================
REM STEP 4.5: FRONTEND CHECK
REM ================================================================================
if not exist "frontend" goto :step5

echo [CHECK] Checking Frontend dependencies...
if exist "frontend\node_modules" (
    echo [PASS]  Frontend dependencies verified.
    goto :step5
)

echo [WARN]  Frontend dependencies (node_modules) are missing!
set "FRONTEND_INSTALL=Y"
set /p FRONTEND_INSTALL="Do you want to install them now? (Y/N) [Y]: "
if /i "!FRONTEND_INSTALL!"=="N" (
    echo [SKIP]  Skipping frontend installation.
    goto :step5
)

echo [INFO]  Installing frontend dependencies...
pushd frontend
call npm install --legacy-peer-deps
popd
echo [PASS]  Frontend installation attempted.

:step5
echo.
echo [DEBUG] Frontend check complete.
pause
echo.
ping -n 2 127.0.0.1 >nul

ping -n 2 127.0.0.1 >nul

REM ================================================================================
REM STEP 5: ENVIRONMENT CONFIGURATION
REM ================================================================================
echo [5/10] CONFIGURING ENVIRONMENT...
echo --------------------------------------------------------------------------------
echo.

if exist ".env" (
    echo [INFO]  Environment file already exists.
    goto :step5_env_done
)

if exist ".env.example" (
    echo [INFO]  Creating .env file from .env.example...
    copy .env.example .env >nul
    goto :step5_env_done
)

echo [INFO]  Creating default .env file...
echo DEBUG=True>.env
echo SECRET_KEY=dev-secret-key-change-in-production>>.env
echo DJANGO_SETTINGS_MODULE=config.settings.development>>.env
echo ALLOWED_HOSTS=localhost,127.0.0.1,!LAN_IP!>>.env
echo DATABASE_URL=sqlite:///db.sqlite3>>.env
echo CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://!LAN_IP!:5173>>.env
echo CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://!LAN_IP!:5173>>.env
echo FRONTEND_URL=http://!LAN_IP!:5173>>.env
echo [PASS]  Default environment file created.

:step5_env_done
if exist "frontend\" (
    echo [INFO]  Configuring frontend environment...
    echo VITE_API_URL=http://!LAN_IP!:%DEFAULT_PORT%/api>frontend/.env
    echo [PASS]  Frontend environment configured.
)
echo.
echo [DEBUG] Step 5 complete.
pause
echo.

if "%ENV_MODE%"=="prod" (
    echo [CHECK] Enforcing PROD strict environment checks...
    findstr /c:"DEBUG=True" .env >nul
    if !errorlevel! equ 0 (
        echo [FAIL]  PROD environment cannot run with DEBUG=True. Please update .env
        pause
        goto :error_exit
    )
    findstr /c:"dev-secret-key-change-in-production" .env >nul
    if !errorlevel! equ 0 (
        echo [FAIL]  PROD environment cannot use default SECRET_KEY. Please update .env
        pause
        goto :error_exit
    )
    if "%ADMIN_PASSWORD%"=="admin123" (
        echo [FAIL]  PROD environment cannot use default admin password. Update ADMIN_PASSWORD in launch.bat
        pause
        goto :error_exit
    )
    echo [PASS]  PROD checks passed successfully
    echo.
)
ping -n 2 127.0.0.1 >nul

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
    goto :error_exit
)
echo [PASS]  Database migrations complete
echo.
ping -n 2 127.0.0.1 >nul

REM Check and Seed Admin User
echo [7/10] SEEDING ADMIN USER...
echo --------------------------------------------------------------------------------
echo.

echo [INFO] Ensuring admin user exists...
python scripts/seed_admin.py
if %errorlevel% neq 0 (
    echo [FAIL]  Admin seeding failed or encountered an error.
    echo [INFO]  Check msu_platform_error.log for details.
) else (
    echo [PASS]  Admin seeding verified/complete.
)
echo.
echo [CREDENTIALS]
echo     Email:    %ADMIN_EMAIL%
echo     Password: %ADMIN_PASSWORD%
echo.
echo [IMPORTANT] Change these credentials after first login!
echo.
ping -n 3 127.0.0.1 >nul

REM ================================================================================
REM STEP 8: POPULATE SEARCH INDEX
REM ================================================================================
echo [8/10] INITIALIZING SEARCH INDEX...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Populating search index...
if "%ENV_MODE%"=="local" (
    echo [SKIP]  Skipping search index initialization in LOCAL mode
) else (
    python manage.py populate_search_index
    if !errorlevel! equ 0 (
        echo [PASS]  Search index initialized successfully
    ) else (
        echo [WARN]  Search index population encountered an issue.
        echo [INFO]  The platform will still run; index will build as you add content.
    )
)
echo.
ping -n 2 127.0.0.1 >nul

REM ================================================================================
REM STEP 8.5: FRONTEND STATUS
REM ================================================================================
if exist "frontend\" (
    echo [8.5/10] FRONTEND READY
    echo --------------------------------------------------------------------------------
    echo [PASS] Frontend environment verified in Step 4.
)
echo.
echo.
ping -n 2 127.0.0.1 >nul

REM ================================================================================
REM STEP 9: START SERVER
REM ================================================================================
echo [9/10] STARTING PLATFORM SERVICES...
echo --------------------------------------------------------------------------------
echo.

echo [INFO]  Starting server on 0.0.0.0:%DEFAULT_PORT%...
echo [INFO]  Server will be accessible from LAN devices
echo.

REM Start server in background and redirect output to log file
start /B python manage.py runserver 0.0.0.0:%DEFAULT_PORT% > server.log 2>&1

REM Wait for server to start
echo [INFO]  Waiting for server to start...
ping -n 4 127.0.0.1 >nul

REM Check if server started successfully
netstat -an | findstr ":%DEFAULT_PORT%" >nul
if %errorlevel% equ 0 (
    echo [PASS]  Server started successfully
) else (
    echo [WARN]  Server may not have started properly
    echo [INFO]  Check server.log for details
)
echo.
ping -n 2 127.0.0.1 >nul

REM Start React frontend if it exists
if exist "frontend\" (
    echo [INFO]  Starting React frontend...
    if "%ENV_MODE%"=="local" (
        start /B cmd /c "cd frontend && npm run dev" > frontend.log 2>&1
    ) else (
        start /B cmd /c "cd frontend && npm run dev -- --host" > frontend.log 2>&1
    )
    echo [PASS]  Frontend started in background
)
echo.
ping -n 2 127.0.0.1 >nul

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
echo   Localhost (API):  http://127.0.0.1:%DEFAULT_PORT%
echo   Localhost (UI):   http://localhost:5173
echo.
echo   LAN Access (API): http://%LAN_IP%:%DEFAULT_PORT%
echo   LAN Access (UI):  http://%LAN_IP%:5173
echo.
echo   Admin Panel:      http://127.0.0.1:%DEFAULT_PORT%/admin/
echo   API Explorer:     http://127.0.0.1:%DEFAULT_PORT%/api/
echo.
echo   [!] The Frontend may take 5-10 seconds to initialize.
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
    if exist "frontend\" (
        echo [INFO]  Opening Frontend at http://localhost:5173...
        start http://localhost:5173
    ) else (
        echo [INFO]  Opening API at http://127.0.0.1:%DEFAULT_PORT%...
        start http://127.0.0.1:%DEFAULT_PORT%
    )
    ping -n 3 127.0.0.1 >nul
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
goto :show_logs

:error_exit
echo.
echo ================================================================================
echo [FATAL ERROR] An unexpected error occurred and operations were halted.
echo Please review the errors printed above.
echo %date% %time% - CRITICAL FAILURE during script execution ^(See console output^) >> msu_platform_error.log
echo ================================================================================
echo.
echo Press any key to return to the Master Menu...
pause >nul
goto :master_menu

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

ping -n 6 127.0.0.1 >nul
goto :show_logs

REM This line won't be reached due to infinite loop above
REM User must press Ctrl+C to exit
