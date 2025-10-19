from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile data
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in meters
    bmi = db.Column(db.Float)
    experience_level = db.Column(db.Integer)  # 1=Beginner, 2=Intermediate, 3=Advanced
    fat_percentage = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workouts = db.relationship('WorkoutLog', backref='user', lazy=True, cascade='all, delete-orphan')
    nutrition_logs = db.relationship('NutritionLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmi(self):
        """Calculate BMI from weight and height"""
        if self.weight and self.height and self.height > 0:
            self.bmi = round(self.weight / (self.height ** 2), 2)
        return self.bmi
    
    def get_bmi_category(self):
        """Get BMI category"""
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
    
    def __repr__(self):
        return f'<User {self.username}>'


class WorkoutLog(db.Model):
    """Workout log model"""
    __tablename__ = 'workout_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Workout details
    workout_type = db.Column(db.String(50))  # Strength, HIIT, Cardio, Yoga, etc.
    session_duration = db.Column(db.Float)  # in hours
    calories_burned = db.Column(db.Integer)
    
    # Heart rate data
    max_bpm = db.Column(db.Integer)
    avg_bpm = db.Column(db.Integer)
    resting_bpm = db.Column(db.Integer)
    
    # Additional data
    workout_frequency = db.Column(db.Integer)  # days per week
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Exercise details
    exercises = db.relationship('ExerciseLog', backref='workout', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<WorkoutLog {self.workout_type} on {self.date}>'


class ExerciseLog(db.Model):
    """Exercise log model - links to workout"""
    __tablename__ = 'exercise_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_logs.id'), nullable=False)
    
    # Exercise details
    name_of_exercise = db.Column(db.String(100))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight_used = db.Column(db.Float)  # in kg
    
    # Exercise metadata
    target_muscle_group = db.Column(db.String(50))
    body_part = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))
    equipment_needed = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<ExerciseLog {self.name_of_exercise}>'


class Exercise(db.Model):
    """Master exercise database"""
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name_of_exercise = db.Column(db.String(100), unique=True, nullable=False)
    
    # Exercise properties
    benefit = db.Column(db.Text)
    burns_calories_per_30min = db.Column(db.Integer)
    target_muscle_group = db.Column(db.String(50))
    equipment_needed = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    body_part = db.Column(db.String(50))
    type_of_muscle = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Exercise {self.name_of_exercise}>'


class NutritionLog(db.Model):
    """Nutrition log model"""
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Daily nutrition totals
    date = db.Column(db.Date, default=datetime.utcnow)
    daily_meals_frequency = db.Column(db.Integer)
    total_calories = db.Column(db.Integer)
    total_carbs = db.Column(db.Integer)  # in grams
    total_proteins = db.Column(db.Integer)  # in grams
    total_fats = db.Column(db.Integer)  # in grams
    water_intake = db.Column(db.Float)  # in liters
    
    # Meals
    meals = db.relationship('Meal', backref='nutrition_log', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NutritionLog {self.date}>'


class Meal(db.Model):
    """Meal model"""
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    nutrition_log_id = db.Column(db.Integer, db.ForeignKey('nutrition_logs.id'), nullable=False)
    
    # Meal details
    meal_name = db.Column(db.String(50))  # Breakfast, Lunch, Dinner, Snack
    meal_type = db.Column(db.String(50))  # Main, Snack, Beverage
    diet_type = db.Column(db.String(50))  # Keto, Vegan, Balanced, etc.
    
    # Nutritional content
    calories = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    proteins = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    sugar = db.Column(db.Integer)
    sodium = db.Column(db.Integer)  # in mg
    cholesterol = db.Column(db.Integer)  # in mg
    
    # Preparation details
    serving_size = db.Column(db.Integer)  # in grams
    cooking_method = db.Column(db.String(50))  # Boiled, Fried, Grilled, Baked
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    is_healthy = db.Column(db.Boolean, default=True)
    
    # Additional info
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Meal {self.meal_name}>'


class DailyStats(db.Model):
    """Daily aggregated statistics"""
    __tablename__ = 'daily_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, unique=True, nullable=False)
    
    # Workout stats
    total_workouts = db.Column(db.Integer, default=0)
    total_workout_duration = db.Column(db.Float, default=0)
    total_calories_burned = db.Column(db.Integer, default=0)
    
    # Nutrition stats
    total_calories_consumed = db.Column(db.Integer, default=0)
    total_meals = db.Column(db.Integer, default=0)
    
    # Balance
    calorie_balance = db.Column(db.Integer)  # consumed - burned
    
    # Body metrics
    weight = db.Column(db.Float)
    bmi = db.Column(db.Float)
    fat_percentage = db.Column(db.Float)
    
    def __repr__(self):
        return f'<DailyStats {self.date}>'
