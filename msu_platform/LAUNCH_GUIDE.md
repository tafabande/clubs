# MSU Platform - One-Tap Launch Guide

**The easiest way to run the MSU Platform on Windows**

---

## 🚀 Quick Start

### One Command to Rule Them All

```batch
launch.bat
```

That's it! Double-click `launch.bat` or run it from command prompt, and the script will:

✅ **Automatically scan** your system for compatibility
✅ **Install prerequisites** (Python packages, dependencies)
✅ **Set up the database** (migrations, schema)
✅ **Create admin user** (pre-configured credentials)
✅ **Start the server** (accessible from LAN)
✅ **Display all access links** (localhost + LAN IP)
✅ **Show live status logs** (real-time monitoring)

---

## 📋 What the Script Does

### Step-by-Step Breakdown

**[1/10] System Compatibility Scan**
- ✓ Checks Windows version (Windows 10+ recommended)
- ✓ Verifies correct directory
- ✓ Checks Python installation (3.11+ required)
- ✓ Checks Python version compatibility
- ✓ Verifies pip is available
- ✓ Checks Git installation (optional)
- ✓ Verifies disk space
- ✓ Tests internet connectivity

**[2/10] Network Configuration**
- ✓ Detects LAN IP address automatically
- ✓ Displays computer name
- ✓ Prepares network access

**[3/10] Virtual Environment Setup**
- ✓ Creates Python virtual environment (if not exists)
- ✓ Activates virtual environment
- ✓ Isolates project dependencies

**[4/10] Prerequisites Installation**
- ✓ Upgrades pip, setuptools, wheel
- ✓ Installs all requirements from requirements.txt
- ✓ Shows progress and handles errors gracefully

**[5/10] Environment Configuration**
- ✓ Creates .env file from .env.example
- ✓ Configures DEBUG, SECRET_KEY, ALLOWED_HOSTS
- ✓ Sets database URL and Django settings

**[6/10] Database Setup**
- ✓ Runs all database migrations
- ✓ Creates tables and schema
- ✓ Applies Row-Level Security policies

**[7/10] Admin User Seeding**
- ✓ Creates superuser account automatically
- ✓ Pre-configured credentials (shown on screen)
- ✓ Skips if admin already exists
- ✓ **Email:** admin@msu.ac.zw
- ✓ **Password:** admin123

**[8/10] Search Index Initialization**
- ✓ Populates PostgreSQL full-text search index
- ✓ Prepares search functionality

**[9/10] Server Startup**
- ✓ Starts Django development server on 0.0.0.0:8000
- ✓ Accessible from LAN devices
- ✓ Logs output to server.log

**[10/10] Platform Ready**
- ✓ Displays localhost link: http://127.0.0.1:8000
- ✓ Displays LAN link: http://[YOUR_IP]:8000
- ✓ Shows admin credentials
- ✓ Opens browser automatically (optional)
- ✓ Streams live status logs

---

## 🖥️ What You'll See

### Example Output

