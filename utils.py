from datetime import datetime, timedelta
from models import db, User, WorkoutLog, NutritionLog, DailyStats
import math

def calculate_bmi(weight_kg, height_m):
    """Calculate BMI from weight (kg) and height (m)"""
    if height_m <= 0:
        return 0
    return round(weight_kg / (height_m ** 2), 2)

def get_bmi_category(bmi):
    """Get BMI category based on BMI value"""
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def calculate_calories_needed(user):
    """Calculate daily calorie needs using Mifflin-St Jeor Equation"""
    # Base Metabolic Rate (BMR)
    if user.gender.lower() == 'male':
        bmr = 10 * user.weight + 6.25 * (user.height * 100) - 5 * user.age + 5
    else:
        bmr = 10 * user.weight + 6.25 * (user.height * 100) - 5 * user.age - 161
    
    # Activity factor based on experience level
    activity_factors = {
        1: 1.2,    # Beginner - Sedentary
        2: 1.55,   # Intermediate - Moderately active
        3: 1.725   # Advanced - Very active
    }
    
    activity_factor = activity_factors.get(user.experience_level, 1.2)
    daily_calories = bmr * activity_factor
    
    return round(daily_calories)

def get_macro_percentages(carbs_g, proteins_g, fats_g):
    """Calculate macro percentages from grams"""
    carb_calories = carbs_g * 4
    protein_calories = proteins_g * 4
    fat_calories = fats_g * 9
    
    total_calories = carb_calories + protein_calories + fat_calories
    
    if total_calories == 0:
        return {'carbs': 0, 'proteins': 0, 'fats': 0}
    
    return {
        'carbs': round((carb_calories / total_calories) * 100, 1),
        'proteins': round((protein_calories / total_calories) * 100, 1),
        'fats': round((fat_calories / total_calories) * 100, 1)
    }

def calculate_heart_rate_zones(age):
    """Calculate heart rate zones based on age"""
    max_hr = 220 - age
    
    return {
        'recovery': {'min': int(max_hr * 0.5), 'max': int(max_hr * 0.6)},
        'aerobic': {'min': int(max_hr * 0.6), 'max': int(max_hr * 0.7)},
        'threshold': {'min': int(max_hr * 0.7), 'max': int(max_hr * 0.85)},
        'maximum': {'min': int(max_hr * 0.85), 'max': max_hr}
    }

def get_heart_rate_zone(avg_bpm, age):
    """Determine which heart rate zone the average BPM falls into"""
    zones = calculate_heart_rate_zones(age)
    
    if avg_bpm <= zones['recovery']['max']:
        return 'Recovery Zone'
    elif avg_bpm <= zones['aerobic']['max']:
        return 'Aerobic Zone'
    elif avg_bpm <= zones['threshold']['max']:
        return 'Threshold Zone'
    else:
        return 'Maximum Zone'

