import os
from flask import Flask
from models import db


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configuration
    from config import BaseConfig
    app.config.from_object(BaseConfig)

    # Extensions
    db.init_app(app)

    # Create database tables if not existing
    with app.app_context():
        db.create_all()

    # Routes / Blueprints
    import routes as routes_module
    routes_module.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
