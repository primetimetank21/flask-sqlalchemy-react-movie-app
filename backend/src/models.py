from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # type: ignore

db = SQLAlchemy()


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "users"

    # Login/Registration information
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Movie relationship
    movies = db.relationship("Movie", back_populates="user")


class Movie(db.Model):  # type: ignore
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="movies")
