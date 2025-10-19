from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pandas as pd
import json
import os
from config import Config
from models import db, User, WorkoutLog, NutritionLog, Meal, Exercise, DailyStats
from utils import calculate_bmi, calculate_calories_needed, get_macro_percentages, calculate_progress_score
from report_generator import generate_pdf_report, generate_excel_report, send_email_report

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Email already registered'})
            flash('Email already registered')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            age=int(data['age']),
            gender=data['gender'],
            weight=float(data['weight']),
            height=float(data['height']),
            experience_level=int(data['experience_level'])
        )
        user.bmi = calculate_bmi(user.weight, user.height)
        
        db.session.add(user)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Registration successful'})
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            if request.is_json:
                return jsonify({'success': True, 'message': 'Login successful'})
            return redirect(url_for('dashboard'))
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
        flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get recent data for dashboard
    recent_workouts = WorkoutLog.query.filter_by(user_id=current_user.id).order_by(WorkoutLog.date.desc()).limit(5).all()
    recent_nutrition = NutritionLog.query.filter_by(user_id=current_user.id).order_by(NutritionLog.date.desc()).limit(5).all()
    
    # Calculate weekly stats
    week_start = datetime.now() - timedelta(days=7)
    weekly_workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == current_user.id,
        WorkoutLog.date >= week_start
    ).all()
    
    weekly_nutrition = NutritionLog.query.filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.date >= week_start
    ).all()
    
    stats = {
        'total_workouts': len(weekly_workouts),
        'total_calories_burned': sum([w.calories_burned for w in weekly_workouts]),
        'avg_session_duration': sum([w.session_duration for w in weekly_workouts]) / len(weekly_workouts) if weekly_workouts else 0,
        'total_meals_logged': len(weekly_nutrition),
        'avg_daily_intake': sum([n.calories for n in weekly_nutrition]) / 7 if weekly_nutrition else 0,
        'current_bmi': current_user.bmi,
        'body_fat': current_user.fat_percentage or 0,
        'progress_score': calculate_progress_score(current_user.id)
    }
    
    return render_template('dashboard.html', stats=stats, recent_workouts=recent_workouts, recent_nutrition=recent_nutrition)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        current_user.age = int(data['age'])
        current_user.weight = float(data['weight'])
        current_user.height = float(data['height'])
        current_user.experience_level = int(data['experience_level'])
        current_user.fat_percentage = float(data.get('fat_percentage', 0))
        current_user.bmi = calculate_bmi(current_user.weight, current_user.height)
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=current_user)

@app.route('/workout_tracker', methods=['GET', 'POST'])
@login_required
def workout_tracker():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        workout = WorkoutLog(
            user_id=current_user.id,
            workout_type=data['workout_type'],
            session_duration=float(data['session_duration']),
            calories_burned=int(data['calories_burned']),
            max_bpm=int(data.get('max_bpm', 0)),
            avg_bpm=int(data.get('avg_bpm', 0)),
            date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.now()
        )
        
        db.session.add(workout)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Workout logged successfully'})
        flash('Workout logged successfully!')
        return redirect(url_for('workout_tracker'))
    
    workouts = WorkoutLog.query.filter_by(user_id=current_user.id).order_by(WorkoutLog.date.desc()).all()
    exercises = Exercise.query.all()
    return render_template('workout_tracker.html', workouts=workouts, exercises=exercises)

@app.route('/nutrition_tracker', methods=['GET', 'POST'])
@login_required
def nutrition_tracker():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        nutrition = NutritionLog(
            user_id=current_user.id,
            meal_name=data['meal_name'],
            calories=int(data['calories']),
            carbs=int(data['carbs']),
            proteins=int(data['proteins']),
            fats=int(data['fats']),
            water_intake=float(data.get('water_intake', 0)),
            date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.now()
        )
        
        db.session.add(nutrition)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Nutrition logged successfully'})
        flash('Nutrition logged successfully!')
        return redirect(url_for('nutrition_tracker'))
    
    nutrition_logs = NutritionLog.query.filter_by(user_id=current_user.id).order_by(NutritionLog.date.desc()).all()
    meals = Meal.query.all()
    return render_template('nutrition_tracker.html', nutrition_logs=nutrition_logs, meals=meals)

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/api/analytics_data')
@login_required
def analytics_data():
    # Get data for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == current_user.id,
        WorkoutLog.date >= thirty_days_ago
    ).all()
    
    nutrition = NutritionLog.query.filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.date >= thirty_days_ago
    ).all()
    
    # Prepare data for charts
    workout_data = []
    nutrition_data = []
    
    for workout in workouts:
        workout_data.append({
            'date': workout.date.strftime('%Y-%m-%d'),
            'calories_burned': workout.calories_burned,
            'duration': workout.session_duration,
            'type': workout.workout_type,
            'avg_bpm': workout.avg_bpm
        })
    
    for n in nutrition:
        nutrition_data.append({
            'date': n.date.strftime('%Y-%m-%d'),
            'calories': n.calories,
            'carbs': n.carbs,
            'proteins': n.proteins,
            'fats': n.fats,
            'meal_name': n.meal_name
        })
    
    # Calculate macro percentages
    total_carbs = sum([n.carbs for n in nutrition])
    total_proteins = sum([n.proteins for n in nutrition])
    total_fats = sum([n.fats for n in nutrition])
    
    macro_percentages = get_macro_percentages(total_carbs, total_proteins, total_fats)
    
    return jsonify({
        'workouts': workout_data,
        'nutrition': nutrition_data,
        'macro_percentages': macro_percentages,
        'total_workouts': len(workouts),
        'total_calories_burned': sum([w.calories_burned for w in workouts]),
        'avg_calories_intake': sum([n.calories for n in nutrition]) / len(nutrition) if nutrition else 0
    })

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/generate_pdf_report')
@login_required
def generate_pdf():
    try:
        filename = generate_pdf_report(current_user.id)
        return send_file(filename, as_attachment=True, download_name=f'lifestyle_report_{current_user.username}.pdf')
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}')
        return redirect(url_for('reports'))

@app.route('/generate_excel_report')
@login_required
def generate_excel():
    try:
        filename = generate_excel_report(current_user.id)
        return send_file(filename, as_attachment=True, download_name=f'lifestyle_data_{current_user.username}.xlsx')
    except Exception as e:
        flash(f'Error generating Excel: {str(e)}')
        return redirect(url_for('reports'))

@app.route('/send_email_report', methods=['POST'])
@login_required
def send_email():
    data = request.get_json() if request.is_json else request.form
    email = data['email']
    
    try:
        send_email_report(current_user.id, email)
        if request.is_json:
            return jsonify({'success': True, 'message': 'Email sent successfully'})
        flash('Email sent successfully!')
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error sending email: {str(e)}'})
        flash(f'Error sending email: {str(e)}')
    
    return redirect(url_for('reports'))

if __name__ == '__main__':
    app.run(debug=True)