# 🚀 START HERE - MSU Platform Quick Start

**New to the project? Start here!**

This is your 5-minute guide to get the MSU Platform running.

---

## ⚡ Super Quick Start (5 Minutes)

### Using Docker (Easiest - Recommended)

```bash
# 1. Make sure Docker is installed
docker --version
docker-compose --version

# 2. Navigate to project folder
cd msu_platform

# 3. Copy environment file
cp .env.example .env

# 4. Start everything
docker-compose up -d

# 5. Run database setup
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py populate_search_index

# 6. Open browser
# Visit: http://localhost
# Admin: http://localhost/admin
```

**Done! 🎉 The application is now running.**

---

## 🐍 Alternative: Local Python Setup (10 Minutes)

### If you don't have Docker:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate     # Mac/Linux
# OR
venv\Scripts\activate        # Windows

# 3. Install packages
pip install -r requirements.txt

# 4. Setup database
cp .env.example .env
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Index search
python manage.py populate_search_index

# 7. Run server
python manage.py runserver

# 8. Open browser
# Visit: http://localhost:8000
# Admin: http://localhost:8000/admin
```

**Done! 🎉 The application is now running.**

---

## 📱 What Can You Do Now?

### As a User:
1. **Register**: Create your account
2. **Browse**: View clubs, churches, teams, activities
3. **Join**: Become a member of organizations
4. **Post**: Share updates, events, achievements
5. **Engage**: Like, comment, share posts
6. **Search**: Find organizations by name or category

### As an Admin (after creating superuser):
1. **Login**: Visit `/admin` with superuser credentials
2. **Manage**: Create and approve organizations
3. **Moderate**: Review and manage posts
4. **Users**: Manage user accounts and permissions
5. **Analytics**: View popular searches and engagement

---

## 🎯 Key URLs

| Purpose | URL | Description |
|---------|-----|-------------|
| **Home** | http://localhost | Main application |
| **Admin** | http://localhost/admin | Django admin panel |
| **API** | http://localhost/api | REST API root |
| **Clubs** | http://localhost/api/clubs/ | List all clubs |
| **Posts** | http://localhost/api/posts/ | Social feed |
| **Search** | http://localhost/api/search/?q=tech | Search organizations |

---

## 💡 First Steps Tutorial

### 1. Create Your First Club

**Via Admin Panel:**
1. Go to http://localhost/admin
2. Login with superuser
3. Click "Clubs" → "Add Club"
4. Fill in:
   - Name: "Tech Club"
   - Description: "Technology enthusiasts"
   - Category: "technology"
   - Email: "tech@msu.ac.zw"
   - Is approved: ✓
5. Click "Save"

**Via API:**
```bash
curl -X POST http://localhost/api/clubs/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Club",
    "description": "Technology enthusiasts",
    "category": "technology",
    "email": "tech@msu.ac.zw"
  }'
```

### 2. Create Your First Post

**Via Admin Panel:**
1. Go to http://localhost/admin
2. Click "Posts" → "Add Post"
3. Fill in:
   - Author: (select your user)
   - Content type: "club"
   - Object ID: (your club's ID)
   - Post type: "announcement"
   - Title: "Welcome!"
   - Content: "Welcome to Tech Club!"
   - Visibility: "public"
4. Click "Save"

### 3. Search for Organizations

**Via Browser:**
```
Visit: http://localhost/api/search/?q=tech
```

**Via API:**
```bash
curl http://localhost/api/search/?q=tech
```

---

## 🛠️ Useful Commands

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Run Django command
docker-compose exec web python manage.py [command]

# Access Django shell
docker-compose exec web python manage.py shell

# Restart web service
docker-compose restart web
```

### Django Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Populate search index
python manage.py populate_search_index

# Collect static files
python manage.py collectstatic

# Shell access
python manage.py shell
```

---

## 🐛 Something Not Working?

### Common Issues and Fixes

**1. "Port already in use"**
```bash
# Check what's using the port
lsof -i :8000  # or :80 for Docker

# Kill it
kill -9 <PID>

# Or use different port
docker-compose up -d --scale web=1
```

**2. "Database connection error"**
```bash
# Docker: Check PostgreSQL is running
docker-compose ps

# Local: Check .env file has correct DATABASE_URL
```

**3. "Static files not loading"**
```bash
# Docker
docker-compose exec web python manage.py collectstatic

# Local
python manage.py collectstatic
```

**4. "Module not found"**
```bash
# Make sure you're in virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 What to Read Next

### For Development:
1. **README.md** - Full project overview
2. **ENHANCED_FEATURES_GUIDE.md** - Code examples
3. **API_DOCUMENTATION.md** - API reference

### For Deployment:
1. **DEPLOY.md** - Complete deployment guide
2. **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist
3. **QUICK_REFERENCE.md** - Command reference

### For Understanding:
1. **PROJECT_STATUS.md** - What's been built
2. **MIGRATION_GUIDE.md** - Database structure
3. **FINAL_SUMMARY.md** - Complete overview

---

## ⚙️ Configuration Tips

### Development (.env file):
```env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (.env file):
```env
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-min-50-chars
DATABASE_URL=postgresql://user:pass@localhost:5432/msu_platform
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

---

## 🎓 Learning Path

### Week 1: Basics
- [ ] Get application running
- [ ] Create superuser
- [ ] Explore admin panel
- [ ] Create test organizations
- [ ] Test feed functionality

### Week 2: Features
- [ ] Understand organization types
- [ ] Test membership workflows
- [ ] Explore post types
- [ ] Test search functionality
- [ ] Review API endpoints

### Week 3: Customization
- [ ] Read ENHANCED_FEATURES_GUIDE.md
- [ ] Customize themes
- [ ] Add new features
- [ ] Test on different devices

### Week 4: Deployment
- [ ] Read DEPLOY.md
- [ ] Set up production environment
- [ ] Configure SSL/HTTPS
- [ ] Deploy to server
- [ ] Set up monitoring

---

## 🆘 Need Help?

### Quick Fixes:
1. **Check logs**: `docker-compose logs -f` or application logs
2. **Restart**: `docker-compose restart web`
3. **Clean start**: `docker-compose down && docker-compose up -d`

### Documentation:
- **QUICK_REFERENCE.md** - Common commands
- **DEPLOY.md** - Troubleshooting section
- **README.md** - Overview and setup

### Community:
- **GitHub Issues**: Report bugs
- **Documentation**: Check all MD files
- **Code Comments**: Read inline comments

---

## ✅ Success Checklist

After following this guide, you should be able to:

- [ ] Access the application in browser
- [ ] Login to admin panel
- [ ] Create organizations (clubs, churches, teams, activities)
- [ ] Create posts
- [ ] Like and comment on posts
- [ ] Search for organizations
- [ ] View trending searches
- [ ] Manage users and permissions

**If you can do all of the above, you're ready to start developing! 🎉**

---

## 🚀 Ready to Go Further?

### Next Steps:
1. **Customize**: Modify themes, add features
2. **Deploy**: Follow DEPLOY.md for production
3. **Scale**: Add more servers, databases
4. **Monitor**: Set up logging and alerts

### Resources:
- **All Documentation**: Check all .md files
- **Code Examples**: ENHANCED_FEATURES_GUIDE.md
- **API Reference**: API_DOCUMENTATION.md

---

**Welcome to MSU Platform! Happy coding! 🎉**

*Last Updated: May 5, 2026*
*Version: 2.0*

---

**Remember:** This guide gets you started. For complete information, read README.md and other documentation files.
