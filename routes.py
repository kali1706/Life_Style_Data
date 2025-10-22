from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from models import db, User, WorkoutLog, NutritionLog, Meal, Exercise, DailyStats, Report
from utils import AnalyticsCalculator, DataProcessor, ChartDataGenerator, EmailTemplate
from datetime import datetime, date, timedelta
import os
import json

main = Blueprint('main', __name__)

# Authentication Routes
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('main.dashboard')})
    
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('main.dashboard')})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Main Routes
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent data for dashboard
    recent_workouts = WorkoutLog.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutLog.workout_date.desc()).limit(5).all()
    
    recent_nutrition = NutritionLog.query.filter_by(user_id=current_user.id)\
        .order_by(NutritionLog.log_date.desc()).limit(7).all()
    
    # Calculate weekly summary
    week_start = date.today() - timedelta(days=7)
    weekly_workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == current_user.id,
        WorkoutLog.workout_date >= week_start
    ).all()
    
    weekly_nutrition = NutritionLog.query.filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.log_date >= week_start
    ).all()
    
    # Calculate metrics
    total_calories_burned = sum(w.calories_burned or 0 for w in weekly_workouts)
    total_calories_consumed = sum(n.calories or 0 for n in weekly_nutrition)
    avg_session_duration = sum(w.session_duration or 0 for w in weekly_workouts) / max(len(weekly_workouts), 1)
    
    # Get chart data
    bmi_trend = ChartDataGenerator.generate_bmi_trend_data(current_user.id)
    calorie_balance = ChartDataGenerator.generate_calorie_balance_data(current_user.id)
    
    # Calculate macro averages
    if weekly_nutrition:
        total_carbs = sum(n.carbs or 0 for n in weekly_nutrition)
        total_proteins = sum(n.proteins or 0 for n in weekly_nutrition)
        total_fats = sum(n.fats or 0 for n in weekly_nutrition)
        total_macros = total_carbs + total_proteins + total_fats
        
        if total_macros > 0:
            macro_avg = {
                'carbs': round((total_carbs / total_macros) * 100, 1),
                'proteins': round((total_proteins / total_macros) * 100, 1),
                'fats': round((total_fats / total_macros) * 100, 1)
            }
        else:
            macro_avg = {'carbs': 0, 'proteins': 0, 'fats': 0}
    else:
        macro_avg = {'carbs': 0, 'proteins': 0, 'fats': 0}
    
    # Generate insights
    user_data = {
        'consistency_score': min(100, len(weekly_workouts) * 20),  # Simple calculation
        'calorie_balance': total_calories_consumed - total_calories_burned,
        'macro_avg': macro_avg,
        'water_intake': sum(n.water_intake or 0 for n in weekly_nutrition) / max(len(weekly_nutrition), 1)
    }
    
    insights = DataProcessor.get_insights(user_data)
    
    dashboard_data = {
        'total_workouts': len(weekly_workouts),
        'total_calories_burned': total_calories_burned,
        'avg_session_duration': round(avg_session_duration, 1),
        'total_meals_logged': len(weekly_nutrition),
        'avg_daily_intake': round(total_calories_consumed / max(len(weekly_nutrition), 1), 0),
        'macro_avg': macro_avg,
        'bmi': current_user.bmi or 0,
        'body_fat': current_user.fat_percentage or 0,
        'consistency_score': user_data['consistency_score'],
        'insights': insights,
        'bmi_trend': bmi_trend,
        'calorie_balance': calorie_balance
    }
    
    return render_template('dashboard.html', data=dashboard_data)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form

        # Update user profile
        current_user.age = int(data.get('age', 0)) or None
        current_user.gender = data.get('gender')
        current_user.weight = float(data.get('weight', 0)) or None
        current_user.height = float(data.get('height', 0)) or None
        current_user.experience_level = int(data.get('experience_level', 0)) or None
        current_user.fat_percentage = float(data.get('fat_percentage', 0)) or None

        # Update email preferences
        current_user.daily_reports = data.get('daily_reports', False) in ['true', True]
        current_user.weekly_reports = data.get('weekly_reports', True) in ['true', True]
        current_user.monthly_reports = data.get('monthly_reports', True) in ['true', True]

        # Calculate BMI
        if current_user.weight and current_user.height:
            current_user.bmi = AnalyticsCalculator.calculate_bmi(
                current_user.weight, current_user.height
            )

        db.session.commit()

        if request.is_json:
            return jsonify({'success': True, 'bmi': current_user.bmi})
        else:
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main.profile'))

    return render_template('user_profile.html', user=current_user)

@main.route('/workout_tracker')
@login_required
def workout_tracker():
    # Get recent workouts
    recent_workouts = WorkoutLog.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutLog.workout_date.desc()).limit(10).all()
    
    # Get available exercises
    exercises = Exercise.query.all()
    
    return render_template('workout_tracker.html', 
                         workouts=recent_workouts, 
                         exercises=exercises)

