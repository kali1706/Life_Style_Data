# Unified Database Configuration for Lifestyle Analytics
# Supports both MySQL and SQL Server

import os
from urllib.parse import quote_plus

class DatabaseConfig:
    """
    Unified database configuration supporting MySQL and SQL Server
    """
    
    # Database Type Selection
    DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlserver')  # 'mysql' or 'sqlserver'
    
    # MySQL Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USERNAME = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'lifestyle_analytics')
    
    # SQL Server Configuration
    SQL_SERVER_HOST = os.environ.get('SQL_SERVER_HOST', 'AYUSH\\SQLEXPRESS')
    SQL_SERVER_PORT = int(os.environ.get('SQL_SERVER_PORT', 1433))
    SQL_SERVER_DATABASE = os.environ.get('SQL_SERVER_DATABASE', 'lifestyle_analytics')
    SQL_SERVER_DRIVER = os.environ.get('SQL_SERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
    SQL_SERVER_AUTHENTICATION = os.environ.get('SQL_SERVER_AUTH', 'Windows')
    SQL_SERVER_USERNAME = os.environ.get('SQL_SERVER_USER', '')
    SQL_SERVER_PASSWORD = os.environ.get('SQL_SERVER_PASSWORD', '')
    
    @classmethod
    def get_database_url(cls):
        """Generate SQLAlchemy database URL based on selected database type"""
        
        if cls.DATABASE_TYPE.lower() == 'mysql':
            return cls._get_mysql_url()
        elif cls.DATABASE_TYPE.lower() == 'sqlserver':
            return cls._get_sqlserver_url()
        else:
            raise ValueError(f"Unsupported database type: {cls.DATABASE_TYPE}")
    
    @classmethod
    def _get_mysql_url(cls):
        """Generate MySQL database URL"""
        password = quote_plus(cls.MYSQL_PASSWORD) if cls.MYSQL_PASSWORD else ''
        return f"mysql+pymysql://{cls.MYSQL_USERNAME}:{password}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
    
    @classmethod
    def _get_sqlserver_url(cls):
        """Generate SQL Server database URL"""
        # Use server name without port for SQL Server
        server = cls.SQL_SERVER_HOST
        
        if cls.SQL_SERVER_AUTHENTICATION.lower() == 'windows':
            # Use proper format for Windows Authentication
            return f"mssql+pyodbc://@{server}/{cls.SQL_SERVER_DATABASE}?driver={quote_plus(cls.SQL_SERVER_DRIVER)}&trusted_connection=yes&encrypt=yes&trustservercertificate=yes"
        else:
            username = quote_plus(cls.SQL_SERVER_USERNAME)
            password = quote_plus(cls.SQL_SERVER_PASSWORD)
            return f"mssql+pyodbc://{username}:{password}@{server}/{cls.SQL_SERVER_DATABASE}?driver={quote_plus(cls.SQL_SERVER_DRIVER)}&encrypt=yes&trustservercertificate=yes"
    
    @classmethod
    def get_connection_params(cls):
        """Get connection parameters for direct database connections"""
        
        if cls.DATABASE_TYPE.lower() == 'mysql':
            return {
                'host': cls.MYSQL_HOST,
                'port': cls.MYSQL_PORT,
                'user': cls.MYSQL_USERNAME,
                'password': cls.MYSQL_PASSWORD,
                'database': cls.MYSQL_DATABASE,
                'charset': 'utf8mb4',
                'autocommit': True
            }
        elif cls.DATABASE_TYPE.lower() == 'sqlserver':
            return {
                'server': cls.SQL_SERVER_HOST,
                'port': cls.SQL_SERVER_PORT,
                'database': cls.SQL_SERVER_DATABASE,
                'driver': cls.SQL_SERVER_DRIVER,
                'trusted_connection': cls.SQL_SERVER_AUTHENTICATION.lower() == 'windows',
                'encrypt': True,
                'trust_server_certificate': True
            }
        else:
            raise ValueError(f"Unsupported database type: {cls.DATABASE_TYPE}")

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
    """SQL Server-specific configuration"""
    DATABASE_TYPE = 'sqlserver'
    SQL_SERVER_HOST = 'AYUSH\\SQLEXPRESS'
    SQL_SERVER_PORT = 1433
    SQL_SERVER_DATABASE = 'lifestyle_analytics'
    SQL_SERVER_DRIVER = 'ODBC Driver 17 for SQL Server'
    SQL_SERVER_AUTHENTICATION = 'Windows'

# Instructions for usage:
"""
USAGE EXAMPLES:

1. For MySQL:
   from database_config import MySQLConfig
   SQLALCHEMY_DATABASE_URI = MySQLConfig.get_database_url()

2. For SQL Server:
   from database_config import SQLServerConfig
   SQLALCHEMY_DATABASE_URI = SQLServerConfig.get_database_url()

3. Using environment variables:
   export DATABASE_TYPE=sqlserver  # or mysql
   from database_config import DatabaseConfig
   SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_url()

4. Custom configuration:
   class CustomConfig(DatabaseConfig):
       DATABASE_TYPE = 'mysql'
       MYSQL_HOST = 'your-mysql-server'
       MYSQL_USERNAME = 'your-username'
       MYSQL_PASSWORD = 'your-password'
"""

