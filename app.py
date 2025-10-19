"""Main Flask application"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, WorkoutLog, NutritionLog, Meal, Exercise, ExerciseLog, DailyStats
from utils import (calculate_bmi, get_weekly_stats, get_monthly_trends, 
                   generate_insights, calculate_progress_score, update_daily_stats)
from datetime import datetime, timedelta
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== Authentication Routes ====================

@app.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


# ==================== Dashboard Routes ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get weekly stats
    weekly_stats = get_weekly_stats(current_user.id)
    
    # Get insights
    insights_data = generate_insights(current_user)
    
    # Get progress score
    progress_score = calculate_progress_score(current_user)
    
    return render_template('dashboard.html', 
                         user=current_user,
                         weekly_stats=weekly_stats,
                         insights=insights_data,
                         progress_score=progress_score)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        current_user.age = request.form.get('age', type=int)
        current_user.gender = request.form.get('gender')
        current_user.weight = request.form.get('weight', type=float)
        current_user.height = request.form.get('height', type=float)
        current_user.fat_percentage = request.form.get('fat_percentage', type=float)
        current_user.experience_level = request.form.get('experience_level', type=int)
        
        # Calculate BMI
        current_user.calculate_bmi()
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=current_user)


# ==================== Workout Tracking Routes ====================

@app.route('/workout_tracker', methods=['GET', 'POST'])
@login_required
def workout_tracker():
    """Workout tracking page"""
    if request.method == 'POST':
        workout = WorkoutLog(
            user_id=current_user.id,
            workout_type=request.form.get('workout_type'),
            session_duration=request.form.get('session_duration', type=float),
            calories_burned=request.form.get('calories_burned', type=int),
            max_bpm=request.form.get('max_bpm', type=int),
            avg_bpm=request.form.get('avg_bpm', type=int),
            resting_bpm=request.form.get('resting_bpm', type=int),
            notes=request.form.get('notes'),
            date=datetime.utcnow()
        )
        
        db.session.add(workout)
        db.session.commit()
        
        # Update daily stats
        update_daily_stats(current_user.id)
        
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('workout_tracker'))
    
    # Get recent workouts
    recent_workouts = WorkoutLog.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutLog.date.desc()).limit(10).all()
    
    return render_template('workout_tracker.html', workouts=recent_workouts)


@app.route('/nutrition_tracker', methods=['GET', 'POST'])
@login_required
def nutrition_tracker():
    """Nutrition tracking page"""
    if request.method == 'POST':
        today = datetime.utcnow().date()
        
        # Get or create today's nutrition log
        nutrition_log = NutritionLog.query.filter_by(
            user_id=current_user.id, 
            date=today
        ).first()
        
        if not nutrition_log:
            nutrition_log = NutritionLog(
                user_id=current_user.id,
                date=today,
                total_calories=0,
                total_carbs=0,
                total_proteins=0,
                total_fats=0
            )
            db.session.add(nutrition_log)
            db.session.commit()
        
        # Add meal
        meal = Meal(
            nutrition_log_id=nutrition_log.id,
            meal_name=request.form.get('meal_name'),
            meal_type=request.form.get('meal_type'),
            diet_type=request.form.get('diet_type'),
            calories=request.form.get('calories', type=int),
            carbs=request.form.get('carbs', type=int),
            proteins=request.form.get('proteins', type=int),
            fats=request.form.get('fats', type=int),
            sugar=request.form.get('sugar', type=int),
            sodium=request.form.get('sodium', type=int),
            description=request.form.get('description')
        )
        
        db.session.add(meal)
        
        # Update totals
        nutrition_log.total_calories = (nutrition_log.total_calories or 0) + (meal.calories or 0)
        nutrition_log.total_carbs = (nutrition_log.total_carbs or 0) + (meal.carbs or 0)
        nutrition_log.total_proteins = (nutrition_log.total_proteins or 0) + (meal.proteins or 0)
        nutrition_log.total_fats = (nutrition_log.total_fats or 0) + (meal.fats or 0)
        
        # Update water intake if provided
        water_intake = request.form.get('water_intake', type=float)
        if water_intake:
            nutrition_log.water_intake = water_intake
        
        db.session.commit()
        
        # Update daily stats
        update_daily_stats(current_user.id)
        
        flash('Meal logged successfully!', 'success')
        return redirect(url_for('nutrition_tracker'))
    
    # Get today's nutrition log
    today = datetime.utcnow().date()
    today_log = NutritionLog.query.filter_by(
        user_id=current_user.id, 
        date=today
    ).first()
    
    # Get recent meals
    recent_logs = NutritionLog.query.filter_by(user_id=current_user.id)\
        .order_by(NutritionLog.date.desc()).limit(7).all()
    
    return render_template('nutrition_tracker.html', 
                         today_log=today_log,
                         recent_logs=recent_logs)


# ==================== Analytics Routes ====================

@app.route('/analytics')
@login_required
def analytics():
    """Analytics page with charts"""
    # Get monthly trends
    trends = get_monthly_trends(current_user.id)
    
    # Get weekly stats
    weekly_stats = get_weekly_stats(current_user.id)
    
    return render_template('analytics.html', 
                         trends=trends,
                         weekly_stats=weekly_stats,
                         user=current_user)


@app.route('/api/dashboard_data')
@login_required
def api_dashboard_data():
    """API endpoint for dashboard data"""
    weekly_stats = get_weekly_stats(current_user.id)
    insights_data = generate_insights(current_user)
    progress_score = calculate_progress_score(current_user)
    
    return jsonify({
        'weekly_stats': weekly_stats,
        'insights': insights_data,
        'progress_score': progress_score,
        'user': {
            'bmi': current_user.bmi,
            'weight': current_user.weight,
            'height': current_user.height,
            'age': current_user.age
        }
    })


@app.route('/api/workout_history')
@login_required
def api_workout_history():
    """API endpoint for workout history"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == current_user.id,
        WorkoutLog.date >= start_date
    ).order_by(WorkoutLog.date).all()
    
    data = {
        'dates': [w.date.strftime('%Y-%m-%d') for w in workouts],
        'calories': [w.calories_burned for w in workouts],
        'durations': [w.session_duration * 60 for w in workouts],  # Convert to minutes
        'types': [w.workout_type for w in workouts]
    }
    
    return jsonify(data)


