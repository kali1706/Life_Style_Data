# Cross-Platform Database Configuration for Lifestyle Analytics
# Supports SQL Server (Windows), PostgreSQL (Linux/Deployment), and MySQL

import os
import sys
from urllib.parse import quote_plus

class DatabaseConfig:
    """
    Cross-platform database configuration
    - Windows: SQL Server (local development)
    - Linux: PostgreSQL (deployment)
    - Fallback: MySQL
    """
    
    # Auto-detect platform and database type
    @classmethod
    def get_platform(cls):
        """Detect the current platform"""
        if sys.platform == "win32":
            return "windows"
        elif sys.platform.startswith("linux"):
            return "linux"
        else:
            return "other"
    
    @classmethod
    def get_database_type(cls):
        """Get database type based on platform and environment"""
        platform = cls.get_platform()
        
        # Check environment variable first (for deployment)
        env_db_type = os.environ.get('DATABASE_TYPE', '').lower()
        if env_db_type in ['sqlserver', 'postgresql', 'mysql']:
            return env_db_type
        
        # Check for Render.com environment variables
        if os.environ.get('RENDER'):
            return "postgresql"
        
        # Auto-detect based on platform
        if platform == "windows":
            return "sqlserver"
        elif platform == "linux":
            return "postgresql"
        else:
            return "mysql"
    
    # MySQL Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USERNAME = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'lifestyle_analytics')
    
    # SQL Server Configuration (Windows)
    SQL_SERVER_HOST = os.environ.get('SQL_SERVER_HOST', 'AYUSH\\SQLEXPRESS')
    SQL_SERVER_PORT = int(os.environ.get('SQL_SERVER_PORT', 1433))
    SQL_SERVER_DATABASE = os.environ.get('SQL_SERVER_DATABASE', 'lifestyle_analytics')
    SQL_SERVER_DRIVER = os.environ.get('SQL_SERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
    SQL_SERVER_AUTHENTICATION = os.environ.get('SQL_SERVER_AUTH', 'Windows')
    SQL_SERVER_USERNAME = os.environ.get('SQL_SERVER_USER', '')
    SQL_SERVER_PASSWORD = os.environ.get('SQL_SERVER_PASSWORD', '')
    
    # PostgreSQL Configuration (Linux/Deployment)
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', os.environ.get('DATABASE_URL', 'localhost').split('@')[1].split(':')[0] if '@' in os.environ.get('DATABASE_URL', '') else 'localhost')
    POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
    POSTGRES_USERNAME = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
    POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE', 'lifestyle_analytics')
    
    @classmethod
    def get_database_url(cls):
        """Generate SQLAlchemy database URL based on detected database type"""
        
        db_type = cls.get_database_type().lower()
        
        if db_type == 'mysql':
            return cls._get_mysql_url()
        elif db_type == 'sqlserver':
            return cls._get_sqlserver_url()
        elif db_type == 'postgresql':
            return cls._get_postgresql_url()
        else:
            # Fallback to SQLite for development
            return 'sqlite:///instance/lifestyle_analytics.db'
    
    @classmethod
    def _get_mysql_url(cls):
        """Generate MySQL database URL"""
        password = quote_plus(cls.MYSQL_PASSWORD) if cls.MYSQL_PASSWORD else ''
        return f"mysql+pymysql://{cls.MYSQL_USERNAME}:{password}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
    
    @classmethod
    def _get_sqlserver_url(cls):
        """Generate SQL Server database URL (Windows only)"""
        server = cls.SQL_SERVER_HOST
        
        if cls.SQL_SERVER_AUTHENTICATION.lower() == 'windows':
            return f"mssql+pyodbc://@{server}/{cls.SQL_SERVER_DATABASE}?driver={quote_plus(cls.SQL_SERVER_DRIVER)}&trusted_connection=yes&encrypt=yes&trustservercertificate=yes"
        else:
            username = quote_plus(cls.SQL_SERVER_USERNAME)
            password = quote_plus(cls.SQL_SERVER_PASSWORD)
            return f"mssql+pyodbc://{username}:{password}@{server}/{cls.SQL_SERVER_DATABASE}?driver={quote_plus(cls.SQL_SERVER_DRIVER)}&encrypt=yes&trustservercertificate=yes"
    
    @classmethod
    def _get_postgresql_url(cls):
        """Generate PostgreSQL database URL (Linux/Deployment)"""
        # Check if DATABASE_URL is provided (common in deployment platforms)
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # Normalize to psycopg3 driver URL for SQLAlchemy
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
            elif database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
            return database_url
        
        # Fallback to individual components
        username = quote_plus(cls.POSTGRES_USERNAME)
        password = quote_plus(cls.POSTGRES_PASSWORD)
        return f"postgresql+psycopg://{username}:{password}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DATABASE}"
    
    @classmethod
    def get_connection_params(cls):
        """Get connection parameters for direct database connections"""
        
        db_type = cls.get_database_type().lower()
        
        if db_type == 'mysql':
            return {
                'host': cls.MYSQL_HOST,
                'port': cls.MYSQL_PORT,
                'user': cls.MYSQL_USERNAME,
                'password': cls.MYSQL_PASSWORD,
                'database': cls.MYSQL_DATABASE,
                'charset': 'utf8mb4',
                'autocommit': True
            }
        elif db_type == 'sqlserver':
            return {
                'server': cls.SQL_SERVER_HOST,
                'port': cls.SQL_SERVER_PORT,
                'database': cls.SQL_SERVER_DATABASE,
                'driver': cls.SQL_SERVER_DRIVER,
                'trusted_connection': cls.SQL_SERVER_AUTHENTICATION.lower() == 'windows',
                'encrypt': True,
                'trust_server_certificate': True
            }
        elif db_type == 'postgresql':
            return {
                'host': cls.POSTGRES_HOST,
                'port': cls.POSTGRES_PORT,
                'user': cls.POSTGRES_USERNAME,
                'password': cls.POSTGRES_PASSWORD,
                'database': cls.POSTGRES_DATABASE
            }
        else:
            return {}

# Predefined configurations for easy use

class MySQLConfig(DatabaseConfig):
    """MySQL-specific configuration"""
    DATABASE_TYPE = 'mysql'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DATABASE = 'lifestyle_analytics'

class SQLServerConfig(DatabaseConfig):
    """SQL Server-specific configuration (Windows only)"""
    DATABASE_TYPE = 'sqlserver'
    SQL_SERVER_HOST = 'AYUSH\\SQLEXPRESS'
    SQL_SERVER_PORT = 1433
    SQL_SERVER_DATABASE = 'lifestyle_analytics'
    SQL_SERVER_DRIVER = 'ODBC Driver 17 for SQL Server'
    SQL_SERVER_AUTHENTICATION = 'Windows'

class PostgreSQLConfig(DatabaseConfig):
    """PostgreSQL-specific configuration (Linux/Deployment)"""
    DATABASE_TYPE = 'postgresql'
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PASSWORD = ''
    POSTGRES_DATABASE = 'lifestyle_analytics'

# Instructions for usage:
"""
USAGE EXAMPLES:

1. Automatic detection (recommended):
   from database_config import DatabaseConfig
   SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_url()

2. For specific database:
   from database_config import SQLServerConfig  # or PostgreSQLConfig, MySQLConfig
   SQLALCHEMY_DATABASE_URI = SQLServerConfig.get_database_url()

3. Using environment variables:
   export DATABASE_TYPE=postgresql
   from database_config import DatabaseConfig
   SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_url()

PLATFORM DETECTION:
- Windows: Uses SQL Server (AYUSH\\SQLEXPRESS)
- Linux: Uses PostgreSQL (for deployment)
- Other: Uses MySQL (fallback)

DEPLOYMENT SETUP:
For Render.com or similar platforms, set these environment variables:
- DATABASE_TYPE=postgresql
- POSTGRES_HOST=your-postgres-host
- POSTGRES_USER=your-username
- POSTGRES_PASSWORD=your-password
- POSTGRES_DATABASE=lifestyle_analytics
"""