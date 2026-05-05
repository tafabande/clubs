"""Seed the database with dummy clubs and monthly history.

This updated seeder reads `static/clubs.json` (if present) and inserts
clubs into the SQLModel/SQLite DB. Seeded clubs get a hashed default
password so they can log in for demo purposes.
"""
from datetime import date, timedelta
import random
import json
import os
from sqlmodel import Session, create_engine, select
from models import Club, ClubHistory
from werkzeug.security import generate_password_hash

DB_URL = 'sqlite:///clubs.db'
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

DEFAULT_PASSWORD = 'password123'


def load_json_clubs(path: str):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed():
    with Session(engine) as session:
        # add clubs only if DB empty
        existing = session.exec(select(Club)).first()
        if existing:
            print('Database already seeded (club found).')
            return

        clubs_data = load_json_clubs(os.path.join(os.path.dirname(__file__), 'static', 'clubs.json'))
        if not clubs_data:
            clubs_data = [
                { 'name': 'Robotics Club', 'email': 'robotics@msu.edu', 'description': 'Build and program robots', 'category':'Engineering' },
                { 'name': 'Chess Club', 'email': 'chess@msu.edu', 'description': 'Weekly chess meetups', 'category':'Games' },
                { 'name': 'Environmental Alliance', 'email': 'enviro@msu.edu', 'description': 'Volunteer and sustainability projects', 'category':'Environmental' },
            ]

        # Insert clubs with hashed default password
        for c in clubs_data:
            # Avoid duplicating by email
            existing = session.exec(select(Club).where(Club.email == c['email'])).first()
            if existing:
                continue
            club = Club(
                name=c.get('name'),
                email=c.get('email'),
                password_hash=generate_password_hash(DEFAULT_PASSWORD),
                description=c.get('description',''),
                category=c.get('category',''),
                website=c.get('website','')
            )
            session.add(club)
        session.commit()

        # create 12 months of history for each club
        clubs = list(session.exec(select(Club)).all())
        today = date.today()
        for club in clubs:
            base_members = random.randint(10, 120)
            for m in range(12, 0, -1):
                d = (today.replace(day=1) - timedelta(days=30*m)).replace(day=1)
                members = max(1, base_members + random.randint(-10, 15))
                events = max(0, random.randint(0, 6))
                hist = ClubHistory(club_id=club.id, date=d, members=members, events=events)
                session.add(hist)
        session.commit()
        print('Seeded database with sample clubs and history. Default password for seeded clubs is:', DEFAULT_PASSWORD)


if __name__ == '__main__':
    seed()
