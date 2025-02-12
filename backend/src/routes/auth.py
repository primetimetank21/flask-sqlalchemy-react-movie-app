from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash  # check_password_hash
from ..models import User, db
from ..schemas import UserSchema

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    register_data = request.get_json()
    if not register_data:
        return jsonify({"message": "No payload received"}), 400

    try:
        user_schema = UserSchema().load(register_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 400

    user_schema["password"] = generate_password_hash(user_schema["password"])
    new_user = User(**user_schema)

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
def get_user(user_id: str):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {"message": "User found", "data": UserSchema(exclude=["password"]).dump(user)}
    ), 200


@auth.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "User logged in"}), 200


@auth.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "User logged out"}), 200
