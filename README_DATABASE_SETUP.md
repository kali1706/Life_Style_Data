# Database Setup Guide - Lifestyle Analytics

This guide will help you set up a MySQL database for your Lifestyle Analytics application.

## 🎯 What You Need to Provide

### Required Server Details:

1. **MySQL Host** - IP address or domain name of your MySQL server
   - Local: `localhost` or `127.0.0.1`
   - Remote: Your server's IP address or domain name
   - Cloud: Your cloud database endpoint

2. **MySQL Port** - Usually `3306` (default MySQL port)

3. **MySQL Username** - Your MySQL user account
   - Local: Usually `root`
   - Remote: Your database username

4. **MySQL Password** - Your MySQL user password

5. **Database Name** - `lifestyle_analytics` (recommended)

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup_database.py
```
This script will:
- Ask for your MySQL server details
- Test the connection
- Create the database and all tables
- Generate a configuration file

### Option 2: Manual Setup
1. Run the SQL schema file:
```bash
mysql -u your_username -p < database_schema.sql
```

2. Update your `config.py` with your database details

## 📋 Common Server Scenarios

### Local Development (XAMPP/WAMP)
```python
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = ''  # Usually empty for local
```

### Remote VPS/Server
```python
MYSQL_HOST = 'your-server-ip-address'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'your_database_user'
MYSQL_PASSWORD = 'your_password'
```

### AWS RDS
```python
MYSQL_HOST = 'your-rds-endpoint.region.rds.amazonaws.com'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_SSL_DISABLED = False  # SSL required
```

### Google Cloud SQL
```python
MYSQL_HOST = 'your-instance-ip'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_SSL_DISABLED = False  # SSL required
```

### Shared Hosting (cPanel)
```python
MYSQL_HOST = 'localhost'  # Usually localhost on shared hosting
MYSQL_PORT = 3306
MYSQL_USERNAME = 'your_cpanel_username'
MYSQL_PASSWORD = 'your_database_password'
```

## 🔧 Configuration Files

### 1. Update config.py
```python
from database_config_generated import Config

# Use the generated configuration
SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
```

### 2. Environment Variables (Optional)
You can also set these as environment variables:
```bash
export MYSQL_HOST=your_host
export MYSQL_USER=your_username
export MYSQL_PASSWORD=your_password
export MYSQL_PORT=3306
```

## 📊 Database Schema

The database includes these tables:
- **users** - User accounts and profiles
- **exercises** - Reference table of exercises
- **workout_logs** - User workout sessions
- **exercise_logs** - Individual exercises in workouts
- **nutrition_logs** - Daily nutrition tracking
- **meals** - Individual meal records
- **daily_stats** - Daily summary statistics
- **reports** - Generated reports

## 🔍 Testing Your Setup

### Test Database Connection
```python
from models import db, User
from app import app

with app.app_context():
    # Test connection
    users = User.query.all()
    print(f"Connected! Found {len(users)} users.")
```

### Test with MySQL Command Line
```bash
mysql -u your_username -p -h your_host
USE lifestyle_analytics;
SHOW TABLES;
```

## 🛠️ Troubleshooting

### Connection Refused
- Check if MySQL server is running
- Verify host and port
- Check firewall settings

### Access Denied
- Verify username and password
- Check user permissions
- Ensure user has CREATE DATABASE privileges

### SSL Errors
- Set `MYSQL_SSL_DISABLED = False` for cloud databases
- Provide SSL certificates if required

### Character Encoding Issues
- Database uses UTF8MB4 encoding
- Ensure your MySQL server supports UTF8MB4

## 📞 Support

If you encounter issues:
1. Check MySQL server logs
2. Verify network connectivity
3. Test with MySQL command line client
4. Check user permissions and privileges

## 🔒 Security Notes

- Never commit passwords to version control
- Use environment variables for sensitive data
- Enable SSL for remote connections
- Use strong passwords
- Limit database user privileges

## 📁 Files Created

After setup, you'll have:
- `database_schema.sql` - Complete database schema
- `setup_database.py` - Automated setup script
- `database_config_generated.py` - Your configuration file
- `database_config_template.py` - Template for custom configs
