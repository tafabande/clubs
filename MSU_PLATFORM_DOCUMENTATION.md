# MSU Platform: Operations & Debugging Guide

This guide is streamlined specifically for operating, monitoring, and debugging the MSU Platform in production and development environments. All legacy setup info has been deprecated in favor of the unified `launch.bat` script.

## 1. Operating the Platform

### Unified Launch Script (`launch.bat`)
The entire platform is now operated through a single master script located at `msu_platform/launch.bat`. Running this script presents an interactive menu to handle all platform operations:

```powershell
# Run the master script
.\msu_platform\launch.bat
```

**Launch Environments:**
1. **Local Mode:** Bypasses strict internet/Windows checks and forces local binding (`127.0.0.1`). Fastest for offline testing.
2. **Online Mode:** Standard LAN/Internet deployment checks.
3. **Prod Mode:** Ultra-strict security checks (enforces `DEBUG=False`, secure `SECRET_KEY`, and strong admin passwords).

### Start, Stop, and Database Operations
All legacy scripts (`start_docker.bat`, `stop_all.bat`, etc.) have been integrated directly into the `launch.bat` master menu.

## 2. Debugging & Error Handling

The platform uses a standardized JSON error format and custom exceptions mapped to HTTP status codes. 

### Common Error Codes & Meanings
- `VALIDATION_ERROR` (400): Client sent invalid data format.
- `TOKEN_EXPIRED` (401): User session JWT has expired.
- `PERMISSION_DENIED` (403): User role lacks access to resource.
- `NOT_FOUND` (404): Requested entity does not exist.
- `RATE_LIMIT_EXCEEDED` (429): User exceeded the 500 req/hr limit.
- `STORAGE_ERROR` / `DATABASE_ERROR` (500): Backend infrastructure failure.

### Log Architecture
Live logs are streamed directly to the terminal when running `launch.bat`. For deep debugging, check the log files:
- `server.log`: Captures all Django development server output, errors, and system messages.

*To view the last 20 errors in real-time on Windows:*
```powershell
Get-Content msu_platform\server.log -Tail 20 -Wait
```

### Common Troubleshooting Scenarios

**1. Port 8000 Already in Use**
- Identify the process blocking the port: `netstat -ano | findstr :8000`
- Kill the process: `taskkill /PID [PID_NUMBER] /F`

**2. Database Migration Failures**
If the schema gets corrupted during development:
- Delete the SQLite database: `del db.sqlite3`
- Re-run migrations via the `launch.bat` initialization.

**3. Missing Static Files (CSS/JS not loading)**
If running in production or behind a web server, ensure static files are collected:
- `python manage.py collectstatic --noinput --clear`

## 3. Production Health Monitoring

For production environments, the platform exposes dedicated health check endpoints that monitor infrastructure status:
- **Overall System Health:** `GET /health/detailed/`
- **Database Status:** `GET /health/db/`
- **Redis/Cache Status:** `GET /health/redis/`

If you are using **Sentry** for error tracking, ensure your `.env` contains:
```env
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
ENVIRONMENT=production
```
Sentry will automatically catch all unhandled exceptions (500s) and provide stack traces linked to the user's request.
