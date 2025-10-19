"""Utility functions for calculations and analytics"""
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, WorkoutLog, NutritionLog, Meal, User, DailyStats
import pandas as pd
import numpy as np


def calculate_bmi(weight_kg, height_m):
    """Calculate BMI"""
    if height_m <= 0:
        return None
    return round(weight_kg / (height_m ** 2), 2)


def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi is None:
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def get_body_fat_category(fat_percentage, gender):
    """Get body fat category based on gender"""
    if fat_percentage is None:
        return "Unknown"
    
    if gender.lower() == 'male':
        if fat_percentage < 10:
            return "Very Low"
        elif fat_percentage < 20:
            return "Fit"
        elif fat_percentage < 25:
            return "Average"
        else:
            return "Above Average"
    else:  # Female
        if fat_percentage < 18:
            return "Very Low"
        elif fat_percentage < 25:
            return "Fit"
        elif fat_percentage < 30:
            return "Average"
        else:
            return "Above Average"


def calculate_macro_percentages(carbs, proteins, fats):
    """Calculate macro percentages"""
    # Convert grams to calories
    carb_cal = carbs * 4
    protein_cal = proteins * 4
    fat_cal = fats * 9
    
    total_cal = carb_cal + protein_cal + fat_cal
    
    if total_cal == 0:
        return {"Carbs": 0, "Protein": 0, "Fat": 0}
    
    return {
        "Carbs": round((carb_cal / total_cal) * 100, 1),
        "Protein": round((protein_cal / total_cal) * 100, 1),
        "Fat": round((fat_cal / total_cal) * 100, 1)
    }


def analyze_macro_balance(carbs_pct, protein_pct, fat_pct):
    """Analyze if macro ratios are balanced"""
    recommendations = []
    
    # Ideal ranges: Carbs 45-65%, Protein 10-35%, Fat 20-35%
    if carbs_pct < 45:
        recommendations.append("Increase carbohydrate intake")
    elif carbs_pct > 65:
        recommendations.append("Reduce carbohydrate intake")
    
    if protein_pct < 10:
        recommendations.append("Increase protein intake")
    elif protein_pct > 35:
        recommendations.append("Reduce protein intake")
    
    if fat_pct < 20:
        recommendations.append("Increase healthy fat intake")
    elif fat_pct > 35:
        recommendations.append("Reduce fat intake")
    
    if not recommendations:
        return "Macro balance is optimal!"
    
    return recommendations


def calculate_heart_rate_zone(hr, max_hr=None, age=None):
    """Calculate heart rate zone"""
    if max_hr is None and age:
        max_hr = 220 - age
    
    if max_hr is None:
        return "Unknown"
    
    percentage = (hr / max_hr) * 100
    
    if percentage < 60:
        return "Zone 1 - Recovery"
    elif percentage < 70:
        return "Zone 2 - Aerobic"
    elif percentage < 85:
        return "Zone 3 - Threshold"
    else:
        return "Zone 4 - Maximum"


def get_weekly_stats(user_id, start_date=None):
    """Get weekly statistics for a user"""
    if start_date is None:
        start_date = datetime.utcnow() - timedelta(days=7)
    
    end_date = datetime.utcnow()
    
    # Workout stats
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        WorkoutLog.date >= start_date,
        WorkoutLog.date <= end_date
    ).all()
    
    # Nutrition stats
    nutrition_logs = NutritionLog.query.filter(
        NutritionLog.user_id == user_id,
        NutritionLog.date >= start_date.date(),
        NutritionLog.date <= end_date.date()
    ).all()
    
    total_workouts = len(workouts)
    total_calories_burned = sum(w.calories_burned or 0 for w in workouts)
    avg_workout_duration = np.mean([w.session_duration or 0 for w in workouts]) if workouts else 0
    
    total_calories_consumed = sum(n.total_calories or 0 for n in nutrition_logs)
    total_meals = sum(len(n.meals) for n in nutrition_logs)
    
    # Calculate averages
    avg_daily_intake = total_calories_consumed / 7 if nutrition_logs else 0
    
    # Macro totals
    total_carbs = sum(n.total_carbs or 0 for n in nutrition_logs)
    total_proteins = sum(n.total_proteins or 0 for n in nutrition_logs)
    total_fats = sum(n.total_fats or 0 for n in nutrition_logs)
    
    macro_percentages = calculate_macro_percentages(total_carbs, total_proteins, total_fats)
    
    # Consistency score
    workout_days = len(set(w.date.date() for w in workouts))
    consistency_score = round((workout_days / 7) * 100, 1)
    
    return {
        "total_workouts": total_workouts,
        "total_calories_burned": total_calories_burned,
        "avg_workout_duration": round(avg_workout_duration * 60, 1),  # in minutes
        "total_calories_consumed": total_calories_consumed,
        "avg_daily_intake": round(avg_daily_intake),
        "total_meals": total_meals,
        "macro_percentages": macro_percentages,
        "consistency_score": consistency_score,
        "calorie_balance": total_calories_consumed - total_calories_burned
    }


