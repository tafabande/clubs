from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime


class Club(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    description: Optional[str] = None
    category: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))


from datetime import date


class ClubHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    club_id: int = Field(foreign_key="club.id")
    date: date
    members: int = 0
    events: int = 0
