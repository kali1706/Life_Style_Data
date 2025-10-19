from __future__ import annotations

from flask import Blueprint, Flask, jsonify, render_template


bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/health")
def health() -> tuple[dict, int]:
    return {"status": "ok"}, 200


@bp.get("/dashboard_data")
def dashboard_data():
    # Static sample data for initial scaffolding
    return jsonify(
        {
            "weekly": {
                "workouts": 5,
                "calories_burned": 2500,
                "avg_session_minutes": 45,
                "meals_logged": 21,
                "avg_daily_intake": 2100,
                "macro_avg": {"carbs": 45, "protein": 25, "fat": 30},
                "bmi": 23.5,
                "body_fat": 18.2,
                "consistency": 92,
            }
        }
    )


def init_app(app: Flask) -> None:
    app.register_blueprint(bp)
