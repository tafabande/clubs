# MSU Platform - Quick Reference Card

**One-page reference for running the MSU Platform**

---

## 🚀 Fastest Way to Start

```batch
launch.bat
```

Double-click and you're done! ✅

---

## 📋 All Launch Commands

| Command | Use Case | Time |
|---------|----------|------|
| **launch.bat** ⭐ | First time / Easiest | 3-5 min |
| **start_local.bat** | Development | 5 min |
| **start_with_sample_data.bat** | Demos | 6-12 min |
| **start_docker.bat** | Docker quick | 5 min |
| **start_full_stack.bat** | Production test | 8-15 min |
| **stop_all.bat** | Stop services | 10 sec |
| **test_platform.bat** | Run tests | 2-3 min |

---

## 🌐 Access Links

### After launch.bat:
```
Localhost: http://127.0.0.1:8000
LAN:       http://[YOUR_IP]:8000
Admin:     http://127.0.0.1:8000/admin/
API:       http://127.0.0.1:8000/api/
```

### After Docker:
```
Localhost: http://localhost
Admin:     http://localhost/admin/
API:       http://localhost/api/
```

---

## 🔐 Default Admin Credentials

**Email:** admin@msu.ac.zw
**Password:** admin123

⚠️ **CHANGE AFTER FIRST LOGIN!**

---

## 🛑 How to Stop

1. Press **Ctrl+C** in terminal
2. Or close Command Prompt window
3. Or run `stop_all.bat` (Docker)

---

## 🆘 Quick Troubleshooting

### Python not found
```
Install: https://www.python.org/downloads/
Check: "Add Python to PATH" during install
```

### Port already in use
```batch
netstat -ano | findstr :8000
taskkill /PID [NUMBER] /F
```

### Docker not running
```
Start Docker Desktop
Wait for green icon
Retry
```

---

## 📊 What You Get

### launch.bat gives you:
✅ Auto compatibility scan
✅ Auto prerequisites install
✅ Auto database setup
✅ Auto admin creation
✅ Localhost + LAN links
✅ Live status logs

### start_full_stack.bat gives you:
✅ PostgreSQL database
✅ Redis caching
✅ Celery workers
✅ Nginx server
✅ Production environment
✅ Port 80 (like production)

---

## 🎯 Common Commands

### View logs
```batch
type server.log
powershell -command "Get-Content server.log -Tail 20"
```

### Run tests
```batch
test_platform.bat
```

### Add sample data
```batch
cd msu_platform
venv\Scripts\activate
python manage.py populate_sample_data
```

### Create new admin
```batch
python manage.py createsuperuser
```

---

## 📱 Mobile/LAN Access

1. Run **launch.bat**
2. Note LAN IP (e.g., 192.168.1.105)
3. On phone/tablet: http://192.168.1.105:8000
4. Must be on same WiFi network

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **LAUNCH_GUIDE.md** | Complete launch.bat docs |
| **QUICK_START_COMPARISON.md** | Compare methods |
| **BATCH_FILES_SUMMARY.md** | All batch files |
| **README.md** | Project overview |
| **MASTER_SUMMARY.md** | Full summary |

---

## ✅ Success Check

### You'll see this when it works:

```
================================================================================
                         MSU PLATFORM IS LIVE!
================================================================================

[ACCESS LINKS]
  Localhost:  http://127.0.0.1:8000
  LAN:        http://192.168.1.105:8000
```

### Then:
1. Open browser to localhost link
2. Login with admin credentials
3. Start exploring!

---

## 🎓 For MSU Gweru

### Quick Demo Setup:
```batch
start_with_sample_data.bat
```

**Gets you:**
- 50 students
- 21 clubs
- 7 churches
- 9 sports teams
- 10 activities
- Realistic posts

### LAN Demo:
```batch
launch.bat
```

**Share LAN link with audience for mobile access**

---

## 💡 Pro Tips

### Faster subsequent launches
After first run, launch.bat takes only 30-60 seconds

### Keep terminal open
Server runs in terminal window - don't close it

### Bookmark links
Save http://127.0.0.1:8000/admin/ for quick access

### Watch logs
Live logs show all activity in real-time

---

**🚀 Ready? Just run: launch.bat**

---

*Quick Reference | MSU Platform v3.0 | May 5, 2026*
