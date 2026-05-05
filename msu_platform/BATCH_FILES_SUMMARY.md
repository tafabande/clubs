# MSU Platform - Batch Files Summary

**All available Windows batch files for easy platform management**

---

## 📂 Available Batch Files

### 1. 🌟 launch.bat - One-Tap Launch (RECOMMENDED)

**Purpose:** The easiest way to run the MSU Platform with automatic setup

**What it does:**
- ✅ Scans system compatibility (Windows, Python, pip, Git, disk space, network)
- ✅ Detects LAN IP address automatically
- ✅ Creates/activates virtual environment
- ✅ Installs all prerequisites from requirements.txt
- ✅ Creates .env configuration
- ✅ Runs database migrations
- ✅ **Auto-creates admin user** (admin@msu.ac.zw / admin123)
- ✅ Populates search index
- ✅ Starts server on 0.0.0.0:8000
- ✅ **Displays localhost AND LAN links**
- ✅ **Shows live status logs** (updates every 5 seconds)
- ✅ Opens browser automatically (optional)

**Usage:**
```batch
launch.bat
```

**Access:**
- Localhost: http://127.0.0.1:8000
- LAN: http://[YOUR_IP]:8000
- Admin: admin@msu.ac.zw / admin123

**Best for:**
- First-time users
- Quick demos
- Non-technical users
- LAN/network access

**Documentation:** [LAUNCH_GUIDE.md](LAUNCH_GUIDE.md)

---

### 2. 🛠️ start_local.bat - Simple Development Server

**Purpose:** Fast Django development server for developers

**What it does:**
- Creates/activates virtual environment
- Installs dependencies
- Runs migrations
- Prompts for superuser creation
- Starts Django development server
- Shows server logs

**Usage:**
```batch
start_local.bat
```

**Access:**
- Localhost: http://127.0.0.1:8000

**Best for:**
- Developers
- Quick testing
- Minimal setup

---

### 3. 📚 start_with_sample_data.bat - With MSU Gweru Data

**Purpose:** Launch with pre-loaded MSU Gweru sample data

**What it does:**
- Everything in start_local.bat, plus:
- Populates search index
- Runs populate_sample_data command
- Creates 50 students, 21 clubs, 7 churches, 9 teams, 10 activities
- Realistic posts and engagement

**Usage:**
```batch
start_with_sample_data.bat
```

**Access:**
- Localhost: http://127.0.0.1:8000
- Admin: Create with prompt

**Best for:**
- Demonstrations
- Training sessions
- Testing with realistic data

---

### 4. 🐳 start_docker.bat - Quick Docker Start

**Purpose:** Simplified Docker deployment

**What it does:**
- Checks Docker installation
- Creates .env from .env.example
- Runs docker-compose up -d
- Opens browser automatically
- Shows logs

**Usage:**
```batch
start_docker.bat
```

**Access:**
- Localhost: http://localhost (port 80)

**Best for:**
- Production simulation
- Complete stack (PostgreSQL, Redis, Celery)
- Docker users

**Requires:** Docker Desktop

---

### 5. 🏗️ start_full_stack.bat - Production Simulation

**Purpose:** Complete production environment locally

**What it does:**
- Checks Docker installation
- Creates .env configuration
- Starts all 6 services (PostgreSQL, Redis, Django, Nginx, Celery Worker, Celery Beat)
- Runs migrations
- Creates superuser
- Opens browser
- **Shows the exact production environment**

**Usage:**
```batch
start_full_stack.bat
```

**Access:**
- Localhost: http://localhost (port 80, like production)

**Best for:**
- Pre-deployment testing
- Integration testing
- Performance testing

**Requires:** Docker Desktop

---

### 6. 🛑 stop_all.bat - Stop All Services

**Purpose:** Clean shutdown of all Docker services

**What it does:**
- Runs docker-compose down
- Stops all containers
- Removes networks
- Clean exit

**Usage:**
```batch
stop_all.bat
```

**Best for:**
- Stopping Docker services
- Cleanup after testing

