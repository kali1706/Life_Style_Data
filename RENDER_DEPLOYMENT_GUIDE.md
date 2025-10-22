# 🚀 Render.com Deployment Guide

## Problem Fixed
The original error was:
```
pyodbc.Error: ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'ODBC Driver 17 for SQL Server' : file not found (0) (SQLDriverConnect)")
```

This happened because:
- SQL Server ODBC drivers are not available on Linux (Render.com uses Linux)
- The app was trying to use SQL Server on Linux deployment

## Solution Applied

### 1. Updated Database Configuration
- Modified `database_config.py` to detect Render.com environment
- Auto-switch to PostgreSQL on Linux/Render.com
- Added support for `DATABASE_URL` environment variable

### 2. Updated Requirements
- Added `psycopg2-binary` for PostgreSQL on Linux
- Platform-specific database drivers

### 3. Created Render Configuration
- `render.yaml` for proper service configuration
- PostgreSQL database service included

## Deployment Steps

### Method 1: Using render.yaml (Recommended)
1. Push code to GitHub
2. Connect GitHub repo to Render.com
3. Render will automatically detect `render.yaml`
4. Both web service and PostgreSQL database will be created

### Method 2: Manual Setup
1. Create PostgreSQL database on Render.com
2. Create web service
3. Set environment variables:
   ```
   DATABASE_TYPE=postgresql
   DATABASE_URL=<your-postgres-url>
   FLASK_ENV=production
   SECRET_KEY=<generate-random-key>
   ```

## Environment Variables for Render.com

### Required Variables:
- `DATABASE_TYPE=postgresql`
- `FLASK_ENV=production`
- `SECRET_KEY=<random-string>`

### Database Variables (if not using DATABASE_URL):
- `POSTGRES_HOST=<your-db-host>`
- `POSTGRES_USER=<your-username>`
- `POSTGRES_PASSWORD=<your-password>`
- `POSTGRES_DATABASE=lifestyle_analytics`

## Database Migration

After deployment, you need to create tables:

### Option 1: Using Python Script
```python
from app import create_app
from models import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
```

### Option 2: Using Flask CLI
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Testing Deployment

1. Check if app starts without errors
2. Visit the health check endpoint: `https://your-app.onrender.com/`
3. Test database connection
4. Verify all routes work

## Troubleshooting

### Common Issues:
1. **Port binding error**: Make sure `PORT` environment variable is used
2. **Database connection error**: Check `DATABASE_URL` format
3. **Missing tables**: Run database migration
4. **Import errors**: Check all dependencies are installed

### Debug Commands:
```bash
# Check database connection
python -c "from app import create_app; app = create_app(); print('DB URL:', app.config['SQLALCHEMY_DATABASE_URI'])"

# Create tables
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('Tables created!')"
```

## Local Development vs Production

- **Local (Windows)**: Uses SQL Server
- **Production (Render.com)**: Uses PostgreSQL
- **Automatic detection**: Based on platform and environment variables

## Next Steps After Deployment

1. Set up domain (if needed)
2. Configure SSL (automatic on Render.com)
3. Set up monitoring
4. Configure backups
5. Add custom domain

## Support

If you encounter issues:
1. Check Render.com logs
2. Verify environment variables
3. Test database connection locally
4. Check this guide for common solutions
