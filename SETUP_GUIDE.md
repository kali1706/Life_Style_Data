# 🚀 Quick Setup Guide - Lifestyle Analytics Platform

## Step-by-Step Installation

### ✅ Step 1: Check Python Installation
```bash
python --version
# Should show Python 3.8 or higher
```

### ✅ Step 2: Navigate to Project Directory
```bash
cd /workspace
# or wherever your project is located
```

### ✅ Step 3: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### ✅ Step 4: Install Required Packages
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database)
- Flask-Login (authentication)
- ReportLab (PDF generation)
- openpyxl (Excel generation)
- And other dependencies...

### ✅ Step 5: Initialize Database
```bash
# Method 1: Using Flask CLI
flask --app app init-db
flask --app app seed-exercises

# Method 2: Just run the app (auto-creates database)
python app.py
```

### ✅ Step 6: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### ✅ Step 7: Open in Browser
```
http://localhost:5000
```

---

## 🎯 First Time Usage

### 1. Register Account
- Click "Register" button
- Enter username, email, password
- Submit registration

### 2. Login
- Use your credentials to login
- You'll be redirected to dashboard

### 3. Setup Profile
- Click "Profile" in navbar
- Enter:
  - Age (e.g., 25)
  - Gender (Male/Female/Other)
  - Weight in kg (e.g., 70)
  - Height in meters (e.g., 1.75)
  - Body Fat % (optional)
  - Experience Level (Beginner/Intermediate/Advanced)
- Click "Update Profile"
- BMI will be calculated automatically!

### 4. Log First Workout
- Click "Workout" in navbar
- Fill in workout details:
  - Type: Strength, Cardio, HIIT, etc.
  - Duration: in hours (e.g., 1.5 for 1hr 30min)
  - Calories burned: estimate or from device
  - Heart rate data (optional)
- Click "Log Workout"

### 5. Log First Meal
- Click "Nutrition" in navbar
- Fill in meal details:
  - Meal name: Breakfast, Lunch, Dinner
  - Calories, Carbs, Protein, Fat
  - Water intake (optional)
- Click "Log Meal"

### 6. View Analytics
- Click "Analytics" to see charts and trends
- Check your progress score!

### 7. Generate Reports
- Click "Reports" in navbar
- Download PDF or Excel report
- Use Excel for Power BI integration

---

## 🔧 Common Issues & Solutions

### Issue 1: ModuleNotFoundError
**Problem**: Missing Python packages

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue 2: Database Error
**Problem**: Database not initialized

**Solution**:
```bash
rm database.db  # Delete old database
python app.py    # Will recreate automatically
```

### Issue 3: Port Already in Use
**Problem**: Port 5000 is occupied

**Solution**:
```bash
# Use different port
flask run --port 5001
```

Or edit `app.py` line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Issue 4: Permission Denied (Linux/Mac)
**Problem**: Cannot write to folders

**Solution**:
```bash
chmod -R 755 reports uploads static/charts
```

### Issue 5: Virtual Environment Not Activating
**Problem**: venv command not working

**Solution**:
```bash
# Install virtualenv
pip install virtualenv

# Create environment
virtualenv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

---

## 📦 Package Requirements Explained

| Package | Purpose |
|---------|---------|
| Flask | Web framework for building the app |
| Flask-SQLAlchemy | Database ORM |
| Flask-Login | User authentication & sessions |
| Werkzeug | Password hashing & security |
| pandas | Data manipulation |
| numpy | Numerical calculations |
| matplotlib | Chart generation |
| plotly | Interactive visualizations |
| reportlab | PDF report generation |
| openpyxl | Excel file creation |
| Pillow | Image processing |
| python-dateutil | Date/time utilities |
| APScheduler | Task scheduling (for automated reports) |
| Flask-Mail | Email functionality |
| gunicorn | Production WSGI server |

---

## 🌐 Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Variables
Create `.env` file:
```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///database.db
FLASK_ENV=production
```

Load in app:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🧪 Testing the Application

### Test User Creation
```python
# In Python shell
from app import app, db
from models import User

with app.app_context():
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    user.age = 25
    user.gender = 'Male'
    user.weight = 70
    user.height = 1.75
    user.calculate_bmi()
    db.session.add(user)
    db.session.commit()
```

### Test Workout Logging
```python
from models import WorkoutLog
from datetime import datetime

with app.app_context():
    workout = WorkoutLog(
        user_id=1,
        workout_type='Strength',
        session_duration=1.0,
        calories_burned=400,
        date=datetime.utcnow()
    )
    db.session.add(workout)
    db.session.commit()
```

---

## 📊 Sample Data for Testing

### Sample Workouts
```
1. Strength Training - 1 hour - 400 calories
2. Cardio Run - 45 min - 350 calories
3. HIIT Session - 30 min - 500 calories
4. Yoga - 1 hour - 200 calories
5. Cycling - 1.5 hours - 600 calories
```

### Sample Meals
```
Breakfast: 500 cal (60g carbs, 20g protein, 15g fat)
Lunch: 700 cal (80g carbs, 35g protein, 25g fat)
Snack: 200 cal (25g carbs, 5g protein, 10g fat)
Dinner: 600 cal (70g carbs, 30g protein, 20g fat)
```

---

## 🎓 Learning Resources

### Flask Documentation
- https://flask.palletsprojects.com/

### SQLAlchemy Documentation
- https://docs.sqlalchemy.org/

### Bootstrap 5
- https://getbootstrap.com/docs/5.3/

### Chart.js
- https://www.chartjs.org/docs/

---

## 💡 Pro Tips

1. **Use Virtual Environment** - Always work in a venv to avoid conflicts
2. **Backup Database** - Regularly backup `database.db` file
3. **Check Logs** - Use `--debug` mode during development
4. **Update Packages** - Keep dependencies updated for security
5. **Test Reports** - Generate reports after adding some data

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed successfully
- [ ] Database created (database.db file exists)
- [ ] Application runs without errors
- [ ] Can access http://localhost:5000
- [ ] Can register a new account
- [ ] Can login successfully
- [ ] Can update profile
- [ ] Can log workout
- [ ] Can log meal
- [ ] Can view analytics
- [ ] Can generate reports

---

## 🆘 Need Help?

If you encounter issues:

1. **Check Python version**: `python --version`
2. **Check installed packages**: `pip list`
3. **Check error messages** in terminal
4. **Check browser console** (F12 in most browsers)
5. **Verify database exists**: `ls -la database.db`
6. **Try recreating database**: Delete and restart app

---

## 🎉 Success!

If you can see the dashboard and log data, congratulations! 🎊

You now have a fully functional Lifestyle Analytics Platform!

**Next Steps:**
- Log your daily workouts and meals
- Track your progress over time
- Generate weekly reports
- Set fitness goals
- Share your success!

---

**Happy Tracking! 💪**
