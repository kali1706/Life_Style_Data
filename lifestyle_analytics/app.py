from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

# Initialize extensions
_db = SQLAlchemy()
_login_manager = LoginManager()
_login_manager.login_view = "auth.login"


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    # init extensions
    _db.init_app(app)
    _login_manager.init_app(app)

    # Blueprints
    from .routes import auth_bp, profile_bp, workout_bp, nutrition_bp, analytics_bp, report_bp, pages_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(nutrition_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(pages_bp)

    # Create tables in dev if not exist
    with app.app_context():
        from .models import db  # noqa: F401
        _db.create_all()

    return app

# expose db and login_manager for other modules

db = _db
login_manager = _login_manager


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
