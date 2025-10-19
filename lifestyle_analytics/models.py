from __future__ import annotations
from datetime import datetime, date
from typing import Optional

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, Date, DateTime, Text

from .app import db, login_manager


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(UserMixin, db.Model, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(120))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[Optional[str]] = mapped_column(String(20))
    height_m: Mapped[Optional[float]] = mapped_column(Float)
    weight_kg: Mapped[Optional[float]] = mapped_column(Float)
    bmi: Mapped[Optional[float]] = mapped_column(Float)
    experience_level: Mapped[Optional[int]] = mapped_column(Integer)  # 1-3

    # Relationships
    workouts: Mapped[list[WorkoutLog]] = relationship("WorkoutLog", back_populates="user")
    nutritions: Mapped[list[NutritionLog]] = relationship("NutritionLog", back_populates="user")
    daily_stats: Mapped[list[DailyStats]] = relationship("DailyStats", back_populates="user")

    def get_id(self) -> str:
        return str(self.id)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return db.session.get(User, int(user_id))


class WorkoutLog(db.Model, TimestampMixin):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Workout & performance fields
    max_bpm: Mapped[Optional[int]] = mapped_column(Integer)
    avg_bpm: Mapped[Optional[int]] = mapped_column(Integer)
    resting_bpm: Mapped[Optional[int]] = mapped_column(Integer)
    session_duration_hours: Mapped[Optional[float]] = mapped_column(Float)
    calories_burned: Mapped[Optional[int]] = mapped_column(Integer)
    workout_type: Mapped[Optional[str]] = mapped_column(String(50))
    workout_frequency: Mapped[Optional[int]] = mapped_column(Integer)  # days/week snapshot
    fat_percentage: Mapped[Optional[float]] = mapped_column(Float)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="workouts")


class NutritionLog(db.Model, TimestampMixin):
    __tablename__ = "nutrition_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    daily_meals_frequency: Mapped[Optional[int]] = mapped_column(Integer)
    carbs_g: Mapped[Optional[int]] = mapped_column(Integer)
    proteins_g: Mapped[Optional[int]] = mapped_column(Integer)
    fats_g: Mapped[Optional[int]] = mapped_column(Integer)
    calories: Mapped[Optional[int]] = mapped_column(Integer)
    water_intake_liters: Mapped[Optional[float]] = mapped_column(Float)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="nutritions")


class Meal(db.Model, TimestampMixin):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    meal_name: Mapped[Optional[str]] = mapped_column(String(50))
    meal_type: Mapped[Optional[str]] = mapped_column(String(50))
    diet_type: Mapped[Optional[str]] = mapped_column(String(50))
    sugar_g: Mapped[Optional[int]] = mapped_column(Integer)
    sodium_mg: Mapped[Optional[int]] = mapped_column(Integer)
    cholesterol_mg: Mapped[Optional[int]] = mapped_column(Integer)
    serving_size_g: Mapped[Optional[int]] = mapped_column(Integer)
    cooking_method: Mapped[Optional[str]] = mapped_column(String(50))
    prep_time_min: Mapped[Optional[int]] = mapped_column(Integer)
    cook_time_min: Mapped[Optional[int]] = mapped_column(Integer)
    is_healthy: Mapped[Optional[bool]] = mapped_column(Boolean)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    user: Mapped[User] = relationship("User")


class Exercise(db.Model, TimestampMixin):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_of_exercise: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    sets: Mapped[Optional[int]] = mapped_column(Integer)
    reps: Mapped[Optional[int]] = mapped_column(Integer)
    benefit: Mapped[Optional[str]] = mapped_column(Text)
    burns_calories_per_30min: Mapped[Optional[int]] = mapped_column(Integer)
    target_muscle_group: Mapped[Optional[str]] = mapped_column(String(120))
    equipment_needed: Mapped[Optional[str]] = mapped_column(String(120))
    difficulty_level: Mapped[Optional[str]] = mapped_column(String(50))
    body_part: Mapped[Optional[str]] = mapped_column(String(50))
    type_of_muscle: Mapped[Optional[str]] = mapped_column(String(50))


class DailyStats(db.Model, TimestampMixin):
    __tablename__ = "daily_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    # Aggregated daily metrics
    total_calories_burned: Mapped[Optional[int]] = mapped_column(Integer)
    total_calories_intake: Mapped[Optional[int]] = mapped_column(Integer)
    avg_session_duration_hours: Mapped[Optional[float]] = mapped_column(Float)
    avg_max_bpm: Mapped[Optional[int]] = mapped_column(Integer)
    avg_resting_bpm: Mapped[Optional[int]] = mapped_column(Integer)
    bmi: Mapped[Optional[float]] = mapped_column(Float)
    body_fat_percentage: Mapped[Optional[float]] = mapped_column(Float)
    consistency_score: Mapped[Optional[int]] = mapped_column(Integer)

    user: Mapped[User] = relationship("User", back_populates="daily_stats")
