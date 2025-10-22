# Database Setup Guide - Lifestyle Analytics

This guide covers database setup for both **MySQL** and **SQL Server** databases.

## 🚀 **Quick Start**

### **Option 1: Unified Setup (Recommended)**
```bash
python setup_database_unified.py
```
This script will:
- Detect available database drivers
- Let you choose between MySQL and SQL Server
- Run the appropriate setup automatically
- Generate a unified configuration file

### **Option 2: Manual Setup**

#### **For MySQL:**
```bash
python setup_database.py
```

#### **For SQL Server:**
```bash
python setup_database_sqlserver.py
```

## 📋 **Database Requirements**

### **MySQL Setup**
- **Driver**: PyMySQL
- **Install**: `pip install PyMySQL`
- **Default Host**: localhost:3306
- **Authentication**: Username/Password

### **SQL Server Setup**
- **Driver**: PyODBC
- **Install**: `pip install pyodbc`
- **Default Host**: AYUSH\SQLEXPRESS:1433
- **Authentication**: Windows or SQL Server

## 🔧 **Configuration**

### **Using Unified Configuration**
```python
# In your config.py
from database_config import SQLServerConfig  # or MySQLConfig
SQLALCHEMY_DATABASE_URI = SQLServerConfig.get_database_url()
```

### **Using Environment Variables**
```bash
# Set database type
export DATABASE_TYPE=sqlserver  # or mysql

# MySQL specific
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password

# SQL Server specific
export SQL_SERVER_HOST=AYUSH\\SQLEXPRESS
export SQL_SERVER_DATABASE=lifestyle_analytics
```

## 📊 **Database Schema**

Both MySQL and SQL Server versions include:
- **users** - User accounts and profiles
- **exercises** - Reference table of exercises
- **workout_logs** - User workout sessions
- **exercise_logs** - Individual exercises in workouts
- **nutrition_logs** - Daily nutrition tracking
- **meals** - Individual meal records
- **daily_stats** - Daily summary statistics
- **reports** - Generated reports

## 🔍 **Testing Your Setup**

### **Test Database Connection**
```python
from database_config import DatabaseConfig
from models import db, User
from app import create_app

# Test connection
app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Connected! Found {len(users)} users.")
```

## 🛠️ **Troubleshooting**

### **MySQL Issues**
- **Connection Refused**: Check if MySQL server is running
- **Access Denied**: Verify username and password
- **Driver Not Found**: Install PyMySQL

### **SQL Server Issues**
- **ODBC Driver Not Found**: Install "ODBC Driver 17 for SQL Server"
- **Login Failed**: Check Windows Authentication
- **Cannot Connect**: Verify server name and service status

## 📁 **File Structure**

```
├── database_config.py              # Unified configuration
├── setup_database_unified.py       # Unified setup script
├── setup_database.py              # MySQL setup script
├── setup_database_sqlserver.py    # SQL Server setup script
├── database_schema.sql            # MySQL schema
├── database_schema_sqlserver.sql  # SQL Server schema
└── README_DATABASE.md             # This file
```

## 🎯 **Your SQL Server Connection**

Based on your connection string:
```
Data Source=AYUSH\SQLEXPRESS;Integrated Security=True;Encrypt=True;TrustServerCertificate=True
```

**Recommended Setup:**
1. Run: `python setup_database_unified.py`
2. Choose option 2 (SQL Server)
3. Your database will be created automatically!

## 🔒 **Security Notes**

- **MySQL**: Use strong passwords, enable SSL for remote connections
- **SQL Server**: Windows Authentication is more secure than SQL Server auth
- **Both**: Enable encryption for production environments

## 📞 **Support**

If you encounter issues:
1. Check database server is running
2. Verify driver installation
3. Test connection with database management tools
4. Check firewall and network settings

## 🎉 **Ready to Use!**

Your database setup supports both MySQL and SQL Server. Choose the one that works best for your environment and follow the setup instructions above!

