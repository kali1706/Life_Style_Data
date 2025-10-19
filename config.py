import os
from datetime import timedelta

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///lifestyle_analytics.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Email configuration (for reports)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Report configuration
    UPLOAD_FOLDER = 'reports'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size