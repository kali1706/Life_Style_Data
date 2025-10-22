# Deployment Guide - Lifestyle Analytics

This guide covers deploying your Lifestyle Analytics application to various platforms.

## 🚀 **Quick Deployment**

### **For Render.com (Recommended)**
```bash
# 1. Run deployment setup
python setup_database_deployment.py

# 2. Deploy to Render
git add .
git commit -m "Deploy to Render"
git push origin main
```

## 📋 **Platform Support**

### **Windows (Local Development)**
- **Database**: SQL Server (AYUSH\SQLEXPRESS)
- **Driver**: pyodbc
- **Setup**: `python setup_database_unified.py`

### **Linux (Deployment)**
- **Database**: PostgreSQL
- **Driver**: psycopg2-binary
- **Setup**: `python setup_database_deployment.py`

### **Fallback**
- **Database**: MySQL
- **Driver**: PyMySQL
- **Setup**: `python setup_database.py`

## 🔧 **Environment Variables**

### **For Render.com**
Set these in your Render dashboard:

```bash
# Database Configuration
DATABASE_TYPE=postgresql
POSTGRES_HOST=your-postgres-host
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DATABASE=lifestyle_analytics

# Application Configuration
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

### **For Heroku**
```bash
# Database Configuration
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:pass@host:port/db

# Application Configuration
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

### **For Railway**
```bash
# Database Configuration
DATABASE_TYPE=postgresql
POSTGRES_HOST=your-postgres-host
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DATABASE=lifestyle_analytics

# Application Configuration
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

## 📁 **Deployment Files**

### **requirements.txt**
- Cross-platform dependencies
- Platform-specific drivers
- No pyodbc on Linux (fixes deployment error)

### **database_config.py**
- Auto-detects platform
- Uses appropriate database
- Fallback to SQLite

### **setup_database_deployment.py**
- Installs correct dependencies
- Sets up appropriate database
- Generates configuration

## 🛠️ **Deployment Steps**

### **1. Prepare for Deployment**
```bash
# Install deployment dependencies
pip install -r requirements.txt

# Run deployment setup
python setup_database_deployment.py
```

### **2. Configure Environment Variables**
Set the appropriate environment variables for your platform.

### **3. Deploy**
```bash
# Commit changes
git add .
git commit -m "Deploy application"

# Push to your deployment platform
git push origin main
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. pyodbc Error on Linux**
- **Problem**: pyodbc doesn't work on Linux
- **Solution**: Use PostgreSQL instead
- **Fix**: Set `DATABASE_TYPE=postgresql`

#### **2. Database Connection Failed**
- **Problem**: Wrong database credentials
- **Solution**: Check environment variables
- **Fix**: Verify all required variables are set

#### **3. Dependencies Missing**
- **Problem**: Platform-specific packages not installed
- **Solution**: Use deployment setup script
- **Fix**: Run `python setup_database_deployment.py`

### **Platform-Specific Issues**

#### **Render.com**
- Use PostgreSQL database
- Set all environment variables
- Check build logs for errors

#### **Heroku**
- Use Heroku Postgres addon
- Set DATABASE_URL environment variable
- Check Heroku logs

#### **Railway**
- Use Railway PostgreSQL
- Set PostgreSQL environment variables
- Check Railway logs

## 📊 **Database Schemas**

### **SQL Server (Windows)**
- File: `database_schema_sqlserver.sql`
- Driver: pyodbc
- Authentication: Windows

### **PostgreSQL (Linux)**
- File: `database_schema_postgresql.sql`
- Driver: psycopg2-binary
- Authentication: Username/Password

### **MySQL (Fallback)**
- File: `database_schema.sql`
- Driver: PyMySQL
- Authentication: Username/Password

## 🎯 **Your Current Setup**

### **Local Development (Windows)**
- ✅ SQL Server: AYUSH\SQLEXPRESS
- ✅ Driver: pyodbc
- ✅ Authentication: Windows
- ✅ Status: Working

### **Deployment (Linux)**
- ✅ Database: PostgreSQL
- ✅ Driver: psycopg2-binary
- ✅ Authentication: Environment variables
- ✅ Status: Ready for deployment

## 🚀 **Ready to Deploy!**

Your application is now ready for deployment on any platform:

1. **Local**: Use SQL Server (Windows)
2. **Deployment**: Use PostgreSQL (Linux)
3. **Fallback**: Use MySQL (Any platform)

The deployment error with pyodbc is now fixed! 🎉

