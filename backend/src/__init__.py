from uuid import uuid4
from pathlib import Path
from flask import Flask
from .models import db
from .routes.auth import login_manager


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    DB_PATH: Path = Path(Path.cwd(), ".db.sqlite3")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = uuid4().hex

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        db.create_all()

    from .routes.health_check import health_check
    from .routes.auth import auth

    app.register_blueprint(health_check)
    app.register_blueprint(auth)

    return app
