# School Clubs Login Platform

Simple Flask application that provides club registration and login for school clubs. Uses SQLite for storage and secure password hashing.

Quick start (PowerShell):

```powershell
# 1. Create virtualenv
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize the database
python init_db.py

# 4. Run the app
$env:FLASK_APP = 'app.py'; flask run

# Open http://127.0.0.1:5000 in your browser
```

Files:
- `app.py` - main Flask app
- `init_db.py` - initializes the SQLite database
- `templates/` - HTML templates for login/register/dashboard
- `static/style.css` - basic styles

Next steps:
- Add club management UI, roles (officer/member), and email verification.
