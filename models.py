from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Profile Data
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    weight = db.Column(db.Float)  # kg
    height = db.Column(db.Float)  # meters
    bmi = db.Column(db.Float)
    experience_level = db.Column(db.Integer)  # 1=Beginner, 2=Intermediate, 3=Advanced
    fat_percentage = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    workouts = db.relationship('WorkoutLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    nutrition_logs = db.relationship('NutritionLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    daily_stats = db.relationship('DailyStats', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmi(self):
        if self.height and self.weight:
            self.bmi = round(self.weight / (self.height ** 2), 2)
            return self.bmi
        return None
    
    def get_bmi_category(self):
        if not self.bmi:
            return "Unknown"
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'weight': self.weight,
            'height': self.height,
            'bmi': self.bmi,
            'experience_level': self.experience_level,
            'fat_percentage': self.fat_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Workout Data
    max_bpm = db.Column(db.Integer)
    avg_bpm = db.Column(db.Integer)
    resting_bpm = db.Column(db.Integer)
    session_duration = db.Column(db.Float)  # hours
    calories_burned = db.Column(db.Integer)
    workout_type = db.Column(db.String(50))
    workout_frequency = db.Column(db.Integer)  # days per week
    
    # Exercise Details
    exercise_name = db.Column(db.String(100))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    benefit = db.Column(db.Text)
    burns_calories_per_30min = db.Column(db.Integer)
    target_muscle_group = db.Column(db.String(100))
    equipment_needed = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    body_part = db.Column(db.String(50))
    type_of_muscle = db.Column(db.String(50))
    
    # Timestamps
    workout_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'max_bpm': self.max_bpm,
            'avg_bpm': self.avg_bpm,
            'resting_bpm': self.resting_bpm,
            'session_duration': self.session_duration,
            'calories_burned': self.calories_burned,
            'workout_type': self.workout_type,
            'workout_frequency': self.workout_frequency,
            'exercise_name': self.exercise_name,
            'sets': self.sets,
            'reps': self.reps,
            'benefit': self.benefit,
            'burns_calories_per_30min': self.burns_calories_per_30min,
            'target_muscle_group': self.target_muscle_group,
            'equipment_needed': self.equipment_needed,
            'difficulty_level': self.difficulty_level,
            'body_part': self.body_part,
            'type_of_muscle': self.type_of_muscle,
            'workout_date': self.workout_date.isoformat() if self.workout_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class NutritionLog(db.Model):
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Daily Nutrition Data
    daily_meals_frequency = db.Column(db.Integer)
    carbs = db.Column(db.Integer)  # grams
    proteins = db.Column(db.Integer)  # grams
    fats = db.Column(db.Integer)  # grams
    calories = db.Column(db.Integer)
    water_intake = db.Column(db.Float)  # liters
    
    # Meal Details
    meal_name = db.Column(db.String(50))  # Breakfast, Lunch, Dinner, Snack
    meal_type = db.Column(db.String(20))  # Main, Snack, Beverage
    diet_type = db.Column(db.String(20))  # Keto, Vegan, Balanced, etc.
    sugar = db.Column(db.Integer)  # grams
    sodium = db.Column(db.Integer)  # mg
    cholesterol = db.Column(db.Integer)  # mg
    serving_size = db.Column(db.Integer)  # grams
    cooking_method = db.Column(db.String(20))  # Boiled, Fried, Grilled, Baked
    prep_time = db.Column(db.Integer)  # minutes
    cook_time = db.Column(db.Integer)  # minutes
    is_healthy = db.Column(db.Boolean, default=True)
    
    # Timestamps
    log_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'daily_meals_frequency': self.daily_meals_frequency,
            'carbs': self.carbs,
            'proteins': self.proteins,
            'fats': self.fats,
            'calories': self.calories,
            'water_intake': self.water_intake,
            'meal_name': self.meal_name,
            'meal_type': self.meal_type,
            'diet_type': self.diet_type,
            'sugar': self.sugar,
            'sodium': self.sodium,
            'cholesterol': self.cholesterol,
            'serving_size': self.serving_size,
            'cooking_method': self.cooking_method,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'is_healthy': self.is_healthy,
            'log_date': self.log_date.isoformat() if self.log_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DailyStats(db.Model):
    __tablename__ = 'daily_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Daily aggregated data
    date = db.Column(db.Date, default=date.today, unique=True)
    total_calories_burned = db.Column(db.Integer, default=0)
    total_calories_consumed = db.Column(db.Integer, default=0)
    total_workout_duration = db.Column(db.Float, default=0)  # hours
    total_water_intake = db.Column(db.Float, default=0)  # liters
    avg_heart_rate = db.Column(db.Integer, default=0)
    max_heart_rate = db.Column(db.Integer, default=0)
    workout_count = db.Column(db.Integer, default=0)
    meal_count = db.Column(db.Integer, default=0)
    
    # Calculated metrics
    calorie_balance = db.Column(db.Integer, default=0)  # consumed - burned
    consistency_score = db.Column(db.Float, default=0)  # 0-100
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_consistency_score(self):
        """Calculate consistency score based on workout frequency and nutrition logging"""
        workout_score = min(self.workout_count * 20, 60)  # Max 60 points for workouts
        nutrition_score = min(self.meal_count * 5, 40)  # Max 40 points for nutrition
        self.consistency_score = workout_score + nutrition_score
        return self.consistency_score
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'total_calories_burned': self.total_calories_burned,
            'total_calories_consumed': self.total_calories_consumed,
            'total_workout_duration': self.total_workout_duration,
            'total_water_intake': self.total_water_intake,
            'avg_heart_rate': self.avg_heart_rate,
            'max_heart_rate': self.max_heart_rate,
            'workout_count': self.workout_count,
            'meal_count': self.meal_count,
            'calorie_balance': self.calorie_balance,
            'consistency_score': self.consistency_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    benefit = db.Column(db.Text)
    burns_calories_per_30min = db.Column(db.Integer)
    target_muscle_group = db.Column(db.String(100))
    equipment_needed = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    body_part = db.Column(db.String(50))
    type_of_muscle = db.Column(db.String(50))
    instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'benefit': self.benefit,
            'burns_calories_per_30min': self.burns_calories_per_30min,
            'target_muscle_group': self.target_muscle_group,
            'equipment_needed': self.equipment_needed,
            'difficulty_level': self.difficulty_level,
            'body_part': self.body_part,
            'type_of_muscle': self.type_of_muscle,
            'instructions': self.instructions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }