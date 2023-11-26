"""
class News(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String, nullable=False)
        url = db.Column(db.String, unique=True, nullable=False)
        published = db.Column(db.DateTime, nullable=False)
        text = db.Column(db.Text, nullable=True)
"""
from sqlmodel import SQLModel, Field
from datetime import datetime


class News(SQLModel):
    title: str
    url: str
    published: datetime.day
    content: str
