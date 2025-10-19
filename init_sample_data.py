#!/usr/bin/env python3
"""
Sample Data Initialization Script for Lifestyle Analytics Platform

This script populates the database with sample data for demonstration purposes.
Run this after setting up the database to see the platform in action.
"""

from app import app, db
from models import User, WorkoutLog, NutritionLog, Meal, Exercise, DailyStats
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_users():
    """Create sample users with different profiles"""
    users = [
        {
            'username': 'demo_beginner',
            'email': 'demo@beginner.com',
            'password': 'demo123456',
            'age': 25,
            'gender': 'Female',
            'weight': 65.0,
            'height': 1.65,
            'experience_level': 1,
            'fat_percentage': 22.0,
            'resting_bpm': 75
        },
        {
            'username': 'demo_advanced',
            'email': 'demo@advanced.com',
            'password': 'demo123456',
            'age': 30,
            'gender': 'Male',
            'weight': 80.0,
            'height': 1.78,
            'experience_level': 3,
            'fat_percentage': 12.0,
            'resting_bpm': 60
        },
        {
            'username': 'fitness_enthusiast',
            'email': 'fitness@example.com',
            'password': 'fitness123',
            'age': 28,
            'gender': 'Female',
            'weight': 58.0,
            'height': 1.62,
            'experience_level': 2,
            'fat_percentage': 18.0,
            'resting_bpm': 68
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            print(f"User {user_data['username']} already exists, skipping...")
            created_users.append(existing_user)
            continue
        
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            age=user_data['age'],
            gender=user_data['gender'],
            weight=user_data['weight'],
            height=user_data['height'],
            experience_level=user_data['experience_level'],
            fat_percentage=user_data['fat_percentage'],
            resting_bpm=user_data['resting_bpm']
        )
        
        # Calculate BMI
        user.bmi = user_data['weight'] / (user_data['height'] ** 2)
        
        db.session.add(user)
        created_users.append(user)
        print(f"Created user: {user_data['username']}")
    
    return created_users

def create_sample_exercises():
    """Create sample exercise library"""
    exercises = [
        {
            'name': 'Push-ups',
            'target_muscle_group': 'Chest',
            'body_part': 'Upper Body',
            'type_of_muscle': 'Upper',
            'difficulty_level': 'Beginner',
            'equipment_needed': 'Bodyweight',
            'sets': 3,
            'reps': 15,
            'benefit': 'Builds chest, shoulder, and tricep strength while improving core stability.',
            'burns_calories_per_30min': 180
        },
        {
            'name': 'Squats',
            'target_muscle_group': 'Legs',
            'body_part': 'Lower Body',
            'type_of_muscle': 'Lower',
            'difficulty_level': 'Beginner',
            'equipment_needed': 'Bodyweight',
            'sets': 3,
            'reps': 20,
            'benefit': 'Strengthens quadriceps, glutes, and hamstrings while improving functional movement.',
            'burns_calories_per_30min': 200
        },
        {
            'name': 'Deadlifts',
            'target_muscle_group': 'Back',
            'body_part': 'Full Body',
            'type_of_muscle': 'Lower',
            'difficulty_level': 'Advanced',
            'equipment_needed': 'Barbell',
            'sets': 3,
            'reps': 8,
            'benefit': 'Builds total-body strength, focusing on posterior chain muscles.',
            'burns_calories_per_30min': 250
        },
        {
            'name': 'Plank',
            'target_muscle_group': 'Core',
            'body_part': 'Core',
            'type_of_muscle': 'Core',
            'difficulty_level': 'Intermediate',
            'equipment_needed': 'Bodyweight',
            'sets': 3,
            'reps': 1,
            'benefit': 'Strengthens core muscles and improves posture and stability.',
            'burns_calories_per_30min': 150
        },
        {
            'name': 'Burpees',
            'target_muscle_group': 'Full Body',
            'body_part': 'Full Body',
            'type_of_muscle': 'Upper',
            'difficulty_level': 'Advanced',
            'equipment_needed': 'Bodyweight',
            'sets': 3,
            'reps': 10,
            'benefit': 'High-intensity full-body exercise that improves cardiovascular fitness.',
            'burns_calories_per_30min': 300
        },
        {
            'name': 'Running',
            'target_muscle_group': 'Legs',
            'body_part': 'Lower Body',
            'type_of_muscle': 'Lower',
            'difficulty_level': 'Intermediate',
            'equipment_needed': 'None',
            'sets': 1,
            'reps': 1,
            'benefit': 'Excellent cardiovascular exercise that builds endurance and burns calories.',
            'burns_calories_per_30min': 400
        }
    ]
    
    created_exercises = []
    for exercise_data in exercises:
        # Check if exercise already exists
        existing_exercise = Exercise.query.filter_by(name=exercise_data['name']).first()
        if existing_exercise:
            print(f"Exercise {exercise_data['name']} already exists, skipping...")
            created_exercises.append(existing_exercise)
            continue
        
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
        created_exercises.append(exercise)
        print(f"Created exercise: {exercise_data['name']}")
    
    return created_exercises

def create_sample_meals():
    """Create sample meal database"""
    meals = [
        {
            'name': 'Grilled Chicken Breast',
            'meal_type': 'Main',
            'diet_type': 'High Protein',
            'calories_per_100g': 165,
            'carbs_per_100g': 0,
            'proteins_per_100g': 31,
            'fats_per_100g': 4,
            'sugar_per_100g': 0,
            'sodium_per_100g': 74,
            'cholesterol_per_100g': 85,
            'cooking_method': 'Grilled',
            'prep_time': 10,
            'cook_time': 15,
            'is_healthy': True
        },
        {
            'name': 'Brown Rice',
            'meal_type': 'Main',
            'diet_type': 'Balanced',
            'calories_per_100g': 111,
            'carbs_per_100g': 23,
            'proteins_per_100g': 3,
            'fats_per_100g': 1,
            'sugar_per_100g': 0,
            'sodium_per_100g': 5,
            'cholesterol_per_100g': 0,
            'cooking_method': 'Boiled',
            'prep_time': 5,
            'cook_time': 45,
            'is_healthy': True
        },
        {
            'name': 'Greek Yogurt',
            'meal_type': 'Snack',
            'diet_type': 'High Protein',
            'calories_per_100g': 59,
            'carbs_per_100g': 4,
            'proteins_per_100g': 10,
            'fats_per_100g': 0,
            'sugar_per_100g': 4,
            'sodium_per_100g': 36,
            'cholesterol_per_100g': 5,
            'cooking_method': 'Raw',
            'prep_time': 0,
            'cook_time': 0,
            'is_healthy': True
        },
        {
            'name': 'Avocado Toast',
            'meal_type': 'Main',
            'diet_type': 'Balanced',
            'calories_per_100g': 190,
            'carbs_per_100g': 18,
            'proteins_per_100g': 5,
            'fats_per_100g': 12,
            'sugar_per_100g': 2,
            'sodium_per_100g': 200,
            'cholesterol_per_100g': 0,
            'cooking_method': 'Raw',
            'prep_time': 5,
            'cook_time': 2,
            'is_healthy': True
        },
        {
            'name': 'Chocolate Chip Cookie',
            'meal_type': 'Snack',
            'diet_type': 'Treat',
            'calories_per_100g': 488,
            'carbs_per_100g': 68,
            'proteins_per_100g': 6,
            'fats_per_100g': 22,
            'sugar_per_100g': 35,
            'sodium_per_100g': 365,
            'cholesterol_per_100g': 31,
            'cooking_method': 'Baked',
            'prep_time': 15,
            'cook_time': 12,
            'is_healthy': False
        },
        {
            'name': 'Salmon Fillet',
            'meal_type': 'Main',
            'diet_type': 'Keto',
            'calories_per_100g': 208,
            'carbs_per_100g': 0,
            'proteins_per_100g': 25,
            'fats_per_100g': 12,
            'sugar_per_100g': 0,
            'sodium_per_100g': 59,
            'cholesterol_per_100g': 55,
            'cooking_method': 'Grilled',
            'prep_time': 5,
            'cook_time': 12,
            'is_healthy': True
        }
    ]
    
    created_meals = []
    for meal_data in meals:
        # Check if meal already exists
        existing_meal = Meal.query.filter_by(name=meal_data['name']).first()
        if existing_meal:
            print(f"Meal {meal_data['name']} already exists, skipping...")
            created_meals.append(existing_meal)
            continue
        
        meal = Meal(**meal_data)
        db.session.add(meal)
        created_meals.append(meal)
        print(f"Created meal: {meal_data['name']}")
    
    return created_meals

def create_sample_workouts(users):
    """Create sample workout data for the past 30 days"""
    workout_types = ['Strength', 'Cardio', 'HIIT', 'Yoga', 'Running', 'Cycling']
    intensity_levels = ['Low', 'Moderate', 'High', 'Very High']
    
    for user in users:
        print(f"Creating workout data for {user.username}...")
        
        # Create workouts for the past 30 days
        for i in range(30):
            date = datetime.now().date() - timedelta(days=i)
            
            # Skip some days randomly to simulate real usage
            if random.random() < 0.3:  # 30% chance to skip a day
                continue
            
            # Create 1-2 workouts per day
            num_workouts = random.choices([1, 2], weights=[0.8, 0.2])[0]
            
            for j in range(num_workouts):
                workout_type = random.choice(workout_types)
                
                # Adjust parameters based on user experience level
                if user.experience_level == 1:  # Beginner
                    duration = random.uniform(0.5, 1.5)
                    calories_base = 200
                    max_bpm_base = 160
                elif user.experience_level == 2:  # Intermediate
                    duration = random.uniform(0.75, 2.0)
                    calories_base = 300
                    max_bpm_base = 170
                else:  # Advanced
                    duration = random.uniform(1.0, 2.5)
                    calories_base = 400
                    max_bpm_base = 180
                
                # Adjust calories based on workout type
                type_multipliers = {
                    'Strength': 0.8,
                    'Cardio': 1.2,
                    'HIIT': 1.4,
                    'Yoga': 0.6,
                    'Running': 1.3,
                    'Cycling': 1.1
                }
                
                calories_burned = int(calories_base * type_multipliers.get(workout_type, 1.0) * duration * random.uniform(0.8, 1.2))
                max_bpm = int(max_bpm_base * random.uniform(0.85, 1.0))
                avg_bpm = int(max_bpm * random.uniform(0.75, 0.9))
                
                workout = WorkoutLog(
                    user_id=user.id,
                    workout_type=workout_type,
                    session_duration=round(duration, 2),
                    calories_burned=calories_burned,
                    max_bpm=max_bpm,
                    avg_bpm=avg_bpm,
                    intensity_level=random.choice(intensity_levels),
                    workout_frequency=random.randint(3, 6),
                    date=date
                )
                
                db.session.add(workout)
    
    print("Sample workout data created successfully!")

def create_sample_nutrition(users):
    """Create sample nutrition data for the past 30 days"""
    meal_names = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
    diet_types = ['Balanced', 'High Protein', 'Keto', 'Vegan', 'Mediterranean']
    
    for user in users:
        print(f"Creating nutrition data for {user.username}...")
        
        # Create nutrition logs for the past 30 days
        for i in range(30):
            date = datetime.now().date() - timedelta(days=i)
            
            # Create 3-5 meals per day
            num_meals = random.randint(3, 5)
            daily_water = 0
            
            for j in range(num_meals):
                meal_name = meal_names[min(j, len(meal_names) - 1)]
                if j >= 3:  # Additional meals are snacks
                    meal_name = 'Snack'
                
                # Adjust portion sizes based on meal type
                portion_multipliers = {
                    'Breakfast': random.uniform(0.8, 1.2),
                    'Lunch': random.uniform(1.0, 1.4),
                    'Dinner': random.uniform(1.0, 1.3),
                    'Snack': random.uniform(0.3, 0.7)
                }
                
                multiplier = portion_multipliers.get(meal_name, 1.0)
                
                # Base nutritional values (adjusted by multiplier)
                base_calories = int(random.randint(200, 600) * multiplier)
                
                # Calculate macros with some variation
                # Typical macro split: 45-65% carbs, 10-35% protein, 20-35% fat
                carb_percent = random.uniform(0.40, 0.60)
                protein_percent = random.uniform(0.15, 0.30)
                fat_percent = 1.0 - carb_percent - protein_percent
                
                carbs = int((base_calories * carb_percent) / 4)  # 4 cal per gram
                proteins = int((base_calories * protein_percent) / 4)  # 4 cal per gram
                fats = int((base_calories * fat_percent) / 9)  # 9 cal per gram
                
                # Water intake (more with meals, less with snacks)
                if meal_name == 'Snack':
                    water_with_meal = random.uniform(0.1, 0.3)
                else:
                    water_with_meal = random.uniform(0.3, 0.6)
                
                daily_water += water_with_meal
                
                nutrition = NutritionLog(
                    user_id=user.id,
                    meal_name=meal_name,
                    meal_type='Main' if meal_name != 'Snack' else 'Snack',
                    diet_type=random.choice(diet_types),
                    calories=base_calories,
                    carbs=carbs,
                    proteins=proteins,
                    fats=fats,
                    sugar=random.randint(5, 25),
                    sodium=random.randint(100, 800),
                    cholesterol=random.randint(0, 100),
                    serving_size=random.randint(100, 400),
                    water_intake=round(water_with_meal, 1),
                    daily_meals_frequency=num_meals,
                    is_healthy=random.choices([True, False], weights=[0.8, 0.2])[0],
                    date=date
                )
                
                db.session.add(nutrition)
            
            # Ensure daily water intake is reasonable (2-4 liters)
            if daily_water < 2.0:
                # Add additional water intake
                additional_water = random.uniform(1.0, 2.0)
                if nutrition:  # Add to last meal of the day
                    nutrition.water_intake += additional_water
    
    print("Sample nutrition data created successfully!")

def create_daily_stats(users):
    """Create aggregated daily statistics"""
    for user in users:
        print(f"Creating daily stats for {user.username}...")
        
        for i in range(30):
            date = datetime.now().date() - timedelta(days=i)
            
            # Get workouts for this date
            workouts = WorkoutLog.query.filter_by(user_id=user.id, date=date).all()
            nutrition = NutritionLog.query.filter_by(user_id=user.id, date=date).all()
            
            if not workouts and not nutrition:
                continue
            
            # Calculate daily aggregates
            total_calories_burned = sum([w.calories_burned for w in workouts])
            total_calories_consumed = sum([n.calories for n in nutrition])
            total_water_intake = sum([n.water_intake for n in nutrition])
            total_carbs = sum([n.carbs for n in nutrition])
            total_proteins = sum([n.proteins for n in nutrition])
            total_fats = sum([n.fats for n in nutrition])
            total_workout_duration = sum([w.session_duration for w in workouts])
            
            daily_stat = DailyStats(
                user_id=user.id,
                date=date,
                total_calories_consumed=total_calories_consumed,
                total_calories_burned=total_calories_burned,
                total_water_intake=round(total_water_intake, 1),
                total_carbs=total_carbs,
                total_proteins=total_proteins,
                total_fats=total_fats,
                total_workout_duration=round(total_workout_duration, 2),
                workout_count=len(workouts),
                meal_count=len(nutrition),
                caloric_balance=total_calories_consumed - total_calories_burned,
                weight_recorded=user.weight + random.uniform(-1, 1),  # Simulate weight fluctuation
                body_fat_recorded=user.fat_percentage + random.uniform(-0.5, 0.5),
                resting_bpm_recorded=user.resting_bpm + random.randint(-5, 5),
                bmi_recorded=user.bmi
            )
            
            db.session.add(daily_stat)
    
    print("Daily statistics created successfully!")

def main():
    """Main function to initialize all sample data"""
    print("🏋️‍♀️ Initializing Lifestyle Analytics Platform with sample data...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Create sample users
            print("\n📝 Creating sample users...")
            users = create_sample_users()
            
            # Create sample exercises
            print("\n💪 Creating exercise library...")
            exercises = create_sample_exercises()
            
            # Create sample meals
            print("\n🍎 Creating meal database...")
            meals = create_sample_meals()
            
            # Commit users, exercises, and meals first
            db.session.commit()
            print("\n✅ Basic data committed to database")
            
            # Create sample workouts
            print("\n🏃‍♀️ Creating sample workout data...")
            create_sample_workouts(users)
            
            # Create sample nutrition
            print("\n🥗 Creating sample nutrition data...")
            create_sample_nutrition(users)
            
            # Create daily statistics
            print("\n📊 Creating daily statistics...")
            create_daily_stats(users)
            
            # Final commit
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("🎉 Sample data initialization completed successfully!")
            print("\n📋 Summary:")
            print(f"   👥 Users created: {len(users)}")
            print(f"   💪 Exercises created: {len(exercises)}")
            print(f"   🍎 Meals created: {len(meals)}")
            print(f"   🏃‍♀️ Workout logs: ~{len(users) * 20} entries")
            print(f"   🥗 Nutrition logs: ~{len(users) * 120} entries")
            print(f"   📊 Daily statistics: ~{len(users) * 30} entries")
            
            print("\n🔑 Demo Login Credentials:")
            print("   Beginner User:")
            print("     Email: demo@beginner.com")
            print("     Password: demo123456")
            print("\n   Advanced User:")
            print("     Email: demo@advanced.com")
            print("     Password: demo123456")
            
            print("\n🚀 You can now start the application with: python app.py")
            print("   Navigate to http://localhost:5000 to begin!")
            
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            db.session.rollback()
            raise
        
        finally:
            db.session.close()

if __name__ == "__main__":
    main()