```
================================================================================
       MSU PLATFORM - ONE-TAP LAUNCH
       Midlands State University Gweru Campus, Zimbabwe
================================================================================

This script will:
  [*] Scan system compatibility
  [*] Install prerequisites automatically
  [*] Set up the platform
  [*] Seed admin user
  [*] Display LAN and localhost links
  [*] Show real-time status logs

================================================================================

[1/10] SCANNING SYSTEM COMPATIBILITY...
--------------------------------------------------------------------------------

[CHECK] Windows Version: 10.0
[PASS]  Windows 10 or higher detected

[PASS]  Running from correct directory

[CHECK] Checking Python installation...
[PASS]  Python 3.11.5 detected

[PASS]  Python version is compatible

[CHECK] Checking pip installation...
[PASS]  pip is available

[CHECK] Checking Git installation...
[PASS]  Git 2.42.0 detected

[CHECK] Available disk space: 50,000,000,000 bytes
[PASS]  Sufficient disk space available

[CHECK] Checking internet connectivity...
[PASS]  Internet connection available

[PASS]  Compatibility scan complete!

[2/10] DETECTING NETWORK CONFIGURATION...
--------------------------------------------------------------------------------

[PASS]  LAN IP Address: 192.168.1.105

[INFO]  Computer Name: DESKTOP-MSU

[3/10] SETTING UP VIRTUAL ENVIRONMENT...
--------------------------------------------------------------------------------

[INFO]  Creating new virtual environment...
[PASS]  Virtual environment created

[INFO]  Activating virtual environment...
[PASS]  Virtual environment activated

[4/10] INSTALLING PREREQUISITES...
--------------------------------------------------------------------------------

[INFO]  Upgrading pip, setuptools, and wheel...
[PASS]  Package managers upgraded

[INFO]  Installing Django and dependencies from requirements.txt...
[INFO]  This may take 2-5 minutes on first run...

[PASS]  All dependencies installed successfully

[5/10] CONFIGURING ENVIRONMENT...
--------------------------------------------------------------------------------

[INFO]  Creating .env file from .env.example...
[PASS]  Environment file created

[6/10] SETTING UP DATABASE...
--------------------------------------------------------------------------------

[INFO]  Running database migrations...
[PASS]  Database migrations complete

[7/10] SEEDING ADMIN USER...
--------------------------------------------------------------------------------

[INFO]  Creating admin user...
[PASS]  Admin user created successfully

[CREDENTIALS]
    Email:    admin@msu.ac.zw
    Password: admin123

[IMPORTANT] Change these credentials after first login!

[8/10] INITIALIZING SEARCH INDEX...
--------------------------------------------------------------------------------

[INFO]  Populating search index...
[PASS]  Search index initialized

[9/10] STARTING DJANGO DEVELOPMENT SERVER...
--------------------------------------------------------------------------------

[INFO]  Starting server on 0.0.0.0:8000...
[INFO]  Server will be accessible from LAN devices

[INFO]  Waiting for server to start...
[PASS]  Server started successfully

[10/10] PLATFORM READY!
--------------------------------------------------------------------------------

================================================================================
                         MSU PLATFORM IS LIVE!
================================================================================

[ACCESS LINKS]

  Localhost:  http://127.0.0.1:8000
  LAN:        http://192.168.1.105:8000

  Admin Panel:     /admin/
  API Endpoints:   /api/
  Documentation:   /api/docs/

[ADMIN CREDENTIALS]

  Email:    admin@msu.ac.zw
  Password: admin123

  [!] CHANGE THESE CREDENTIALS AFTER FIRST LOGIN

[NETWORK ACCESS]

  Your platform is accessible from any device on your network at:
  http://192.168.1.105:8000

  Share this link with others on your network to allow access.

[SERVER STATUS]

  Status:   RUNNING
  Port:     8000
  Log file: server.log

================================================================================

Open platform in browser? (Y/N): Y

[INFO]  Opening http://127.0.0.1:8000 in default browser...

================================================================================
                         LIVE STATUS LOGS
================================================================================

Press Ctrl+C to stop the server and exit

Showing server logs (last 20 lines, updates every 5 seconds)...

--------------------------------------------------------------------------------
================================================================================
MSU PLATFORM - LIVE STATUS LOGS
================================================================================

[STATUS] Server running on http://192.168.1.105:8000
[TIME]   05/05/2026 15:30:45

--------------------------------------------------------------------------------
RECENT LOG ENTRIES:
--------------------------------------------------------------------------------

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 05, 2026 - 15:30:40
Django version 5.0.6, using settings 'config.settings.development'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.

--------------------------------------------------------------------------------
Press Ctrl+C to stop server | Refreshing in 5 seconds...
--------------------------------------------------------------------------------
```

---

## 🌐 Access the Platform

### From Your Computer

Open your browser and go to:
```
http://127.0.0.1:8000
```

### From Other Devices on Your Network

**Mobile phone, tablet, or another computer on the same WiFi/LAN:**

```
http://192.168.1.105:8000
```
*(Replace with your actual LAN IP shown in the script output)*

### Important Pages

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | http://127.0.0.1:8000 | Main platform homepage |
| **Admin Panel** | http://127.0.0.1:8000/admin/ | Django admin interface |
| **API Root** | http://127.0.0.1:8000/api/ | REST API endpoints |
| **API Docs** | http://127.0.0.1:8000/api/docs/ | API documentation |

