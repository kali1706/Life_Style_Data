# Database Configuration Template
# Copy this file to database_config.py and fill in your actual server details

import os
from urllib.parse import quote_plus

class DatabaseConfig:
    """
    Database configuration template for MySQL server
    Fill in your actual server details below
    """
    
    # MySQL Server Details - FILL THESE IN
    MYSQL_HOST = 'localhost'  # Your MySQL server host/IP address
    MYSQL_PORT = 3306         # Your MySQL server port (default: 3306)
    MYSQL_USERNAME = 'root'   # Your MySQL username
    MYSQL_PASSWORD = ''       # Your MySQL password
    MYSQL_DATABASE = 'lifestyle_analytics'  # Database name
    
    # Connection Pool Settings
    MYSQL_POOL_SIZE = 10
    MYSQL_MAX_OVERFLOW = 20
    MYSQL_POOL_TIMEOUT = 30
    MYSQL_POOL_RECYCLE = 3600
    
    # SSL Settings (if required)
    MYSQL_SSL_DISABLED = True  # Set to False if SSL is required
    MYSQL_SSL_CA = None        # Path to SSL CA certificate if needed
    MYSQL_SSL_CERT = None      # Path to SSL client certificate if needed
    MYSQL_SSL_KEY = None       # Path to SSL client key if needed
    
    @classmethod
    def get_database_url(cls):
        """Generate SQLAlchemy database URL"""
        # URL encode password to handle special characters
        password = quote_plus(cls.MYSQL_PASSWORD) if cls.MYSQL_PASSWORD else ''
        
        # Build connection string
        connection_string = f"mysql+pymysql://{cls.MYSQL_USERNAME}:{password}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
        
        # Add SSL parameters if needed
        if not cls.MYSQL_SSL_DISABLED:
            ssl_params = []
            if cls.MYSQL_SSL_CA:
                ssl_params.append(f"ssl_ca={cls.MYSQL_SSL_CA}")
            if cls.MYSQL_SSL_CERT:
                ssl_params.append(f"ssl_cert={cls.MYSQL_SSL_CERT}")
            if cls.MYSQL_SSL_KEY:
                ssl_params.append(f"ssl_key={cls.MYSQL_SSL_KEY}")
            
            if ssl_params:
                connection_string += "?" + "&".join(ssl_params)
        
        return connection_string
    
    @classmethod
    def get_connection_params(cls):
        """Get connection parameters for direct MySQL connections"""
        return {
            'host': cls.MYSQL_HOST,
            'port': cls.MYSQL_PORT,
            'user': cls.MYSQL_USERNAME,
            'password': cls.MYSQL_PASSWORD,
            'database': cls.MYSQL_DATABASE,
            'charset': 'utf8mb4',
            'autocommit': True
        }

# Example configurations for different environments

class LocalDatabaseConfig(DatabaseConfig):
    """Local development configuration"""
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = ''  # Add your local MySQL password
    MYSQL_DATABASE = 'lifestyle_analytics'

class RemoteDatabaseConfig(DatabaseConfig):
    """Remote server configuration"""
    MYSQL_HOST = 'your-server-ip-or-domain.com'
    MYSQL_PORT = 3306
    MYSQL_USERNAME = 'your_username'
    MYSQL_PASSWORD = 'your_password'
    MYSQL_DATABASE = 'lifestyle_analytics'

class CloudDatabaseConfig(DatabaseConfig):
    """Cloud database configuration (AWS RDS, Google Cloud SQL, etc.)"""
    MYSQL_HOST = 'your-cloud-instance.amazonaws.com'
    MYSQL_PORT = 3306
    MYSQL_USERNAME = 'your_username'
    MYSQL_PASSWORD = 'your_password'
    MYSQL_DATABASE = 'lifestyle_analytics'
    MYSQL_SSL_DISABLED = False  # Usually required for cloud databases

# Instructions for setting up your database configuration:
"""
STEP 1: Copy this file to database_config.py
STEP 2: Fill in your MySQL server details above
STEP 3: Update your config.py to use the database URL

Example config.py update:
from database_config import LocalDatabaseConfig
SQLALCHEMY_DATABASE_URI = LocalDatabaseConfig.get_database_url()

Required Server Details:
1. MySQL Host: IP address or domain name of your MySQL server
2. MySQL Port: Usually 3306 (default MySQL port)
3. MySQL Username: Your MySQL user account
4. MySQL Password: Your MySQL user password
5. Database Name: 'lifestyle_analytics' (or your preferred name)
6. SSL Settings: If your server requires SSL connections

Common MySQL Server Scenarios:
- Local XAMPP/WAMP: host='localhost', port=3306, username='root'
- Remote VPS: host='your-vps-ip', port=3306, username='your_user'
- AWS RDS: host='your-rds-endpoint', port=3306, SSL required
- Google Cloud SQL: host='your-instance-ip', port=3306, SSL required
- Shared Hosting: host='your-host-domain', port=3306, username='your_cpanel_user'
"""