def calculate_progress_score(user_id):
    """Calculate overall progress score (0-100) based on various factors"""
    user = User.query.get(user_id)
    if not user:
        return 0
    
    # Get data from last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        WorkoutLog.date >= thirty_days_ago.date()
    ).all()
    
    nutrition_logs = NutritionLog.query.filter(
        NutritionLog.user_id == user_id,
        NutritionLog.date >= thirty_days_ago.date()
    ).all()
    
    score = 0
    max_score = 100
    
    # BMI Score (20 points)
    bmi_score = 0
    if user.bmi:
        if 18.5 <= user.bmi <= 24.9:
            bmi_score = 20  # Perfect BMI
        elif 17 <= user.bmi < 18.5 or 25 <= user.bmi <= 27:
            bmi_score = 15  # Close to perfect
        elif 16 <= user.bmi < 17 or 27 < user.bmi <= 30:
            bmi_score = 10  # Needs improvement
        else:
            bmi_score = 5   # Significant improvement needed
    
    # Workout Consistency Score (30 points)
    workout_score = 0
    if workouts:
        workout_days = len(set([w.date for w in workouts]))
        consistency_ratio = workout_days / 30  # Days with workouts in last 30 days
        workout_score = min(30, int(consistency_ratio * 30 * 1.5))  # Bonus for high consistency
    
    # Nutrition Balance Score (25 points)
    nutrition_score = 0
    if nutrition_logs:
        total_carbs = sum([n.carbs for n in nutrition_logs])
        total_proteins = sum([n.proteins for n in nutrition_logs])
        total_fats = sum([n.fats for n in nutrition_logs])
        
        macro_percentages = get_macro_percentages(total_carbs, total_proteins, total_fats)
        
        # Ideal ranges: Carbs 45-65%, Protein 15-25%, Fat 20-35%
        carb_score = max(0, 10 - abs(macro_percentages['carbs'] - 55))
        protein_score = max(0, 8 - abs(macro_percentages['proteins'] - 20))
        fat_score = max(0, 7 - abs(macro_percentages['fats'] - 27.5))
        
        nutrition_score = carb_score + protein_score + fat_score
    
    # Activity Level Score (15 points)
    activity_score = 0
    if workouts:
        avg_duration = sum([w.session_duration for w in workouts]) / len(workouts)
        total_calories_burned = sum([w.calories_burned for w in workouts])
        
        # Score based on average workout duration and total calories
        duration_score = min(8, int(avg_duration * 8))  # Up to 8 points for 1+ hour avg
        calorie_score = min(7, int(total_calories_burned / 500))  # Up to 7 points for 3500+ calories
        
        activity_score = duration_score + calorie_score
    
    # Water Intake Score (10 points)
    water_score = 0
    if nutrition_logs:
        avg_water = sum([n.water_intake for n in nutrition_logs]) / len(nutrition_logs)
        if avg_water >= 2.5:
            water_score = 10
        elif avg_water >= 2.0:
            water_score = 8
        elif avg_water >= 1.5:
            water_score = 6
        elif avg_water >= 1.0:
            water_score = 4
        else:
            water_score = 2
    
    total_score = bmi_score + workout_score + nutrition_score + activity_score + water_score
    
    return min(100, total_score)

