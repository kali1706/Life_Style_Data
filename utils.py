import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
import json

class AnalyticsCalculator:
    """Utility class for calculating various health and fitness metrics"""
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_m: float) -> float:
        """Calculate BMI from weight and height"""
        if height_m <= 0:
            return 0
        return round(weight_kg / (height_m ** 2), 2)
    
    @staticmethod
    def get_bmi_category(bmi: float) -> str:
        """Get BMI category based on BMI value"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    @staticmethod
    def calculate_caloric_balance(calories_consumed: int, calories_burned: int) -> int:
        """Calculate caloric balance (positive = surplus, negative = deficit)"""
        return calories_consumed - calories_burned
    
    @staticmethod
    def calculate_macro_percentages(carbs: int, proteins: int, fats: int) -> Dict[str, float]:
        """Calculate macro nutrient percentages"""
        total = carbs + proteins + fats
        if total == 0:
            return {"carbs": 0, "proteins": 0, "fats": 0}
        
        return {
            "carbs": round((carbs / total) * 100, 1),
            "proteins": round((proteins / total) * 100, 1),
            "fats": round((fats / total) * 100, 1)
        }
    
    @staticmethod
    def get_heart_rate_zones(max_hr: int) -> Dict[str, Tuple[int, int]]:
        """Calculate heart rate training zones"""
        return {
            "Zone 1 (Recovery)": (int(max_hr * 0.5), int(max_hr * 0.6)),
            "Zone 2 (Aerobic)": (int(max_hr * 0.6), int(max_hr * 0.7)),
            "Zone 3 (Threshold)": (int(max_hr * 0.7), int(max_hr * 0.85)),
            "Zone 4 (Maximum)": (int(max_hr * 0.85), int(max_hr * 1.0))
        }
    
    @staticmethod
    def get_body_fat_category(fat_percentage: float, gender: str) -> str:
        """Get body fat category based on percentage and gender"""
        if gender.lower() == 'male':
            if fat_percentage < 10:
                return "Very Low"
            elif 10 <= fat_percentage < 20:
                return "Fit"
            elif 20 <= fat_percentage < 25:
                return "Average"
            else:
                return "Above Average"
        else:  # female
            if fat_percentage < 18:
                return "Very Low"
            elif 18 <= fat_percentage < 25:
                return "Fit"
            elif 25 <= fat_percentage < 30:
                return "Average"
            else:
                return "Above Average"
    
    @staticmethod
    def calculate_consistency_score(workout_days: int, target_days: int) -> int:
        """Calculate consistency score (0-100)"""
        if target_days == 0:
            return 0
        return min(100, int((workout_days / target_days) * 100))
    
    @staticmethod
    def calculate_progress_score(bmi_improvement: float, calorie_balance: int, 
                               consistency: int, water_intake: float) -> int:
        """Calculate overall progress score (0-100)"""
        # BMI improvement (0-30 points)
        bmi_score = min(30, max(0, bmi_improvement * 10))
        
        # Calorie balance (0-25 points) - optimal range gets max points
        if -200 <= calorie_balance <= 200:  # Optimal range
            calorie_score = 25
        else:
            calorie_score = max(0, 25 - abs(calorie_balance) / 50)
        
        # Consistency (0-25 points)
        consistency_score = consistency * 0.25
        
        # Water intake (0-20 points) - 2.5L+ gets max points
        water_score = min(20, water_intake * 8)
        
        return int(bmi_score + calorie_score + consistency_score + water_score)

class DataProcessor:
    """Utility class for processing and aggregating data"""
    
    @staticmethod
    def get_weekly_summary(user_id: int, start_date: date, end_date: date) -> Dict:
        """Get weekly summary data for a user"""
        from models import WorkoutLog, NutritionLog, DailyStats
        
        # This would be implemented with actual database queries
        # For now, returning sample structure
        return {
            "total_workouts": 5,
            "total_calories_burned": 2500,
            "avg_session_duration": 45,
            "total_meals_logged": 21,
            "avg_daily_intake": 2100,
            "macro_avg": {"carbs": 45, "proteins": 25, "fats": 30},
            "bmi": 23.5,
            "body_fat": 18.2,
            "consistency_score": 92
        }
    
    @staticmethod
    def get_insights(user_data: Dict) -> List[str]:
        """Generate personalized insights based on user data"""
        insights = []
        
        # Workout insights
        if user_data.get('consistency_score', 0) > 90:
            insights.append("✓ Excellent workout consistency this week!")
        
        # Calorie balance insights
        calorie_balance = user_data.get('calorie_balance', 0)
        if -200 <= calorie_balance <= 200:
            insights.append("✓ Your calorie balance is optimal for weight maintenance")
        elif calorie_balance > 200:
            insights.append("! Consider reducing calorie intake for better balance")
        else:
            insights.append("! Consider increasing calorie intake for better balance")
        
        # Macro insights
        macro_avg = user_data.get('macro_avg', {})
        carbs = macro_avg.get('carbs', 0)
        proteins = macro_avg.get('proteins', 0)
        fats = macro_avg.get('fats', 0)
        
        if 40 <= carbs <= 65 and 10 <= proteins <= 35 and 20 <= fats <= 35:
            insights.append("✓ Macro ratios are well-balanced")
        else:
            insights.append("! Consider adjusting macro ratios for optimal nutrition")
        
        # Water intake insights
        water_intake = user_data.get('water_intake', 0)
        if water_intake < 2.5:
            insights.append("! Water intake slightly below recommended 2.5L daily")
        
        return insights

class ChartDataGenerator:
    """Utility class for generating chart data"""
    
    @staticmethod
    def generate_bmi_trend_data(user_id: int, days: int = 30) -> Dict:
        """Generate BMI trend data for charts"""
        # This would query actual BMI data from database
        # For now, returning sample data
        dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') 
                for i in range(days, 0, -1)]
        bmi_values = [23.5 + np.random.normal(0, 0.2) for _ in range(days)]
        
        return {
            "labels": dates,
            "data": [round(val, 2) for val in bmi_values],
            "title": "BMI Trend (Last 30 Days)"
        }
    
    @staticmethod
    def generate_calorie_balance_data(user_id: int, days: int = 7) -> Dict:
        """Generate calorie balance data for charts"""
        dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') 
                for i in range(days, 0, -1)]
        consumed = [2100 + np.random.randint(-200, 200) for _ in range(days)]
        burned = [1800 + np.random.randint(-300, 300) for _ in range(days)]
        
        return {
            "labels": dates,
            "datasets": [
                {"label": "Calories Consumed", "data": consumed, "backgroundColor": "rgba(54, 162, 235, 0.6)"},
                {"label": "Calories Burned", "data": burned, "backgroundColor": "rgba(255, 99, 132, 0.6)"}
            ],
            "title": "Daily Calorie Balance (Last 7 Days)"
        }
    
    @staticmethod
    def generate_macro_breakdown_data(user_data: Dict) -> Dict:
        """Generate macro nutrient breakdown for pie chart"""
        macro_avg = user_data.get('macro_avg', {})
        return {
            "labels": ["Carbs", "Proteins", "Fats"],
            "data": [
                macro_avg.get('carbs', 0),
                macro_avg.get('proteins', 0),
                macro_avg.get('fats', 0)
            ],
            "backgroundColor": [
                "rgba(255, 99, 132, 0.6)",
                "rgba(54, 162, 235, 0.6)",
                "rgba(255, 205, 86, 0.6)"
            ],
            "title": "Macro Nutrient Distribution"
        }

class EmailTemplate:
    """Utility class for email templates"""
    
    @staticmethod
    def generate_weekly_report_email(user_name: str, report_data: Dict) -> str:
        """Generate HTML email template for weekly report"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Your Weekly Lifestyle Report</h2>
                <p>Dear {user_name},</p>
                
                <p>Here's your detailed weekly lifestyle analysis:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">Highlights:</h3>
                    <ul>
                        <li>Workouts Completed: {report_data.get('total_workouts', 0)}</li>
                        <li>Calories Burned: {report_data.get('total_calories_burned', 0)} kcal</li>
                        <li>Average Daily Intake: {report_data.get('avg_daily_intake', 0)} kcal</li>
                        <li>BMI Status: {report_data.get('bmi', 0)} ({report_data.get('bmi_category', 'Unknown')})</li>
                        <li>Consistency: {report_data.get('consistency_score', 0)}%</li>
                    </ul>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3 style="color: #2c3e50;">Key Insights:</h3>
                    <ul>
                        {''.join([f'<li>{insight}</li>' for insight in report_data.get('insights', [])])}
                    </ul>
                </div>
                
                <p>Keep up the great work! Your detailed report is attached as a PDF.</p>
                
                <p>Best Regards,<br>
                Lifestyle Analytics Team</p>
            </div>
        </body>
        </html>
        """