**Requires:** Docker Desktop

---

### 7. 🧪 test_platform.bat - Run Test Suite

**Purpose:** Execute comprehensive test suite

**What it does:**
- Activates virtual environment
- Installs pytest and test dependencies
- Sets test environment (config.settings.testing)
- Runs database migrations for tests
- Executes pytest with verbose output
- Shows test results and suggestions

**Usage:**
```batch
test_platform.bat
```

**Best for:**
- Running tests
- Verifying functionality
- Quality assurance

---

## 🎯 Quick Reference

| Batch File | Setup Time | Complexity | Best For |
|-----------|-----------|-----------|----------|
| **launch.bat** ⭐ | 3-5 min | Very Easy | First-time users, demos |
| **start_local.bat** | 5-10 min | Easy | Developers |
| **start_with_sample_data.bat** | 6-12 min | Easy | Demonstrations |
| **start_docker.bat** | 5-10 min | Medium | Docker users |
| **start_full_stack.bat** | 8-15 min | Medium | Pre-deployment testing |
| **stop_all.bat** | 10 sec | Very Easy | Stopping services |
| **test_platform.bat** | 2-3 min | Easy | Running tests |

---

## 🚀 Recommended Workflow

### For First-Time Users

```batch
# 1. Launch platform
launch.bat

# 2. Access platform
# Open http://127.0.0.1:8000 in browser

# 3. Login as admin
# Email: admin@msu.ac.zw
# Password: admin123

# 4. Explore platform

# 5. Stop when done (Ctrl+C)
```

---

### For Demonstrations

```batch
# 1. Launch with sample data
start_with_sample_data.bat

# 2. Access platform
# Open http://127.0.0.1:8000

# 3. Show pre-loaded MSU Gweru content
# - 50 students
# - 21 clubs
# - 7 churches
# - 9 sports teams
# - Realistic posts

# 4. Stop when done (Ctrl+C)
```

---

### For Development

```batch
# 1. Start development server
start_local.bat

# 2. Make code changes

# 3. Test changes
test_platform.bat

# 4. Restart server (Ctrl+C then start_local.bat again)
```

---

### For Production Testing

```batch
# 1. Start full stack
start_full_stack.bat

# 2. Test complete environment
# Access http://localhost

# 3. Stop all services
stop_all.bat
```

---

## 📊 Feature Comparison

| Feature | launch.bat | start_local.bat | start_with_sample_data.bat | start_docker.bat | start_full_stack.bat |
|---------|-----------|----------------|---------------------------|-----------------|---------------------|
| **Auto Prerequisites** | ✅ | ❌ | ❌ | ⚠️ Docker | ⚠️ Docker |
| **Auto Admin User** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Compatibility Scan** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Show LAN Link** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Live Status Logs** | ✅ | ❌ | ❌ | ⚠️ Manual | ⚠️ Manual |
| **Sample Data** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **PostgreSQL** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Redis** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Celery** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Nginx** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Production-Like** | ❌ | ❌ | ❌ | ⚠️ Partial | ✅ |

---

## 🎓 For MSU Gweru IT Staff

### Setup for Campus Demonstration

**Day Before:**
```batch
# Test launch on demo computer
launch.bat

# Verify everything works
# Access http://127.0.0.1:8000

# Stop server
# Press Ctrl+C
```

**Day of Demonstration:**
```batch
# 1. Start with sample data
start_with_sample_data.bat

# 2. Note the LAN IP shown (e.g., 192.168.1.105)

# 3. Share LAN link with audience
# http://192.168.1.105:8000

# 4. Present platform features
# - Show clubs, churches, teams
# - Demonstrate posts, comments, likes
# - Show search functionality

# 5. Allow audience to access from phones/tablets
```

### Training Session Setup

**For Each Trainer Computer:**
```batch
launch.bat
```

**Share with Trainees:**
- LAN link from launch.bat output
- Admin credentials: admin@msu.ac.zw / admin123
- Allow hands-on exploration