---

## 🔐 Default Admin Credentials

**⚠️ IMPORTANT: Change these after first login!**

```
Email:    admin@msu.ac.zw
Password: admin123
```

### How to Change Password

1. Go to http://127.0.0.1:8000/admin/
2. Log in with the default credentials
3. Click on your username in the top-right corner
4. Select "Change password"
5. Enter new password and save

---

## 📊 Live Status Logs

The script shows **real-time server logs** that update every 5 seconds:

- **Request logs** - Every HTTP request made to the server
- **Error logs** - Any errors or warnings
- **System messages** - Django system checks and info
- **Performance** - Response times and query counts

### Log File

All logs are also saved to `server.log` in the msu_platform directory.

**View log file manually:**
```batch
type server.log
```

**View last 20 lines:**
```batch
powershell -command "Get-Content server.log -Tail 20"
```

---

## 🛠️ Prerequisites

### Required

- **Windows 10+** (Windows 11 recommended)
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
  - ⚠️ During installation, check "Add Python to PATH"
- **Internet connection** - For installing dependencies

### Optional

- **Git** - [Download](https://git-scm.com/download/win) - For version control
- **PostgreSQL** - For production database (SQLite used by default)
- **Redis** - For caching and Celery (optional)

---

## ❓ Troubleshooting

### "Python is not installed or not in PATH"

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Restart your command prompt
4. Run `launch.bat` again

### "Failed to install dependencies"

**Solution 1: Check internet connection**
```batch
ping google.com
```

**Solution 2: Install dependencies manually**
```batch
cd msu_platform
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Solution 3: Use verbose installation**
```batch
pip install -r requirements.txt -v
```

### "Database migration failed"

**Solution: Delete database and try again**
```batch
del db.sqlite3
python manage.py migrate
```

### "Port 8000 already in use"

**Solution 1: Stop other servers**
```batch
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

**Solution 2: Use different port**
Edit `launch.bat` and change:
```batch
set "DEFAULT_PORT=8001"
```

### "Could not detect LAN IP"

**Solution: Check network adapter**
```batch
ipconfig
```
Look for "IPv4 Address" under your active network adapter.

### Server won't start

**Check server.log for details:**
```batch
type server.log
```

**Common issues:**
- Port already in use (see above)
- Missing dependencies (reinstall requirements.txt)
- Database locked (close other Python processes)

---

## 🔄 Stopping the Server

**Method 1: Press Ctrl+C in the terminal**

**Method 2: Close the command prompt window**

**Method 3: Kill Python process**
```batch
taskkill /IM python.exe /F
```

---

## 🚀 Advanced Usage

### Run with Custom Port

Edit `launch.bat` and change:
```batch
set "DEFAULT_PORT=9000"
```

### Run with Sample Data

After the platform starts, open a new terminal:
```batch
cd msu_platform
venv\Scripts\activate
python manage.py populate_sample_data
```

This creates:
- 50 MSU Gweru students
- 21 clubs
- 7 churches
- 9 sports teams
- 10 campus activities
- Realistic posts and engagement

### Run Tests

```batch
cd msu_platform
venv\Scripts\activate
pytest -v
```

### View All Available Commands

```batch
cd msu_platform
venv\Scripts\activate
python manage.py --help
```

---

## 📱 Mobile Access

### Same WiFi Network

1. Make sure your phone/tablet is on the **same WiFi network** as your computer
2. Note the LAN IP shown in the launch script (e.g., 192.168.1.105)
3. Open browser on mobile device
4. Go to: `http://192.168.1.105:8000`

### Firewall Issues

If you can't access from mobile:

**Windows Defender Firewall:**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Click "Change settings"
4. Click "Allow another app"
5. Browse to: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\python.exe`
6. Add and check both Private and Public networks

---

## 💡 Tips

### Faster Subsequent Launches

After the first run:
- Virtual environment exists ✓
- Dependencies installed ✓
- Database migrated ✓
- Admin user created ✓

**Next launches will be much faster** (30-60 seconds instead of 3-5 minutes)

### Keep Terminal Open

Don't close the command prompt window while using the platform. The server runs in this window and shows live logs.

### Bookmark Access Links

Save these for quick access:
- http://127.0.0.1:8000 (Localhost)
- http://127.0.0.1:8000/admin/ (Admin Panel)
- http://[YOUR_LAN_IP]:8000 (LAN Access)

### Monitor Performance

Watch the live logs to see:
- Response times
- Database queries
- Error messages
- User activity

---

## 📚 Next Steps

After launching:

1. **Change admin password** (security!)
2. **Explore admin panel** - Create clubs, churches, teams
3. **Test API endpoints** - /api/
4. **Create test users** - Register new accounts
5. **Populate sample data** - `python manage.py populate_sample_data`
6. **Read documentation** - Check MASTER_SUMMARY.md

---

## 🆚 Comparison with Other Launch Methods

| Feature | launch.bat | start_local.bat | start_docker.bat |
|---------|-----------|----------------|------------------|
| **Setup Time (First Run)** | 3-5 min | 5-10 min | 5 min |
| **Setup Time (Subsequent)** | 30-60 sec | 1-2 min | 1 min |
| **Compatibility Scan** | ✅ Yes | ❌ No | ❌ No |
| **Auto-Install Prerequisites** | ✅ Yes | ⚠️ Manual | ⚠️ Requires Docker |
| **Auto-Seed Admin** | ✅ Yes | ⚠️ Manual | ⚠️ Manual |
| **Show LAN Link** | ✅ Yes | ❌ No | ❌ No |
| **Live Status Logs** | ✅ Yes | ❌ No | ⚠️ Manual |
| **Network Access** | ✅ Auto-configured | ⚠️ Manual | ✅ Yes |
| **Production-Like** | ❌ No (Dev server) | ❌ No | ✅ Yes (All services) |
| **Best For** | 🏆 First-time users | Developers | Production simulation |

**Recommendation:**
- **First time?** → Use `launch.bat` (easiest)
- **Development?** → Use `start_local.bat` (fast)
- **Testing production?** → Use `start_docker.bat` (complete)

---

## 🎓 For MSU Gweru Staff

### Demonstration Setup

**Before demonstration:**
1. Run `launch.bat` (one-tap setup)
2. Wait for "PLATFORM READY!" message
3. Populate sample data: `python manage.py populate_sample_data`
4. Open http://127.0.0.1:8000 in browser

**During demonstration:**
- Show localhost link to presenter
- Share LAN link with audience (mobile access)
- Admin credentials on screen for easy reference
- Live logs show real-time activity

### Training Sessions

**For staff training:**
1. Each trainer runs `launch.bat` on their computer
2. LAN IP shown automatically
3. Trainees access via LAN link on tablets/phones
4. Everyone can explore simultaneously
5. Live logs help troubleshoot issues

---

## 📞 Support

### Getting Help

**Check the logs:**
```batch
type server.log
```

**Common issues:**
- See **Troubleshooting** section above
- Check **MASTER_SUMMARY.md** for complete documentation
- Review **README.md** for platform overview

**Documentation files:**
- `LAUNCH_GUIDE.md` (this file)
- `MASTER_SUMMARY.md` - Complete platform summary
- `README.md` - Project overview
- `TESTING_GUIDE.md` - Testing documentation
- `DEPLOY.md` - Production deployment

---

## ✅ Checklist

Before running `launch.bat`:

- [ ] Python 3.11+ installed
- [ ] "Add Python to PATH" checked during installation
- [ ] Internet connection available
- [ ] In correct directory (msu_platform folder)
- [ ] No other servers running on port 8000

After successful launch:

- [ ] Server shows "PLATFORM READY!"
- [ ] Localhost link accessible
- [ ] LAN link accessible (from mobile)
- [ ] Admin login works
- [ ] Live logs showing

---

**🚀 You're ready to launch the MSU Platform with a single command!**

```batch
launch.bat
```

---

*Last Updated: May 5, 2026*
*Version: 1.0*
*For: Midlands State University Gweru Campus, Zimbabwe*
