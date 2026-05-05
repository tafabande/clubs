# MSU Platform - Quick Start Comparison

**Choose the best launch method for your needs**

---

## 🎯 Which Method Should I Use?

### 🌟 launch.bat - One-Tap Launch (RECOMMENDED for Windows)

**Best for:**
- ✅ First-time users
- ✅ Quick demonstrations
- ✅ Non-technical users
- ✅ LAN/network access needed
- ✅ Want automatic setup

**Pros:**
- 🚀 Easiest method - just double-click
- 🔍 Automatic compatibility scanning
- 📦 Auto-installs prerequisites
- 👤 Auto-creates admin user
- 🌐 Shows LAN link for network access
- 📊 Live status logs
- ⚡ Fast setup (3-5 min first run, 30-60 sec after)

**Cons:**
- 🪟 Windows only
- 🔧 Development server (not production-grade)
- 💾 SQLite database (not PostgreSQL)

**Command:**
```batch
launch.bat
```

**Access:**
- Localhost: http://127.0.0.1:8000
- LAN: http://[YOUR_IP]:8000
- Admin: admin@msu.ac.zw / admin123

---

### 🐳 start_docker.bat - Docker Quick Start

**Best for:**
- ✅ Production simulation
- ✅ Testing complete stack
- ✅ Need PostgreSQL + Redis
- ✅ Want all 6 services running
- ✅ Closer to production environment

**Pros:**
- 🏗️ Complete production stack
- 🗄️ PostgreSQL database
- ⚡ Redis caching
- 🔄 Celery workers + beat
- 🌐 Nginx reverse proxy
- 📦 Containerized (consistent environment)

**Cons:**
- 🐋 Requires Docker Desktop
- 💻 More resource-intensive
- ⏱️ Slower startup (downloads images)

**Command:**
```batch
start_docker.bat
```

**Access:**
- Localhost: http://localhost (port 80)
- Admin: Create with `docker-compose exec web python manage.py createsuperuser`

---

### 🛠️ start_local.bat - Simple Development

**Best for:**
- ✅ Developers
- ✅ Quick testing
- ✅ Minimal setup
- ✅ Don't need Docker

**Pros:**
- ⚡ Fast startup
- 💻 Low resource usage
- 🔧 Easy to modify code
- 🐍 Direct Python execution

**Cons:**
- 📝 Manual admin creation
- 🔧 Manual prerequisite checks
- 💾 SQLite only
- ❌ No LAN link shown

**Command:**
```batch
start_local.bat
```

**Access:**
- Localhost: http://127.0.0.1:8000
- Admin: Run `python manage.py createsuperuser`

---

### 📊 start_with_sample_data.bat - With MSU Gweru Data

**Best for:**
- ✅ Demonstrations
- ✅ Testing with realistic data
- ✅ Training sessions
- ✅ Understanding platform features

**Pros:**
- 📚 Pre-loaded with MSU Gweru data
- 👥 50 students, 21 clubs, 7 churches, 9 teams
- 📝 Realistic posts and engagement
- 🎓 Authentic MSU Gweru context
- 👤 Auto-creates admin

**Cons:**
- ⏱️ Longer initial setup (loads all sample data)
- 💾 SQLite database
- 🪟 Windows only

**Command:**
```batch
start_with_sample_data.bat
```

**Access:**
- Localhost: http://127.0.0.1:8000
- Admin: admin@msu.ac.zw / admin123

---

### 🏗️ start_full_stack.bat - Production Simulation

**Best for:**
- ✅ Pre-deployment testing
- ✅ Exact production environment
- ✅ Performance testing
- ✅ Integration testing

**Pros:**
- 🎯 Exact production replica
- 🗄️ All 6 services (PostgreSQL, Redis, Django, Nginx, Celery Worker, Celery Beat)
- 🌐 Accessible on port 80 (like production)
- 📦 Docker containerized
- ⚡ Redis caching enabled

**Cons:**
- 🐋 Requires Docker Desktop
- 💻 Most resource-intensive
- ⏱️ Slower startup
- 🔧 More complex troubleshooting

**Command:**
```batch
start_full_stack.bat
```

**Access:**
- Localhost: http://localhost (port 80)
- Admin: Create with `docker-compose exec web python manage.py createsuperuser`

---

## 📊 Feature Comparison Table

| Feature | launch.bat | start_docker.bat | start_local.bat | start_with_sample_data.bat | start_full_stack.bat |
|---------|-----------|-----------------|----------------|---------------------------|---------------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Setup Time (First)** | 3-5 min | 5-10 min | 5-10 min | 6-12 min | 8-15 min |
| **Setup Time (After)** | 30-60 sec | 1-2 min | 1 min | 2-3 min | 2-3 min |
| **Compatibility Scan** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Auto Prerequisites** | ✅ Yes | ⚠️ Needs Docker | ⚠️ Manual | ⚠️ Manual | ⚠️ Needs Docker |
| **Auto Admin User** | ✅ Yes | ❌ Manual | ❌ Manual | ✅ Yes | ❌ Manual |
| **Show LAN Link** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Live Status Logs** | ✅ Yes | ⚠️ Manual | ❌ No | ❌ No | ⚠️ Manual |
| **Database** | SQLite | PostgreSQL | SQLite | SQLite | PostgreSQL |
| **Redis Cache** | ❌ No | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Celery Tasks** | ❌ No | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Nginx** | ❌ No | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Sample Data** | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **LAN Access** | ✅ Auto | ✅ Yes | ⚠️ Manual | ✅ Auto | ✅ Yes |
| **Production-Like** | ❌ No | ⚠️ Partial | ❌ No | ❌ No | ✅ Yes |
| **Resource Usage** | Low | Medium | Low | Low | High |
| **Platform** | Windows | Any | Windows | Windows | Any |