# ==================== Reports Routes ====================

@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    return render_template('reports.html')


@app.route('/generate_report/<report_type>')
@login_required
def generate_report(report_type):
    """Generate and download report"""
    if report_type == 'pdf':
        from report_generator import generate_pdf_report
        filename = generate_pdf_report(current_user.id)
        return send_file(filename, as_attachment=True)
    
    elif report_type == 'excel':
        from report_generator import generate_excel_report
        filename = generate_excel_report(current_user.id)
        return send_file(filename, as_attachment=True)
    
    else:
        flash('Invalid report type', 'error')
        return redirect(url_for('reports'))


# ==================== Database Initialization ====================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")


@app.cli.command()
def seed_exercises():
    """Seed exercise database with sample data"""
    sample_exercises = [
        Exercise(name_of_exercise="Push-ups", benefit="Builds chest and triceps strength", 
                burns_calories_per_30min=167, target_muscle_group="Chest", 
                equipment_needed="None", difficulty_level="Beginner", body_part="Chest", 
                type_of_muscle="Upper"),
        Exercise(name_of_exercise="Squats", benefit="Strengthens legs and glutes", 
                burns_calories_per_30min=223, target_muscle_group="Quadriceps", 
                equipment_needed="None", difficulty_level="Beginner", body_part="Legs", 
                type_of_muscle="Lower"),
        Exercise(name_of_exercise="Plank", benefit="Core stability and strength", 
                burns_calories_per_30min=149, target_muscle_group="Core", 
                equipment_needed="None", difficulty_level="Beginner", body_part="Core", 
                type_of_muscle="Core"),
        Exercise(name_of_exercise="Burpees", benefit="Full body conditioning", 
                burns_calories_per_30min=298, target_muscle_group="Full Body", 
                equipment_needed="None", difficulty_level="Advanced", body_part="Full Body", 
                type_of_muscle="Upper"),
        Exercise(name_of_exercise="Deadlift", benefit="Strengthens back and legs", 
                burns_calories_per_30min=266, target_muscle_group="Back", 
                equipment_needed="Barbell", difficulty_level="Intermediate", body_part="Back", 
                type_of_muscle="Lower"),
    ]
    
    for exercise in sample_exercises:
        existing = Exercise.query.filter_by(name_of_exercise=exercise.name_of_exercise).first()
        if not existing:
            db.session.add(exercise)
    
    db.session.commit()
    print("Exercise database seeded!")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
