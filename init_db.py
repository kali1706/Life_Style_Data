from app import create_app
from models import db

def init_database():
    """Initialize the database and create all tables"""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

        # Check if sample data was added
        from models import Exercise
        if Exercise.query.first():
            print("Sample exercises already exist in database")
        else:
            print("No sample exercises found - they will be added when app starts")

if __name__ == '__main__':
    init_database()
