import os
from datetime import timedelta

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@lifestyleanalytics.com'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Report settings
    REPORTS_FOLDER = os.path.join(BASE_DIR, 'reports')
    
    # Analytics settings
    CHART_EXPORT_PATH = os.path.join(BASE_DIR, 'static', 'charts')
    
    # Health metrics configuration
    BMI_CATEGORIES = {
        'Underweight': (0, 18.5),
        'Normal': (18.5, 25),
        'Overweight': (25, 30),
        'Obese': (30, 100)
    }
    
    BODY_FAT_CATEGORIES = {
        'Male': {
            'Very Low': (0, 10),
            'Fit': (10, 20),
            'Average': (20, 25),
            'Above Average': (25, 100)
        },
        'Female': {
            'Very Low': (0, 18),
            'Fit': (18, 25),
            'Average': (25, 30),
            'Above Average': (30, 100)
        }
    }
    
    MACRO_IDEAL_RANGES = {
        'Carbs': (45, 65),
        'Protein': (10, 35),
        'Fat': (20, 35)
    }
    
    # Create necessary folders
    @staticmethod
    def init_app(app):
        """Initialize application folders"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.REPORTS_FOLDER, exist_ok=True)
        os.makedirs(Config.CHART_EXPORT_PATH, exist_ok=True)
