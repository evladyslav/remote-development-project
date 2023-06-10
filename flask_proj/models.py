from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Reservation(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))