def get_monthly_trends(user_id):
    """Get monthly trends data"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    # Get daily stats
    daily_stats = DailyStats.query.filter(
        DailyStats.user_id == user_id,
        DailyStats.date >= start_date.date(),
        DailyStats.date <= end_date.date()
    ).order_by(DailyStats.date).all()
    
    if not daily_stats:
        return None
    
    dates = [stat.date.strftime('%Y-%m-%d') for stat in daily_stats]
    weights = [stat.weight for stat in daily_stats if stat.weight]
    bmis = [stat.bmi for stat in daily_stats if stat.bmi]
    calories_burned = [stat.total_calories_burned or 0 for stat in daily_stats]
    calories_consumed = [stat.total_calories_consumed or 0 for stat in daily_stats]
    
    return {
        "dates": dates,
        "weights": weights,
        "bmis": bmis,
        "calories_burned": calories_burned,
        "calories_consumed": calories_consumed
    }


def generate_insights(user):
    """Generate personalized insights for user"""
    insights = []
    recommendations = []
    
    # Get weekly stats
    weekly_stats = get_weekly_stats(user.id)
    
    # BMI analysis
    if user.bmi:
        bmi_category = user.get_bmi_category()
        insights.append(f"Your current BMI is {user.bmi} ({bmi_category})")
        
        if bmi_category == "Overweight":
            recommendations.append("Focus on calorie deficit and increase cardio workouts")
        elif bmi_category == "Underweight":
            recommendations.append("Increase calorie intake with protein-rich foods")
    
    # Workout consistency
    if weekly_stats['consistency_score'] >= 80:
        insights.append(f"Excellent workout consistency this week! ({weekly_stats['consistency_score']}%)")
    elif weekly_stats['consistency_score'] < 50:
        recommendations.append("Try to work out at least 4 days per week")
    
    # Calorie balance
    cal_balance = weekly_stats['calorie_balance']
    if abs(cal_balance) < 500:
        insights.append("Your calorie balance is optimal for weight maintenance")
    elif cal_balance > 500:
        insights.append("You're in a calorie surplus - good for muscle gain")
    else:
        insights.append("You're in a calorie deficit - good for weight loss")
    
    # Macro analysis
    macro_pct = weekly_stats['macro_percentages']
    macro_recommendations = analyze_macro_balance(
        macro_pct['Carbs'], 
        macro_pct['Protein'], 
        macro_pct['Fat']
    )
    
    if isinstance(macro_recommendations, list):
        recommendations.extend(macro_recommendations)
    else:
        insights.append(macro_recommendations)
    
    # Water intake check (if we have recent data)
    recent_nutrition = NutritionLog.query.filter(
        NutritionLog.user_id == user.id
    ).order_by(NutritionLog.date.desc()).first()
    
    if recent_nutrition and recent_nutrition.water_intake:
        if recent_nutrition.water_intake < 2.5:
            recommendations.append(f"Increase water intake to at least 2.5L daily (currently {recent_nutrition.water_intake}L)")
        else:
            insights.append("Great job staying hydrated!")
    
    # Workout variation
    recent_workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user.id
    ).order_by(WorkoutLog.date.desc()).limit(5).all()
    
    if recent_workouts:
        workout_types = set(w.workout_type for w in recent_workouts)
        if len(workout_types) == 1:
            recommendations.append("Try different workout types to prevent plateau")
    
    return {
        "insights": insights,
        "recommendations": recommendations
    }


def calculate_progress_score(user):
    """Calculate overall progress score (0-100)"""
    score = 0
    max_score = 100
    
    # BMI score (30 points)
    if user.bmi:
        bmi_category = user.get_bmi_category()
        if bmi_category == "Normal":
            score += 30
        elif bmi_category in ["Overweight", "Underweight"]:
            score += 15
    
    # Consistency score (40 points)
    weekly_stats = get_weekly_stats(user.id)
    score += (weekly_stats['consistency_score'] / 100) * 40
    
    # Macro balance (30 points)
    macro_pct = weekly_stats['macro_percentages']
    carbs_ok = 45 <= macro_pct['Carbs'] <= 65
    protein_ok = 10 <= macro_pct['Protein'] <= 35
    fat_ok = 20 <= macro_pct['Fat'] <= 35
    
    if carbs_ok:
        score += 10
    if protein_ok:
        score += 10
    if fat_ok:
        score += 10
    
    return round(score)


def update_daily_stats(user_id, date=None):
    """Update or create daily stats for a user"""
    if date is None:
        date = datetime.utcnow().date()
    
    # Get or create daily stat
    daily_stat = DailyStats.query.filter_by(user_id=user_id, date=date).first()
    if not daily_stat:
        daily_stat = DailyStats(user_id=user_id, date=date)
        db.session.add(daily_stat)
    
    # Calculate workout stats
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        func.date(WorkoutLog.date) == date
    ).all()
    
    daily_stat.total_workouts = len(workouts)
    daily_stat.total_workout_duration = sum(w.session_duration or 0 for w in workouts)
    daily_stat.total_calories_burned = sum(w.calories_burned or 0 for w in workouts)
    
    # Calculate nutrition stats
    nutrition_log = NutritionLog.query.filter_by(user_id=user_id, date=date).first()
    if nutrition_log:
        daily_stat.total_calories_consumed = nutrition_log.total_calories or 0
        daily_stat.total_meals = len(nutrition_log.meals)
        daily_stat.calorie_balance = daily_stat.total_calories_consumed - daily_stat.total_calories_burned
    
    # Update body metrics
    user = User.query.get(user_id)
    if user:
        daily_stat.weight = user.weight
        daily_stat.bmi = user.bmi
        daily_stat.fat_percentage = user.fat_percentage
    
    db.session.commit()
    return daily_stat
