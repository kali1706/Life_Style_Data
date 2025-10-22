#!/usr/bin/env python3
"""
SQL Server Database Setup Script for Lifestyle Analytics
This script will create the database and all required tables.
"""

import pyodbc
import os
import sys
from urllib.parse import quote_plus

def get_sqlserver_config():
    """Get SQL Server configuration from user input or environment variables"""
    
    print("SQL Server Database Setup for Lifestyle Analytics")
    print("=" * 50)
    
    # Try to get from environment variables first
    server = os.environ.get('SQL_SERVER_HOST')
    database = os.environ.get('SQL_SERVER_DATABASE')
    driver = os.environ.get('SQL_SERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
    auth_type = os.environ.get('SQL_SERVER_AUTH', 'Windows')
    
    if not server:
        print("\nPlease provide your SQL Server details:")
        server = input("SQL Server Host (default: AYUSH\\SQLEXPRESS): ").strip() or 'AYUSH\\SQLEXPRESS'
    
    if not database:
        database = input("Database Name (default: lifestyle_analytics): ").strip() or 'lifestyle_analytics'
    
    if not driver:
        driver = input("ODBC Driver (default: ODBC Driver 17 for SQL Server): ").strip() or 'ODBC Driver 17 for SQL Server'
    
    if not auth_type:
        auth_type = input("Authentication (Windows/SQL Server, default: Windows): ").strip() or 'Windows'
    
    username = None
    password = None
    
    if auth_type.lower() == 'sql server':
        username = input("Username: ").strip()
        password = input("Password: ").strip()
    
    return {
        'server': server,
        'database': database,
        'driver': driver,
        'auth_type': auth_type,
        'username': username,
        'password': password
    }

def test_connection(config):
    """Test SQL Server connection"""
    try:
        print(f"\nTesting connection to {config['server']}...")
        
        # Build connection string
        if config['auth_type'].lower() == 'windows':
            conn_str = f"DRIVER={{{config['driver']}}};SERVER={config['server']};DATABASE=master;Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes"
        else:
            conn_str = f"DRIVER={{{config['driver']}}};SERVER={config['server']};DATABASE=master;UID={config['username']};PWD={config['password']};Encrypt=yes;TrustServerCertificate=yes"
        
        connection = pyodbc.connect(conn_str)
        print("Connection successful!")
        return connection
    except pyodbc.Error as e:
        print(f"Connection failed: {e}")
        return None

def create_database_and_tables(connection, config):
    """Create database and all tables"""
    try:
        with connection.cursor() as cursor:
            # Create database
            print(f"\nCreating database '{config['database']}'...")
            cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{config['database']}') BEGIN CREATE DATABASE {config['database']}; END")
            print("Database created successfully!")
            
            # Use the database
            cursor.execute(f"USE {config['database']}")
            
            # Read and execute SQL schema
            print("\nCreating tables...")
            schema_file = 'database_schema_sqlserver.sql'
            
            if os.path.exists(schema_file):
                with open(schema_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Split SQL content by GO statements and execute each batch
                batches = [batch.strip() for batch in sql_content.split('GO') if batch.strip()]
                
                for i, batch in enumerate(batches):
                    if batch.upper().startswith(('CREATE', 'INSERT', 'ALTER', 'DROP')):
                        try:
                            cursor.execute(batch)
                            print(f"Executed batch {i+1}/{len(batches)}")
                        except pyodbc.Error as e:
                            print(f"Warning on batch {i+1}: {e}")
            else:
                print(f"Schema file '{schema_file}' not found!")
                return False
            
            print("All tables created successfully!")
            
        connection.commit()
        return True
        
    except pyodbc.Error as e:
        print(f"Error creating database/tables: {e}")
        return False

def generate_config_file(config):
    """Generate configuration file for the application"""
    print("\nGenerating configuration file...")
    
    # Generate database URL
    if config['auth_type'].lower() == 'windows':
        database_url = f"mssql+pyodbc://@{config['server']}/{config['database']}?driver={quote_plus(config['driver'])}&trusted_connection=yes&encrypt=yes&trustservercertificate=yes"
    else:
        username = quote_plus(config['username'])
        password = quote_plus(config['password'])
        database_url = f"mssql+pyodbc://{username}:{password}@{config['server']}/{config['database']}?driver={quote_plus(config['driver'])}&encrypt=yes&trustservercertificate=yes"
    
    config_content = f"""# Database Configuration - Generated by setup_database_sqlserver.py
import os

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = '{database_url}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lifestyle-analytics-secret-key-2024'
    
    # Email configuration (add your details)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# SQL Server Connection Details:
# Server: {config['server']}
# Database: {config['database']}
# Driver: {config['driver']}
# Authentication: {config['auth_type']}
"""
    
    with open('database_config_generated_sqlserver.py', 'w') as f:
        f.write(config_content)
    
    print("Configuration file 'database_config_generated_sqlserver.py' created!")
    return database_url

def main():
    """Main setup function"""
    try:
        # Get SQL Server configuration
        config = get_sqlserver_config()
        
        # Test connection
        connection = test_connection(config)
        if not connection:
            return False
        
        # Create database and tables
        if not create_database_and_tables(connection, config):
            return False
        
        # Generate configuration file
        database_url = generate_config_file(config)
        
        print("\nDatabase setup completed successfully!")
        print("=" * 50)
        print("Summary:")
        print(f"   • Database: {config['database']}")
        print(f"   • Server: {config['server']}")
        print(f"   • Driver: {config['driver']}")
        print(f"   • Authentication: {config['auth_type']}")
        print(f"   • Connection URL: {database_url}")
        print("\nNext Steps:")
        print("1. Update your config.py to use the generated database URL")
        print("2. Test your application connection")
        print("3. Start using your lifestyle analytics app!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
