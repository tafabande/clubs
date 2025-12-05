"""Seed the database with dummy clubs and monthly history."""
from datetime import date, datetime, timedelta
import random
from sqlmodel import Session, create_engine, select
from models import Club, ClubHistory

DB_URL = 'sqlite:///clubs.db'
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SAMPLE_CLUBS = [
    { 'name': 'Robotics Club', 'email': 'robotics@msu.edu', 'description': 'Build and program robots', 'category':'Engineering' },
    { 'name': 'Chess Club', 'email': 'chess@msu.edu', 'description': 'Weekly chess meetups', 'category':'Games' },
    { 'name': 'Environmental Alliance', 'email': 'enviro@msu.edu', 'description': 'Volunteer and sustainability projects', 'category':'Environmental' },
    { 'name': 'Programming Guild', 'email': 'code@msu.edu', 'description': 'Coding workshops and hackathons', 'category':'Technology' },
    { 'name': 'Music Ensemble', 'email': 'music@msu.edu', 'description': 'Instrumental and vocal groups', 'category':'Arts' },
]

def seed():
    with Session(engine) as session:
        # add clubs only if DB empty
        existing = session.exec(select(Club)).first()
        if existing:
            print('Database already seeded (club found).')
            return

        for c in SAMPLE_CLUBS:
            club = Club(name=c['name'], email=c['email'], password_hash='seeded',
                        description=c.get('description',''), category=c.get('category',''))
            session.add(club)
        session.commit()

        # create 12 months of history for each club
        clubs = list(session.exec(select(Club)).all())
        today = date.today()
        for club in clubs:
            base_members = random.randint(10, 120)
            for m in range(12, 0, -1):
                d = (today.replace(day=1) - timedelta(days=30*m)).replace(day=1)
                # small variation
                members = max(1, base_members + random.randint(-10, 15))
                events = max(0, random.randint(0, 6))
                hist = ClubHistory(club_id=club.id, date=d, members=members, events=events)
                session.add(hist)
        session.commit()
        print('Seeded database with sample clubs and history.')

if __name__ == '__main__':
    seed()
