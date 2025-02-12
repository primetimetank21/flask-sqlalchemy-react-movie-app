from flask import Blueprint

health_check = Blueprint("health_check", __name__, url_prefix="/health-check")


@health_check.route("/", methods=["GET"])
def ping():
    return "pong"


@health_check.route("/hello", methods=["GET"])
def hello():
    return "Hello world"