---

## 🔧 Customization

### Change Admin Credentials

Edit `launch.bat` (lines 10-13):
```batch
set "ADMIN_EMAIL=your.email@msu.ac.zw"
set "ADMIN_PASSWORD=your_password"
set "ADMIN_FIRST_NAME=Your"
set "ADMIN_LAST_NAME=Name"
```

### Change Default Port

Edit batch file:
```batch
set "DEFAULT_PORT=9000"
```

### Disable Auto-Browser Open

In `launch.bat`, comment out:
```batch
REM start http://127.0.0.1:%DEFAULT_PORT%
```

---

## 🆘 Troubleshooting

### Batch File Won't Run

**Problem:** Double-clicking does nothing

**Solution:**
```batch
# Right-click batch file
# Select "Edit" to check syntax
# Or run from Command Prompt to see errors
```

### Python Not Found

**Problem:** "Python is not installed or not in PATH"

**Solution:**
1. Install Python 3.11+ from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt
4. Run batch file again

### Port Already in Use

**Problem:** "Port 8000 is already in use"

**Solution 1 - Stop other processes:**
```batch
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

**Solution 2 - Use different port:**
Edit batch file and change `DEFAULT_PORT`

### Docker Not Running

**Problem:** "Docker is not running"

**Solution:**
1. Open Docker Desktop
2. Wait for it to fully start (green icon)
3. Run batch file again

### Virtual Environment Issues

**Problem:** "Failed to create virtual environment"

**Solution:**
```batch
# Delete existing venv
rmdir /s /q venv

# Run batch file again (will recreate)
```

---

## 📝 Log Files

### server.log

**Location:** `msu_platform/server.log`

**Contains:**
- Django server output
- Request logs
- Error messages
- System checks

**View:**
```batch
type server.log
```

**View last 20 lines:**
```batch
powershell -command "Get-Content server.log -Tail 20"
```

**Clear log:**
```batch
del server.log
```

---

## 🎯 Decision Guide

**Start here:** What do you want to do?

### I want the easiest setup
→ Use **launch.bat** ⭐

### I want to demonstrate the platform
→ Use **start_with_sample_data.bat** 📚

### I'm a developer
→ Use **start_local.bat** 🛠️

### I want to test production setup
→ Use **start_full_stack.bat** 🏗️

### I just want Docker
→ Use **start_docker.bat** 🐳

### I want to run tests
→ Use **test_platform.bat** 🧪

### I want to stop everything
→ Use **stop_all.bat** 🛑

---

## 📚 Related Documentation

- **LAUNCH_GUIDE.md** - Detailed launch.bat documentation
- **QUICK_START_COMPARISON.md** - Compare all launch methods
- **README.md** - Project overview
- **MASTER_SUMMARY.md** - Complete platform summary
- **TESTING_GUIDE.md** - Testing documentation
- **DEPLOY.md** - Production deployment

---

## ✅ Quick Checklist

Before running any batch file:

- [ ] Windows 10+ installed
- [ ] Python 3.11+ installed (for non-Docker methods)
- [ ] "Add Python to PATH" checked during installation
- [ ] Internet connection available
- [ ] In correct directory (msu_platform folder)
- [ ] Docker Desktop running (for Docker methods)

---

## 🎉 Success Indicators

### launch.bat Success:
```
[10/10] PLATFORM READY!
================================================================================
                         MSU PLATFORM IS LIVE!
================================================================================

[ACCESS LINKS]
  Localhost:  http://127.0.0.1:8000
  LAN:        http://192.168.1.105:8000
```

### Docker Success:
```
✅ All services started successfully
🌐 Platform available at: http://localhost
```

### Test Success:
```
================================================================================
256 passed in 45.23s
================================================================================
```

---

**🚀 Choose your batch file and launch the MSU Platform in minutes!**

*Recommended: launch.bat for first-time users*

---

*Last Updated: May 5, 2026*
*Version: 1.0*
*For: Midlands State University Gweru Campus, Zimbabwe*
