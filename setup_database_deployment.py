#!/usr/bin/env python3
"""
Deployment Database Setup Script for Lifestyle Analytics
Automatically detects platform and sets up appropriate database
"""

import os
import sys
import subprocess

def detect_platform():
    """Detect the current platform"""
    if sys.platform == "win32":
        return "windows"
    elif sys.platform.startswith("linux"):
        return "linux"
    else:
        return "other"

def install_dependencies():
    """Install platform-specific dependencies"""
    platform = detect_platform()
    
    print(f"Detected platform: {platform}")
    print("Installing dependencies...")
    
    if platform == "windows":
        # Install Windows-specific packages
        packages = ["PyMySQL", "pyodbc"]
    elif platform == "linux":
        # Install Linux-specific packages
        packages = ["psycopg2-binary"]
    else:
        # Install fallback packages
        packages = ["PyMySQL"]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")

def setup_database():
    """Set up database based on platform"""
    platform = detect_platform()
    
    print(f"\nSetting up database for {platform}...")
    
    if platform == "windows":
        # Use SQL Server setup
        try:
            from setup_database_sqlserver import main as sqlserver_main
            return sqlserver_main()
        except ImportError:
            print("SQL Server setup not available, using MySQL...")
            from setup_database import main as mysql_main
            return mysql_main()
    
    elif platform == "linux":
        # Use PostgreSQL setup
        return setup_postgresql()
    
    else:
        # Use MySQL setup
        try:
            from setup_database import main as mysql_main
            return mysql_main()
        except ImportError:
            print("MySQL setup not available, using SQLite...")
            return True

def setup_postgresql():
    """Set up PostgreSQL database"""
    print("Setting up PostgreSQL database...")
    
    # Check if we have PostgreSQL connection details
    postgres_host = os.environ.get('POSTGRES_HOST')
    postgres_user = os.environ.get('POSTGRES_USER')
    postgres_password = os.environ.get('POSTGRES_PASSWORD')
    postgres_db = os.environ.get('POSTGRES_DATABASE', 'lifestyle_analytics')
    
    if not all([postgres_host, postgres_user, postgres_password]):
        print("⚠️ PostgreSQL environment variables not set.")
        print("Please set the following environment variables:")
        print("  POSTGRES_HOST=your-postgres-host")
        print("  POSTGRES_USER=your-username")
        print("  POSTGRES_PASSWORD=your-password")
        print("  POSTGRES_DATABASE=lifestyle_analytics")
        return False
    
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=postgres_host,
            user=postgres_user,
            password=postgres_password,
            database='postgres'  # Connect to default database first
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{postgres_db}'")
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {postgres_db}")
                print(f"✓ Created database '{postgres_db}'")
            else:
                print(f"✓ Database '{postgres_db}' already exists")
        
        conn.close()
        
        # Now connect to the specific database and create tables
        conn = psycopg2.connect(
            host=postgres_host,
            user=postgres_user,
            password=postgres_password,
            database=postgres_db
        )
        
        with conn.cursor() as cursor:
            # Read and execute SQL schema
            schema_file = 'database_schema_postgresql.sql'
            if os.path.exists(schema_file):
                with open(schema_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Execute SQL statements
                cursor.execute(sql_content)
                print("✓ Database tables created successfully")
            else:
                print(f"⚠️ Schema file '{schema_file}' not found")
        
        conn.commit()
        conn.close()
        
        print("✓ PostgreSQL setup completed successfully!")
        return True
        
    except ImportError:
        print("✗ psycopg2 not installed. Please install it first:")
        print("  pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"✗ PostgreSQL setup failed: {e}")
        return False

def generate_config():
    """Generate configuration file"""
    print("\nGenerating configuration file...")
    
    platform = detect_platform()
    
    config_content = f"""# Database Configuration - Generated by setup_database_deployment.py
import os

# Set database type based on platform
os.environ['DATABASE_TYPE'] = '{platform}'

# Import the unified configuration
from database_config import DatabaseConfig

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lifestyle-analytics-secret-key-2024'
    
    # Email configuration (add your details)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# Platform: {platform.upper()}
# Generated automatically by setup_database_deployment.py
"""
    
    with open('database_config_generated.py', 'w') as f:
        f.write(config_content)
    
    print("✓ Configuration file 'database_config_generated.py' created!")
    return True

def main():
    """Main setup function"""
    try:
        print("Deployment Database Setup for Lifestyle Analytics")
        print("=" * 60)
        
        # Install dependencies
        install_dependencies()
        
        # Setup database
        if not setup_database():
            return False
        
        # Generate configuration
        if not generate_config():
            return False
        
        print("\n" + "=" * 60)
        print("Setup Completed Successfully!")
        print("=" * 60)
        print(f"Platform: {detect_platform().upper()}")
        print("Configuration: database_config_generated.py")
        print()
        print("Next Steps:")
        print("1. Update your config.py to use the generated configuration")
        print("2. Test your application")
        print("3. Deploy your application!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