---

## 🎯 Decision Tree

```
START HERE
│
├─ Are you on Windows?
│  ├─ NO → Use start_docker.bat (Docker)
│  └─ YES → Continue...
│
├─ Is this your first time?
│  ├─ YES → Use launch.bat ⭐ (Easiest!)
│  └─ NO → Continue...
│
├─ Do you need sample data for demo?
│  ├─ YES → Use start_with_sample_data.bat
│  └─ NO → Continue...
│
├─ Do you have Docker installed?
│  ├─ NO → Use start_local.bat
│  └─ YES → Continue...
│
├─ Testing production deployment?
│  ├─ YES → Use start_full_stack.bat
│  └─ NO → Use start_docker.bat
```

---

## 🌟 Recommendations by Use Case

### 👨‍🎓 Student / First-Time User
**Use:** `launch.bat`
- Easiest to use
- No technical knowledge needed
- Automatic everything
- Clear instructions

### 👨‍💼 Demonstration / Training
**Use:** `start_with_sample_data.bat`
- Pre-loaded MSU Gweru data
- Realistic content
- Auto admin credentials
- Perfect for showcasing features

### 👨‍💻 Developer
**Use:** `start_local.bat` or `start_docker.bat`
- Fast iteration
- Easy code changes
- Docker if need PostgreSQL/Redis

### 🚀 Pre-Production Testing
**Use:** `start_full_stack.bat`
- Exact production environment
- All services running
- Performance testing
- Integration testing

### 🎓 MSU Gweru IT Staff
**Use:** `launch.bat` for demos, `start_full_stack.bat` for testing
- Easy demos with launch.bat
- Test deployment with start_full_stack.bat
- Train users with start_with_sample_data.bat

---

## ⚡ Quick Reference

### Fastest Setup
```batch
launch.bat
```
3-5 minutes, everything automatic.

### Most Realistic
```batch
start_full_stack.bat
```
Exact production environment.

### Best for Demos
```batch
start_with_sample_data.bat
```
Pre-loaded with MSU Gweru data.

### Simplest (No Docker)
```batch
start_local.bat
```
Just Django development server.

---

## 🛠️ Setup Requirements

### All Methods
- Windows 10+ (for .bat files)
- Python 3.11+
- Internet connection

### Docker Methods (start_docker.bat, start_full_stack.bat)
- Docker Desktop installed
- 4GB+ RAM available
- 10GB+ disk space

### Non-Docker Methods (launch.bat, start_local.bat, start_with_sample_data.bat)
- Virtual environment support
- pip (Python package manager)
- 2GB+ RAM available

---

## 📝 After Launch

### All Methods

**Access the platform:**
- Open your browser
- Go to localhost link (shown in terminal)
- For admin panel: add `/admin/` to the URL

**Default admin credentials (where auto-created):**
- Email: admin@msu.ac.zw
- Password: admin123
- ⚠️ Change after first login!

**Stop the server:**
- Press `Ctrl+C` in terminal
- Or close the command prompt window

---

## 🆘 Troubleshooting

### Method Won't Start

**Try in this order:**

1. **launch.bat** - Most user-friendly, auto-checks everything
2. **start_local.bat** - Simple Python server
3. **start_docker.bat** - If Docker is installed
4. **start_full_stack.bat** - Complete stack

### Common Issues

**"Python not found"**
- Solution: Install Python 3.11+ and check "Add to PATH"
- Then retry launch.bat

**"Port already in use"**
- Solution: Stop other servers on port 8000/80
- Or edit batch file to use different port

**"Docker not running"**
- Solution: Start Docker Desktop
- Wait for it to fully start (icon turns green)
- Then retry

**Dependencies failed**
- Solution: Use launch.bat (auto-installs)
- Or manually: `pip install -r requirements.txt`

---

## 📚 Documentation

- **LAUNCH_GUIDE.md** - Complete launch.bat documentation
- **README.md** - Project overview
- **MASTER_SUMMARY.md** - Complete platform summary
- **DEPLOY.md** - Production deployment guide

---

## 🎉 Success Indicators

You'll know it's working when you see:

**launch.bat:**
```
[10/10] PLATFORM READY!
================================================================================
                         MSU PLATFORM IS LIVE!
================================================================================
```

**start_docker.bat / start_full_stack.bat:**
```
✅ All services started successfully
🌐 Platform available at: http://localhost
```

**start_local.bat:**
```
Django version 5.0.6, using settings 'config.settings.development'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

---

**🚀 Choose your method and get started in minutes!**

*Recommended for most users: launch.bat*

---

*Last Updated: May 5, 2026*
*Version: 1.0*
*For: Midlands State University Gweru Campus, Zimbabwe*
