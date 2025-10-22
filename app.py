from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User, Exercise
from routes import main
from config import Config
from email_service import EmailService
import os
import pymysql

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(main)

    # Initialize email service
    email_service = EmailService(app)

    # Create database tables
    with app.app_context():
        db.create_all()

        # Add sample exercises if database is empty
        if not Exercise.query.first():
            sample_exercises = [
                {
                    'name': 'Push-ups',
                    'benefit': 'Builds upper body strength, improves core stability',
                    'burns_calories_per_30min': 200,
                    'target_muscle_group': 'Chest, Shoulders, Triceps',
                    'equipment_needed': 'None',
                    'difficulty_level': 'Beginner',
                    'body_part': 'Arms',
                    'type_of_muscle': 'Upper',
                    'instructions': 'Start in plank position, lower body to ground, push back up'
                },
                {
                    'name': 'Squats',
                    'benefit': 'Builds leg strength, improves mobility',
                    'burns_calories_per_30min': 180,
                    'target_muscle_group': 'Quadriceps, Glutes, Hamstrings',
                    'equipment_needed': 'None',
                    'difficulty_level': 'Beginner',
                    'body_part': 'Legs',
                    'type_of_muscle': 'Lower',
                    'instructions': 'Stand with feet shoulder-width apart, lower as if sitting in chair, return to standing'
                },
                {
                    'name': 'Plank',
                    'benefit': 'Strengthens core, improves posture',
                    'burns_calories_per_30min': 150,
                    'target_muscle_group': 'Core, Shoulders',
                    'equipment_needed': 'None',
                    'difficulty_level': 'Beginner',
                    'body_part': 'Core',
                    'type_of_muscle': 'Core',
                    'instructions': 'Hold plank position with straight body line, engage core'
                },
                {
                    'name': 'Burpees',
                    'benefit': 'Full body workout, improves cardiovascular fitness',
                    'burns_calories_per_30min': 300,
                    'target_muscle_group': 'Full Body',
                    'equipment_needed': 'None',
                    'difficulty_level': 'Intermediate',
                    'body_part': 'Full Body',
                    'type_of_muscle': 'Full Body',
                    'instructions': 'Squat down, jump back to plank, do push-up, jump feet forward, jump up'
                },
                {
                    'name': 'Mountain Climbers',
                    'benefit': 'Cardio workout, strengthens core and shoulders',
                    'burns_calories_per_30min': 250,
                    'target_muscle_group': 'Core, Shoulders, Legs',
                    'equipment_needed': 'None',
                    'difficulty_level': 'Intermediate',
                    'body_part': 'Full Body',
                    'type_of_muscle': 'Full Body',
                    'instructions': 'Start in plank, alternate bringing knees to chest rapidly'
                }
            ]

            for exercise_data in sample_exercises:
                exercise = Exercise(**exercise_data)
                db.session.add(exercise)

            db.session.commit()
            print("Sample exercises added to database")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)