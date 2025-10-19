from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Male, Female, Other
    weight = db.Column(db.Float, nullable=False)  # in kg
    height = db.Column(db.Float, nullable=False)  # in meters
    bmi = db.Column(db.Float)
    experience_level = db.Column(db.Integer, nullable=False)  # 1=Beginner, 2=Intermediate, 3=Advanced
    fat_percentage = db.Column(db.Float)
    resting_bpm = db.Column(db.Integer, default=70)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workout_logs = db.relationship('WorkoutLog', backref='user', lazy=True, cascade='all, delete-orphan')
    nutrition_logs = db.relationship('NutritionLog', backref='user', lazy=True, cascade='all, delete-orphan')
    daily_stats = db.relationship('DailyStats', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_bmi_category(self):
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 25:
            return 'Normal'
        elif 25 <= self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    def get_experience_level_text(self):
        levels = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}
        return levels.get(self.experience_level, 'Unknown')

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Workout details
    workout_type = db.Column(db.String(50), nullable=False)  # Strength, HIIT, Cardio, Yoga, etc.
    session_duration = db.Column(db.Float, nullable=False)  # in hours
    calories_burned = db.Column(db.Integer, nullable=False)
    
    # Heart rate data
    max_bpm = db.Column(db.Integer)
    avg_bpm = db.Column(db.Integer)
    
    # Additional metrics
    workout_frequency = db.Column(db.Integer, default=1)  # sessions per week
    intensity_level = db.Column(db.String(20))  # Low, Moderate, High, Very High
    
    # Timestamp
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WorkoutLog {self.workout_type} - {self.date}>'
    
    def get_heart_rate_zone(self):
        if not self.avg_bpm:
            return 'Unknown'
        
        # Estimate max HR as 220 - age
        user_max_hr = 220 - self.user.age
        hr_percentage = (self.avg_bpm / user_max_hr) * 100
        
        if hr_percentage < 60:
            return 'Recovery Zone (50-60%)'
        elif hr_percentage < 70:
            return 'Aerobic Zone (60-70%)'
        elif hr_percentage < 85:
            return 'Threshold Zone (70-85%)'
        else:
            return 'Maximum Zone (85-100%)'

class NutritionLog(db.Model):
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Meal information
    meal_name = db.Column(db.String(50), nullable=False)  # Breakfast, Lunch, Dinner, Snack
    meal_type = db.Column(db.String(20))  # Main, Snack, Beverage
    diet_type = db.Column(db.String(20))  # Keto, Vegan, Balanced, etc.
    
    # Nutritional values
    calories = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)  # in grams
    proteins = db.Column(db.Integer, nullable=False)  # in grams
    fats = db.Column(db.Integer, nullable=False)  # in grams
    sugar = db.Column(db.Integer, default=0)  # in grams
    sodium = db.Column(db.Integer, default=0)  # in mg
    cholesterol = db.Column(db.Integer, default=0)  # in mg
    
    # Additional info
    serving_size = db.Column(db.Integer)  # in grams
    water_intake = db.Column(db.Float, default=0)  # in liters
    daily_meals_frequency = db.Column(db.Integer, default=3)
    is_healthy = db.Column(db.Boolean, default=True)
    
    # Timestamp
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NutritionLog {self.meal_name} - {self.date}>'
    
    def get_macro_percentages(self):
        total_calories = self.calories
        if total_calories == 0:
            return {'carbs': 0, 'proteins': 0, 'fats': 0}
        
        carb_calories = self.carbs * 4
        protein_calories = self.proteins * 4
        fat_calories = self.fats * 9
        
        return {
            'carbs': round((carb_calories / total_calories) * 100, 1),
            'proteins': round((protein_calories / total_calories) * 100, 1),
            'fats': round((fat_calories / total_calories) * 100, 1)
        }

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # Main, Snack, Beverage
    diet_type = db.Column(db.String(20))  # Keto, Vegan, Balanced, etc.
    
    # Nutritional information per 100g
    calories_per_100g = db.Column(db.Integer, nullable=False)
    carbs_per_100g = db.Column(db.Integer, nullable=False)
    proteins_per_100g = db.Column(db.Integer, nullable=False)
    fats_per_100g = db.Column(db.Integer, nullable=False)
    sugar_per_100g = db.Column(db.Integer, default=0)
    sodium_per_100g = db.Column(db.Integer, default=0)
    cholesterol_per_100g = db.Column(db.Integer, default=0)
    
    # Preparation details
    cooking_method = db.Column(db.String(50))  # Boiled, Fried, Grilled, Baked, Raw
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    is_healthy = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Meal {self.name}>'

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Exercise details
    target_muscle_group = db.Column(db.String(50), nullable=False)  # Chest, Back, Legs, etc.
    body_part = db.Column(db.String(50))  # Arms, Legs, Chest, Back, Core
    type_of_muscle = db.Column(db.String(30))  # Upper, Lower, Core, Grip Strength
    difficulty_level = db.Column(db.String(20), nullable=False)  # Beginner, Intermediate, Advanced
    
    # Equipment and setup
    equipment_needed = db.Column(db.String(100))  # Dumbbells, Barbell, Bodyweight, etc.
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    
    # Benefits and calories
    benefit = db.Column(db.Text)
    burns_calories_per_30min = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Exercise {self.name}>'

class DailyStats(db.Model):
    __tablename__ = 'daily_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Daily aggregated data
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    total_calories_consumed = db.Column(db.Integer, default=0)
    total_calories_burned = db.Column(db.Integer, default=0)
    total_water_intake = db.Column(db.Float, default=0)  # in liters
    
    # Macro totals
    total_carbs = db.Column(db.Integer, default=0)
    total_proteins = db.Column(db.Integer, default=0)
    total_fats = db.Column(db.Integer, default=0)
    
    # Activity metrics
    total_workout_duration = db.Column(db.Float, default=0)  # in hours
    workout_count = db.Column(db.Integer, default=0)
    meal_count = db.Column(db.Integer, default=0)
    
    # Health metrics
    weight_recorded = db.Column(db.Float)  # if user updates weight
    body_fat_recorded = db.Column(db.Float)  # if user updates body fat
    resting_bpm_recorded = db.Column(db.Integer)  # if user records resting HR
    
    # Calculated metrics
    caloric_balance = db.Column(db.Integer)  # consumed - burned
    bmi_recorded = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DailyStats {self.date} - User {self.user_id}>'
    
    def get_caloric_balance_status(self):
        if self.caloric_balance is None:
            return 'Unknown'
        elif self.caloric_balance > 500:
            return 'High Surplus'
        elif self.caloric_balance > 0:
            return 'Surplus'
        elif self.caloric_balance > -500:
            return 'Deficit'
        else:
            return 'High Deficit'