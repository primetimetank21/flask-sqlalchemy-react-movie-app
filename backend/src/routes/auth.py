from flask import Blueprint, jsonify, request
from flask_login import (  # type: ignore
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db
from ..schemas import UserSchema

auth = Blueprint("auth", __name__)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route("/register", methods=["POST"])
def register():
    register_data = request.get_json()
    if not register_data:
        return jsonify({"message": "No payload received"}), 400

    try:
        user_dict = UserSchema().load(register_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 400

    user_dict["password"] = generate_password_hash(user_dict["password"])
    new_user = User(**user_dict)

    if User.query.filter_by(email=new_user.email).first():
        return jsonify({"message": "User already exists"}), 400

    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            "message": "User registered",
            "data": UserSchema(exclude=["password"]).dump(new_user),
        }
    ), 201


@auth.route("/user/<user_id>", methods=["GET"])
@login_required
def get_user(user_id: str):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {"message": "User found", "data": UserSchema(exclude=["password"]).dump(user)}
    ), 200


@auth.route("/login", methods=["POST"])
def login():
    login_data = request.get_json()
    if not login_data:
        return jsonify({"message": "No payload received"}), 400

    try:
        user_schema = UserSchema().load(login_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 400

    user = User.query.filter_by(
        email=user_schema["email"], username=user_schema["username"]
    ).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user.password, user_schema["password"]):
        return jsonify({"message": "Invalid password"}), 401

    login_user(user)

    return jsonify({"message": "User logged in"}), 200


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "User logged out"}), 200


@auth.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify(
        {
            "message": "User found",
            "data": UserSchema(exclude=["password"]).dump(current_user),
        }
    ), 200
