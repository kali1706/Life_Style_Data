from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db: SQLAlchemy = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    height_m = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)
    experience_level = db.Column(db.Integer, nullable=True)  # 1=Beginner, 2=Intermediate, 3=Advanced

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    workout_logs = db.relationship("WorkoutLog", back_populates="user", cascade="all, delete-orphan")
    nutrition_logs = db.relationship("NutritionLog", back_populates="user", cascade="all, delete-orphan")
    daily_stats = db.relationship("DailyStats", back_populates="user", cascade="all, delete-orphan")
    meals = db.relationship("Meal", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class WorkoutLog(db.Model):
    __tablename__ = "workout_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    logged_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    max_bpm = db.Column(db.Integer, nullable=True)
    avg_bpm = db.Column(db.Integer, nullable=True)
    resting_bpm = db.Column(db.Integer, nullable=True)
    session_duration_hours = db.Column(db.Float, nullable=True)
    calories_burned = db.Column(db.Integer, nullable=True)
    workout_type = db.Column(db.String(50), nullable=True)  # Strength, HIIT, Cardio, etc.
    workout_frequency_per_week = db.Column(db.Integer, nullable=True)  # 0-7
    fat_percentage = db.Column(db.Float, nullable=True)

    user = db.relationship("User", back_populates="workout_logs")


class NutritionLog(db.Model):
    __tablename__ = "nutrition_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    logged_on = db.Column(db.Date, default=date.today, nullable=False)
    daily_meals_frequency = db.Column(db.Integer, nullable=True)
    carbs_g = db.Column(db.Integer, nullable=True)
    proteins_g = db.Column(db.Integer, nullable=True)
    fats_g = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    water_intake_liters = db.Column(db.Float, nullable=True)

    user = db.relationship("User", back_populates="nutrition_logs")
    meals = db.relationship("Meal", back_populates="nutrition_log", cascade="all, delete-orphan")


class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    nutrition_log_id = db.Column(db.Integer, db.ForeignKey("nutrition_logs.id"), nullable=True, index=True)

    meal_name = db.Column(db.String(50), nullable=True)  # Breakfast, Lunch, Dinner, Snack
    meal_type = db.Column(db.String(50), nullable=True)  # Main, Snack, Beverage
    diet_type = db.Column(db.String(50), nullable=True)  # Keto, Vegan, Balanced, etc.
    sugar_g = db.Column(db.Integer, nullable=True)
    sodium_mg = db.Column(db.Integer, nullable=True)
    cholesterol_mg = db.Column(db.Integer, nullable=True)
    serving_size_g = db.Column(db.Integer, nullable=True)
    cooking_method = db.Column(db.String(50), nullable=True)  # Boiled, Fried, Grilled, Baked
    prep_time_min = db.Column(db.Integer, nullable=True)
    cook_time_min = db.Column(db.Integer, nullable=True)
    is_healthy = db.Column(db.Boolean, default=None, nullable=True)

    user = db.relationship("User", back_populates="meals")
    nutrition_log = db.relationship("NutritionLog", back_populates="meals")


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name_of_exercise = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    benefit = db.Column(db.Text, nullable=True)
    burns_calories_per_30min = db.Column(db.Integer, nullable=True)
    target_muscle_group = db.Column(db.String(100), nullable=True)
    equipment_needed = db.Column(db.String(100), nullable=True)
    difficulty_level = db.Column(db.String(50), nullable=True)  # Beginner, Intermediate, Advanced
    body_part = db.Column(db.String(50), nullable=True)  # Arms, Legs, Chest, Back, Core
    type_of_muscle = db.Column(db.String(50), nullable=True)  # Upper, Lower, Core, Grip Strength


class DailyStats(db.Model):
    __tablename__ = "daily_stats"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    stat_date = db.Column(db.Date, default=date.today, nullable=False)
    weight_kg = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)
    fat_percentage = db.Column(db.Float, nullable=True)
    resting_bpm = db.Column(db.Integer, nullable=True)
    consistency_score = db.Column(db.Integer, nullable=True)  # 0-100

    user = db.relationship("User", back_populates="daily_stats")