def get_fitness_recommendations(user_id):
    """Generate personalized fitness recommendations"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    recommendations = []
    
    # BMI-based recommendations
    if user.bmi:
        if user.bmi < 18.5:
            recommendations.append({
                'type': 'nutrition',
                'priority': 'high',
                'message': 'Consider increasing calorie intake with healthy, nutrient-dense foods to reach a healthy weight.'
            })
        elif user.bmi > 25:
            recommendations.append({
                'type': 'nutrition',
                'priority': 'high',
                'message': 'Focus on creating a moderate caloric deficit through balanced nutrition and regular exercise.'
            })
    
    # Get recent activity data
    week_ago = datetime.now() - timedelta(days=7)
    recent_workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        WorkoutLog.date >= week_ago.date()
    ).all()
    
    recent_nutrition = NutritionLog.query.filter(
        NutritionLog.user_id == user_id,
        NutritionLog.date >= week_ago.date()
    ).all()
    
    # Workout frequency recommendations
    if len(recent_workouts) < 3:
        recommendations.append({
            'type': 'workout',
            'priority': 'medium',
            'message': 'Try to increase workout frequency to at least 3-4 sessions per week for optimal results.'
        })
    elif len(recent_workouts) > 6:
        recommendations.append({
            'type': 'recovery',
            'priority': 'medium',
            'message': 'Great consistency! Make sure to include rest days for proper recovery.'
        })
    
    # Nutrition recommendations
    if recent_nutrition:
        avg_water = sum([n.water_intake for n in recent_nutrition]) / len(recent_nutrition)
        if avg_water < 2.0:
            recommendations.append({
                'type': 'hydration',
                'priority': 'medium',
                'message': 'Increase daily water intake to at least 2-2.5 liters for better performance and recovery.'
            })
        
        # Macro balance check
        total_carbs = sum([n.carbs for n in recent_nutrition])
        total_proteins = sum([n.proteins for n in recent_nutrition])
        total_fats = sum([n.fats for n in recent_nutrition])
        
        macro_percentages = get_macro_percentages(total_carbs, total_proteins, total_fats)
        
        if macro_percentages['proteins'] < 15:
            recommendations.append({
                'type': 'nutrition',
                'priority': 'medium',
                'message': 'Consider increasing protein intake to support muscle recovery and growth.'
            })
    
    # Experience level recommendations
    if user.experience_level == 1:  # Beginner
        recommendations.append({
            'type': 'workout',
            'priority': 'low',
            'message': 'Focus on learning proper form and gradually increasing workout intensity.'
        })
    elif user.experience_level == 3:  # Advanced
        recommendations.append({
            'type': 'workout',
            'priority': 'low',
            'message': 'Consider periodization and varying your training to prevent plateaus.'
        })
    
    return recommendations

def update_daily_stats(user_id, date=None):
    """Update or create daily stats for a user"""
    if date is None:
        date = datetime.now().date()
    
    # Get or create daily stats record
    daily_stats = DailyStats.query.filter_by(user_id=user_id, date=date).first()
    if not daily_stats:
        daily_stats = DailyStats(user_id=user_id, date=date)
        db.session.add(daily_stats)
    
    # Get all workouts for the day
    workouts = WorkoutLog.query.filter_by(user_id=user_id, date=date).all()
    daily_stats.total_calories_burned = sum([w.calories_burned for w in workouts])
    daily_stats.total_workout_duration = sum([w.session_duration for w in workouts])
    daily_stats.workout_count = len(workouts)
    
    # Get all nutrition logs for the day
    nutrition_logs = NutritionLog.query.filter_by(user_id=user_id, date=date).all()
    daily_stats.total_calories_consumed = sum([n.calories for n in nutrition_logs])
    daily_stats.total_carbs = sum([n.carbs for n in nutrition_logs])
    daily_stats.total_proteins = sum([n.proteins for n in nutrition_logs])
    daily_stats.total_fats = sum([n.fats for n in nutrition_logs])
    daily_stats.total_water_intake = sum([n.water_intake for n in nutrition_logs])
    daily_stats.meal_count = len(nutrition_logs)
    
    # Calculate caloric balance
    daily_stats.caloric_balance = daily_stats.total_calories_consumed - daily_stats.total_calories_burned
    
    # Update user's current stats
    user = User.query.get(user_id)
    if user:
        daily_stats.bmi_recorded = user.bmi
        daily_stats.weight_recorded = user.weight
        daily_stats.body_fat_recorded = user.fat_percentage
        daily_stats.resting_bpm_recorded = user.resting_bpm
    
    db.session.commit()
    return daily_stats

def get_weekly_summary(user_id):
    """Get weekly summary statistics"""
    week_start = datetime.now() - timedelta(days=7)
    
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        WorkoutLog.date >= week_start.date()
    ).all()
    
    nutrition = NutritionLog.query.filter(
        NutritionLog.user_id == user_id,
        NutritionLog.date >= week_start.date()
    ).all()
    
    summary = {
        'total_workouts': len(workouts),
        'total_calories_burned': sum([w.calories_burned for w in workouts]),
        'avg_session_duration': sum([w.session_duration for w in workouts]) / len(workouts) if workouts else 0,
        'total_meals_logged': len(nutrition),
        'avg_daily_intake': sum([n.calories for n in nutrition]) / 7 if nutrition else 0,
        'avg_water_intake': sum([n.water_intake for n in nutrition]) / 7 if nutrition else 0,
        'workout_types': list(set([w.workout_type for w in workouts])),
        'consistency_score': len(set([w.date for w in workouts])) / 7 * 100  # Percentage of days with workouts
    }
    
    if nutrition:
        total_carbs = sum([n.carbs for n in nutrition])
        total_proteins = sum([n.proteins for n in nutrition])
        total_fats = sum([n.fats for n in nutrition])
        summary['macro_percentages'] = get_macro_percentages(total_carbs, total_proteins, total_fats)
    else:
        summary['macro_percentages'] = {'carbs': 0, 'proteins': 0, 'fats': 0}
    
    return summary