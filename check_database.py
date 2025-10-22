#!/usr/bin/env python3
"""
Database Data Checker for Lifestyle Analytics
आपके database में data check करने के लिए
"""

from app import create_app
from models import User, WorkoutLog, NutritionLog, Meal, DailyStats, Exercise, Report
from sqlalchemy import text

def check_all_data():
    """Check all data in database"""
    print("🔍 DATABASE DATA CHECKER")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        # Users
        users = User.query.all()
        print(f"👥 USERS: {len(users)}")
        for user in users:
            print(f"   • {user.username} ({user.email}) - Created: {user.created_at}")
        
        # Exercises
        exercises = Exercise.query.all()
        print(f"\n🏃‍♂️ EXERCISES: {len(exercises)}")
        for exercise in exercises[:5]:  # Show first 5
            print(f"   • {exercise.name} - {exercise.difficulty_level}")
        if len(exercises) > 5:
            print(f"   ... and {len(exercises) - 5} more")
        
        # Workout Logs
        workouts = WorkoutLog.query.all()
        print(f"\n💪 WORKOUT LOGS: {len(workouts)}")
        for workout in workouts[:3]:  # Show first 3
            print(f"   • {workout.workout_type} - {workout.workout_date} - {workout.calories_burned} calories")
        
        # Nutrition Logs
        nutrition = NutritionLog.query.all()
        print(f"\n🍎 NUTRITION LOGS: {len(nutrition)}")
        for nut in nutrition[:3]:  # Show first 3
            print(f"   • {nut.log_date} - {nut.calories} calories - {nut.carbs}g carbs")
        
        # Meals
        meals = Meal.query.all()
        print(f"\n🍽️ MEALS: {len(meals)}")
        for meal in meals[:3]:  # Show first 3
            print(f"   • {meal.meal_name} - {meal.meal_date} - {meal.calories} calories")
        
        # Daily Stats
        daily_stats = DailyStats.query.all()
        print(f"\n📊 DAILY STATS: {len(daily_stats)}")
        for stat in daily_stats[:3]:  # Show first 3
            print(f"   • {stat.date} - Burned: {stat.total_calories_burned}, Consumed: {stat.total_calories_consumed}")
        
        # Reports
        reports = Report.query.all()
        print(f"\n📄 REPORTS: {len(reports)}")
        for report in reports[:3]:  # Show first 3
            print(f"   • {report.report_type} - {report.created_at}")

def check_specific_user(username):
    """Check data for specific user"""
    print(f"\n🔍 CHECKING DATA FOR USER: {username}")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ User '{username}' not found!")
            return
        
        print(f"✅ User found: {user.username} ({user.email})")
        print(f"   Age: {user.age}, Gender: {user.gender}")
        print(f"   Weight: {user.weight}kg, Height: {user.height}m")
        print(f"   BMI: {user.bmi}")
        
        # User's workouts
        workouts = user.workouts.all()
        print(f"\n💪 User's Workouts: {len(workouts)}")
        for workout in workouts:
            print(f"   • {workout.workout_type} - {workout.workout_date}")
        
        # User's nutrition logs
        nutrition = user.nutrition_logs.all()
        print(f"\n🍎 User's Nutrition Logs: {len(nutrition)}")
        for nut in nutrition:
            print(f"   • {nut.log_date} - {nut.calories} calories")
        
        # User's meals
        meals = user.meals.all()
        print(f"\n🍽️ User's Meals: {len(meals)}")
        for meal in meals:
            print(f"   • {meal.meal_name} - {meal.meal_date}")

def check_database_connection():
    """Check database connection"""
    print("🔌 CHECKING DATABASE CONNECTION")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Test basic query
            result = User.query.count()
            print(f"✅ Database connection successful!")
            print(f"✅ Can query users table: {result} users found")
            
            # Test raw SQL
            from sqlalchemy import text
            result = app.db.session.execute(text("SELECT COUNT(*) as count FROM users")).fetchone()
            print(f"✅ Raw SQL query successful: {result[0]} users")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

def show_database_info():
    """Show database information"""
    print("📊 DATABASE INFORMATION")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        from database_config import DatabaseConfig
        
        print(f"Platform: {DatabaseConfig.get_platform()}")
        print(f"Database Type: {DatabaseConfig.get_database_type()}")
        print(f"Connection URL: {DatabaseConfig.get_database_url()}")
        
        # Table counts
        tables = {
            'users': User.query.count(),
            'exercises': Exercise.query.count(),
            'workout_logs': WorkoutLog.query.count(),
            'nutrition_logs': NutritionLog.query.count(),
            'meals': Meal.query.count(),
            'daily_stats': DailyStats.query.count(),
            'reports': Report.query.count()
        }
        
        print(f"\n📋 TABLE RECORDS:")
        for table, count in tables.items():
            print(f"   {table}: {count}")

def main():
    """Main function"""
    print("🚀 LIFESTYLE ANALYTICS DATABASE CHECKER")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Check all data")
        print("2. Check specific user")
        print("3. Check database connection")
        print("4. Show database info")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            check_all_data()
        elif choice == '2':
            username = input("Enter username to check: ").strip()
            check_specific_user(username)
        elif choice == '3':
            check_database_connection()
        elif choice == '4':
            show_database_info()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