@main.route('/log_workout', methods=['POST'])
@login_required
def log_workout():
    data = request.get_json()
    
    # Create workout log
    workout = WorkoutLog(
        user_id=current_user.id,
        workout_type=data.get('workout_type'),
        session_duration=float(data.get('session_duration', 0)),
        calories_burned=int(data.get('calories_burned', 0)),
        max_bpm=int(data.get('max_bpm', 0)) or None,
        avg_bpm=int(data.get('avg_bpm', 0)) or None,
        resting_bpm=int(data.get('resting_bpm', 0)) or None,
        workout_frequency=int(data.get('workout_frequency', 0)) or None,
        workout_date=datetime.strptime(data.get('workout_date', date.today().isoformat()), '%Y-%m-%d').date()
    )
    
    db.session.add(workout)
    db.session.flush()  # Get the workout ID
    
    # Add exercises if provided
    exercises_data = data.get('exercises', [])
    for exercise_data in exercises_data:
        exercise = ExerciseLog(
            workout_id=workout.id,
            name_of_exercise=exercise_data.get('name'),
            sets=int(exercise_data.get('sets', 0)) or None,
            reps=int(exercise_data.get('reps', 0)) or None,
            benefit=exercise_data.get('benefit'),
            burns_calories_per_30min=int(exercise_data.get('burns_calories', 0)) or None,
            target_muscle_group=exercise_data.get('target_muscle_group'),
            equipment_needed=exercise_data.get('equipment_needed'),
            difficulty_level=exercise_data.get('difficulty_level'),
            body_part=exercise_data.get('body_part'),
            type_of_muscle=exercise_data.get('type_of_muscle')
        )
        db.session.add(exercise)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Workout logged successfully!'})

@main.route('/nutrition_tracker')
@login_required
def nutrition_tracker():
    # Get recent nutrition logs
    recent_nutrition = NutritionLog.query.filter_by(user_id=current_user.id)\
        .order_by(NutritionLog.log_date.desc()).limit(10).all()
    
    # Get recent meals
    recent_meals = Meal.query.filter_by(user_id=current_user.id)\
        .order_by(Meal.meal_date.desc()).limit(20).all()
    
    return render_template('nutrition_tracker.html', 
                         nutrition_logs=recent_nutrition,
                         meals=recent_meals)

@main.route('/log_nutrition', methods=['POST'])
@login_required
def log_nutrition():
    data = request.get_json()
    
    # Create nutrition log
    nutrition = NutritionLog(
        user_id=current_user.id,
        daily_meals_frequency=int(data.get('daily_meals_frequency', 0)) or None,
        carbs=int(data.get('carbs', 0)) or None,
        proteins=int(data.get('proteins', 0)) or None,
        fats=int(data.get('fats', 0)) or None,
        calories=int(data.get('calories', 0)) or None,
        water_intake=float(data.get('water_intake', 0)) or None,
        log_date=datetime.strptime(data.get('log_date', date.today().isoformat()), '%Y-%m-%d').date()
    )
    
    db.session.add(nutrition)
    db.session.flush()  # Get the nutrition log ID
    
    # Add meals if provided
    meals_data = data.get('meals', [])
    for meal_data in meals_data:
        meal = Meal(
            user_id=current_user.id,
            nutrition_log_id=nutrition.id,
            meal_name=meal_data.get('meal_name'),
            meal_type=meal_data.get('meal_type'),
            diet_type=meal_data.get('diet_type'),
            sugar=int(meal_data.get('sugar', 0)) or None,
            sodium=int(meal_data.get('sodium', 0)) or None,
            cholesterol=int(meal_data.get('cholesterol', 0)) or None,
            serving_size=int(meal_data.get('serving_size', 0)) or None,
            calories=int(meal_data.get('calories', 0)) or None,
            carbs=int(meal_data.get('carbs', 0)) or None,
            proteins=int(meal_data.get('proteins', 0)) or None,
            fats=int(meal_data.get('fats', 0)) or None,
            cooking_method=meal_data.get('cooking_method'),
            prep_time=int(meal_data.get('prep_time', 0)) or None,
            cook_time=int(meal_data.get('cook_time', 0)) or None,
            is_healthy=meal_data.get('is_healthy', True),
            meal_date=nutrition.log_date
        )
        db.session.add(meal)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Nutrition logged successfully!'})

