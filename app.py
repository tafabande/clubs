from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlmodel import select, Session, create_engine
from models import Club
from datetime import datetime

DB_URL = 'sqlite:///clubs.db'

app = Flask(__name__)
app.secret_key = 'change-this-secret-in-production'

# SQLModel engine
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'club_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'club_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        description = request.form.get('description')
        category = request.form.get('category')
        if not (name and email and password):
            flash('All fields are required')
            return render_template('register.html')

        with Session(engine) as db:
            # Check existing
            existing = db.exec(select(Club).where(Club.email == email)).first()
            if existing:
                flash('A club with that email already exists')
                return render_template('register.html')

            club = Club(name=name, email=email, password_hash=generate_password_hash(password),
                        description=description, category=category, created_at=datetime.utcnow())
            db.add(club)
            db.commit()
            flash('Registration successful — please log in')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        with Session(engine) as db:
            row = db.exec(select(Club).where(Club.email == email)).first()
            if row and check_password_hash(row.password_hash, password):
                session.clear()
                session['club_id'] = row.id
                session['club_name'] = row.name
                return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # Dashboard is mostly static front-end; session available for server-side features
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/clubs')
def api_clubs():
    with Session(engine) as db:
        clubs = db.exec(select(Club)).all()
        data = []
        for c in clubs:
            data.append({
                'id': c.id,
                'name': c.name,
                'email': c.email,
                'description': c.description,
                'category': c.category,
                'website': c.website,
                'created_at': c.created_at.isoformat() if c.created_at else None,
            })
    return jsonify(data)


@app.route('/api/clubs/<int:club_id>')
def api_club(club_id: int):
    with Session(engine) as db:
        c = db.get(Club, club_id)
        if not c:
            return jsonify({'error': 'not found'}), 404
        return jsonify({
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'description': c.description,
            'category': c.category,
            'website': c.website,
            'created_at': c.created_at.isoformat() if c.created_at else None,
        })


@app.route('/api/clubs/<int:club_id>/history')
def api_club_history(club_id: int):
    with Session(engine) as db:
        rows = db.exec(select(ClubHistory).where(ClubHistory.club_id == club_id).order_by(ClubHistory.date)).all()
        data = [{'date': r.date.isoformat(), 'members': r.members, 'events': r.events} for r in rows]
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
