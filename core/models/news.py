"""
class News(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String, nullable=False)
        url = db.Column(db.String, unique=True, nullable=False)
        published = db.Column(db.DateTime, nullable=False)
        text = db.Column(db.Text, nullable=True)
"""
from sqlalchemy.orm import Mapped
from .base import Base


class News(Base):
    title: Mapped[str]
    url: Mapped[str]
    published: Mapped[str]
    content: Mapped[str]