@main.route('/analytics')
@login_required
def analytics():
    # Get chart data
    bmi_trend = ChartDataGenerator.generate_bmi_trend_data(current_user.id, 30)
    calorie_balance = ChartDataGenerator.generate_calorie_balance_data(current_user.id, 14)
    
    # Get workout type distribution
    workout_types = db.session.query(WorkoutLog.workout_type, 
                                   db.func.count(WorkoutLog.id))\
        .filter(WorkoutLog.user_id == current_user.id)\
        .group_by(WorkoutLog.workout_type).all()
    
    workout_distribution = {
        'labels': [wt[0] or 'Unknown' for wt in workout_types],
        'data': [wt[1] for wt in workout_types],
        'title': 'Workout Type Distribution'
    }
    
    # Get heart rate trends
    heart_rate_data = db.session.query(
        WorkoutLog.workout_date,
        WorkoutLog.avg_bpm,
        WorkoutLog.max_bpm
    ).filter(
        WorkoutLog.user_id == current_user.id,
        WorkoutLog.avg_bpm.isnot(None)
    ).order_by(WorkoutLog.workout_date.desc()).limit(14).all()
    
    hr_trend = {
        'labels': [str(hr[0]) for hr in heart_rate_data],
        'datasets': [
            {
                'label': 'Average BPM',
                'data': [hr[1] for hr in heart_rate_data],
                'backgroundColor': 'rgba(54, 162, 235, 0.6)'
            },
            {
                'label': 'Max BPM',
                'data': [hr[2] for hr in heart_rate_data],
                'backgroundColor': 'rgba(255, 99, 132, 0.6)'
            }
        ],
        'title': 'Heart Rate Trends (Last 14 Days)'
    }
    
    return render_template('analytics.html',
                         bmi_trend=bmi_trend,
                         calorie_balance=calorie_balance,
                         workout_distribution=workout_distribution,
                         hr_trend=hr_trend)

@main.route('/advanced-analytics')
@login_required
def advanced_analytics():
    """Advanced analytics dashboard with interactive tabs and modern UI"""
    return render_template('advanced_analytics.html')

@main.route('/reports')
@login_required
def reports():
    # Get user's reports
    user_reports = Report.query.filter_by(user_id=current_user.id)\
        .order_by(Report.created_at.desc()).limit(10).all()
    
    return render_template('reports.html', reports=user_reports)

@main.route('/generate_report', methods=['POST'])
@login_required
def generate_report():
    data = request.get_json()
    report_type = data.get('type', 'weekly')  # daily, weekly, monthly
    report_format = data.get('format', 'pdf')  # pdf, excel
    email_recipients = data.get('email_recipients', [])
    
    # Calculate date range
    end_date = date.today()
    if report_type == 'daily':
        start_date = end_date
    elif report_type == 'weekly':
        start_date = end_date - timedelta(days=7)
    else:  # monthly
        start_date = end_date - timedelta(days=30)
    
    # Generate report (placeholder - would implement actual report generation)
    report = Report(
        user_id=current_user.id,
        report_type=report_type,
        report_format=report_format,
        file_path=f"reports/{current_user.id}_{report_type}_{end_date}.{report_format}",
        start_date=start_date,
        end_date=end_date,
        email_recipients=json.dumps(email_recipients)
    )
    
    db.session.add(report)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{report_type.title()} {report_format.upper()} report generated successfully!',
        'report_id': report.id
    })

@main.route('/api/dashboard_data')
@login_required
def api_dashboard_data():
    """API endpoint for dashboard data"""
    # Get recent data
    recent_workouts = WorkoutLog.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutLog.workout_date.desc()).limit(7).all()
    
    recent_nutrition = NutritionLog.query.filter_by(user_id=current_user.id)\
        .order_by(NutritionLog.log_date.desc()).limit(7).all()
    
    # Calculate metrics
    total_calories_burned = sum(w.calories_burned or 0 for w in recent_workouts)
    total_calories_consumed = sum(n.calories or 0 for n in recent_nutrition)
    
    return jsonify({
        'total_workouts': len(recent_workouts),
        'total_calories_burned': total_calories_burned,
        'total_calories_consumed': total_calories_consumed,
        'calorie_balance': total_calories_consumed - total_calories_burned,
        'bmi': current_user.bmi,
        'bmi_category': AnalyticsCalculator.get_bmi_category(current_user.bmi or 0)
    })

@main.route('/api/chart_data/<chart_type>')
@login_required
def api_chart_data(chart_type):
    """API endpoint for chart data"""
    if chart_type == 'bmi_trend':
        return jsonify(ChartDataGenerator.generate_bmi_trend_data(current_user.id))
    elif chart_type == 'calorie_balance':
        return jsonify(ChartDataGenerator.generate_calorie_balance_data(current_user.id))
    elif chart_type == 'macro_breakdown':
        # Get recent nutrition data for macro breakdown
        recent_nutrition = NutritionLog.query.filter_by(user_id=current_user.id)\
            .order_by(NutritionLog.log_date.desc()).limit(7).all()
        
        if recent_nutrition:
            total_carbs = sum(n.carbs or 0 for n in recent_nutrition)
            total_proteins = sum(n.proteins or 0 for n in recent_nutrition)
            total_fats = sum(n.fats or 0 for n in recent_nutrition)
            
            return jsonify({
                'labels': ['Carbs', 'Proteins', 'Fats'],
                'data': [total_carbs, total_proteins, total_fats],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 205, 86, 0.6)'
                ],
                'title': 'Macro Nutrient Distribution (Last 7 Days)'
            })
    
    return jsonify({'error': 'Invalid chart type'}), 400