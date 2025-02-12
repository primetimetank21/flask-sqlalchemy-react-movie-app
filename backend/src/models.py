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

    # TODO: add movie class-related information
