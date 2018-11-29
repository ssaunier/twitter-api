from datetime import datetime
from sqlalchemy.schema import ForeignKey

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship("User", back_populates="tweets")

    def __repr__(self):
        return f"<Tweet #{self.id}>"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(200))
    api_key = db.Column(db.String(80))
    tweets = db.relationship('Tweet', back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
