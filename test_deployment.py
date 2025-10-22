#!/usr/bin/env python3
"""
Test script for deployment environment
यह script deployment environment को test करने के लिए है
"""

import os
import sys
from app import create_app
from models import db, User, Exercise

def test_deployment():
    """Test deployment configuration"""
    print("TESTING DEPLOYMENT CONFIGURATION")
    print("=" * 50)
    
    # Check environment
    print(f"Platform: {sys.platform}")
    print(f"Python Version: {sys.version}")
    print(f"Render Environment: {os.environ.get('RENDER', 'Not detected')}")
    print(f"Database Type: {os.environ.get('DATABASE_TYPE', 'Auto-detect')}")
    
    # Test database configuration
    try:
        from database_config import DatabaseConfig
        db_type = DatabaseConfig.get_database_type()
        db_url = DatabaseConfig.get_database_url()
        
        print(f"\nDatabase Type: {db_type}")
        print(f"Database URL: {db_url[:50]}...")
        
        # Test app creation
        app = create_app()
        print(f"Flask App Created Successfully")
        print(f"App Config DB URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        # Test database connection
        with app.app_context():
            try:
                # Test basic query
                user_count = User.query.count()
                print(f"Database Connection: SUCCESS")
                print(f"Users in database: {user_count}")
                
                # Test table creation
                db.create_all()
                print(f"Tables created/verified successfully")
                
                # Test exercise data
                exercise_count = Exercise.query.count()
                print(f"Exercises in database: {exercise_count}")
                
            except Exception as e:
                print(f"Database Connection Error: {e}")
                return False
                
    except Exception as e:
        print(f"Configuration Error: {e}")
        return False
    
    print(f"\nDEPLOYMENT TEST PASSED!")
    return True

def test_environment_variables():
    """Test environment variables"""
    print("\nENVIRONMENT VARIABLES")
    print("=" * 30)
    
    env_vars = [
        'DATABASE_TYPE',
        'DATABASE_URL', 
        'POSTGRES_HOST',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_DATABASE',
        'FLASK_ENV',
        'SECRET_KEY',
        'PORT'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        if 'PASSWORD' in var or 'SECRET' in var:
            value = '***' if value != 'Not set' else value
        print(f"{var}: {value}")

if __name__ == '__main__':
    test_environment_variables()
    success = test_deployment()
    
    if success:
        print("\nAll tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("\nSome tests failed. Check the errors above.")
        sys.exit(1)
