from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile Data
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))  # Male, Female, Other
    weight = db.Column(db.Float)  # kg
    height = db.Column(db.Float)  # meters
    bmi = db.Column(db.Float)
    experience_level = db.Column(db.Integer)  # 1=Beginner, 2=Intermediate, 3=Advanced
    fat_percentage = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Email preferences
    daily_reports = db.Column(db.Boolean, default=False)
    weekly_reports = db.Column(db.Boolean, default=True)
    monthly_reports = db.Column(db.Boolean, default=True)

    # Relationships
    workouts = db.relationship('WorkoutLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    nutrition_logs = db.relationship('NutritionLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    meals = db.relationship('Meal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    daily_stats = db.relationship('DailyStats', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmi(self):
        if self.weight and self.height:
            self.bmi = round(self.weight / (self.height ** 2), 2)
            return self.bmi
        return None
    
    def get_bmi_category(self):
        if not self.bmi:
            return "Unknown"
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def __repr__(self):
        return f'<User {self.username}>'

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Workout Data
    workout_type = db.Column(db.String(50))  # Strength, HIIT, Cardio, etc.
    session_duration = db.Column(db.Float)  # hours
    calories_burned = db.Column(db.Integer)
    max_bpm = db.Column(db.Integer)
    avg_bpm = db.Column(db.Integer)
    resting_bpm = db.Column(db.Integer)
    workout_frequency = db.Column(db.Integer)  # days per week
    
    # Timestamps
    workout_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    exercises = db.relationship('ExerciseLog', backref='workout', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<WorkoutLog {self.workout_type} - {self.workout_date}>'

class ExerciseLog(db.Model):
    __tablename__ = 'exercise_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_logs.id'), nullable=False)
    
    # Exercise Data
    name_of_exercise = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    benefit = db.Column(db.Text)
    burns_calories_per_30min = db.Column(db.Integer)
    target_muscle_group = db.Column(db.String(50))
    equipment_needed = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    body_part = db.Column(db.String(30))  # Arms, Legs, Chest, Back, Core
    type_of_muscle = db.Column(db.String(30))  # Upper, Lower, Core, Grip Strength
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExerciseLog {self.name_of_exercise}>'

class NutritionLog(db.Model):
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Daily Nutrition Data
    daily_meals_frequency = db.Column(db.Integer)  # meals per day
    carbs = db.Column(db.Integer)  # grams
    proteins = db.Column(db.Integer)  # grams
    fats = db.Column(db.Integer)  # grams
    calories = db.Column(db.Integer)
    water_intake = db.Column(db.Float)  # liters
    
    # Timestamps
    log_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    meals = db.relationship('Meal', backref='nutrition_log', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NutritionLog {self.log_date}>'

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nutrition_log_id = db.Column(db.Integer, db.ForeignKey('nutrition_logs.id'))
    
    # Meal Data
    meal_name = db.Column(db.String(50))  # Breakfast, Lunch, Dinner, Snack
    meal_type = db.Column(db.String(30))  # Main, Snack, Beverage
    diet_type = db.Column(db.String(30))  # Keto, Vegan, Balanced, etc.
    
    # Nutritional Content
    sugar = db.Column(db.Integer)  # grams
    sodium = db.Column(db.Integer)  # mg
    cholesterol = db.Column(db.Integer)  # mg
    serving_size = db.Column(db.Integer)  # grams
    calories = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    proteins = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    
    # Preparation Details
    cooking_method = db.Column(db.String(30))  # Boiled, Fried, Grilled, Baked
    prep_time = db.Column(db.Integer)  # minutes
    cook_time = db.Column(db.Integer)  # minutes
    is_healthy = db.Column(db.Boolean, default=True)
    
    # Timestamps
    meal_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Meal {self.meal_name} - {self.meal_date}>'

class DailyStats(db.Model):
    __tablename__ = 'daily_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Daily Summary
    date = db.Column(db.Date, default=date.today, unique=True)
    total_calories_burned = db.Column(db.Integer, default=0)
    total_calories_consumed = db.Column(db.Integer, default=0)
    total_workout_duration = db.Column(db.Float, default=0)  # hours
    total_water_intake = db.Column(db.Float, default=0)  # liters
    avg_heart_rate = db.Column(db.Integer)
    consistency_score = db.Column(db.Integer, default=0)  # 0-100
    
    # Calculated Metrics
    caloric_balance = db.Column(db.Integer)  # consumed - burned
    macro_carbs_percent = db.Column(db.Float)
    macro_proteins_percent = db.Column(db.Float)
    macro_fats_percent = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DailyStats {self.date}>'

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    benefit = db.Column(db.Text)
    burns_calories_per_30min = db.Column(db.Integer)
    target_muscle_group = db.Column(db.String(50))
    equipment_needed = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    body_part = db.Column(db.String(30))
    type_of_muscle = db.Column(db.String(30))
    instructions = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Exercise {self.name}>'

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Report Details
    report_type = db.Column(db.String(20))  # daily, weekly, monthly
    report_format = db.Column(db.String(10))  # pdf, excel
    file_path = db.Column(db.String(255))
    email_sent = db.Column(db.Boolean, default=False)
    email_recipients = db.Column(db.Text)  # JSON list of emails
    
    # Date Range
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Report {self.report_type} - {self.created_at}>'