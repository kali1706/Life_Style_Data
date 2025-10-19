# ✅ Installation & Verification Checklist

## 🎯 Complete Installation Guide

यह checklist आपको step-by-step guide करेगी कि project को कैसे install और verify करें।

---

## 📋 Pre-Installation Checklist

### System Requirements
- [ ] **Python 3.8 or higher** installed
  ```bash
  python --version
  # OR
  python3 --version
  ```
  Expected output: `Python 3.8.x` or higher

- [ ] **pip** (Python package manager) installed
  ```bash
  pip --version
  # OR
  python -m pip --version
  ```

- [ ] **Git** (optional, for version control)
  ```bash
  git --version
  ```

- [ ] **Text Editor** or IDE
  - VS Code (recommended)
  - PyCharm
  - Sublime Text
  - Or any editor

---

## 📁 Step 1: Project Files Verification

### Verify All Files Exist

Run these commands to verify project structure:

```bash
# Navigate to project directory
cd /workspace

# List all Python files
ls -la *.py

# Expected files:
# - app.py
# - config.py
# - models.py
# - utils.py
# - report_generator.py

# List all templates
ls -la templates/

# Expected files (10):
# - base.html
# - index.html
# - login.html
# - register.html
# - dashboard.html
# - profile.html
# - workout_tracker.html
# - nutrition_tracker.html
# - analytics.html
# - reports.html

# List static files
ls -la static/css/
ls -la static/js/

# Expected files:
# - static/css/style.css
# - static/js/charts.js
```

### File Count Verification
```bash
# Count Python files
ls *.py | wc -l
# Expected: 5

# Count template files
ls templates/*.html | wc -l
# Expected: 10

# Count documentation files
ls *.md | wc -l
# Expected: 6+
```

---

## 🔧 Step 2: Virtual Environment Setup

### Create Virtual Environment

```bash
# Method 1: Using venv
python -m venv venv

# Method 2: Using virtualenv
virtualenv venv

# Method 3: Using python3
python3 -m venv venv
```

### Activate Virtual Environment

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**On Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

### Verify Activation
After activation, your terminal prompt should show `(venv)` at the beginning:
```
(venv) user@machine:/workspace$
```

---

## 📦 Step 3: Install Dependencies

### Install All Packages

```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### Expected Installation Output
```
Installing collected packages:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug
- pandas
- numpy
- matplotlib
- plotly
- reportlab
- openpyxl
- ... (and others)
```

### Verify Installation

```bash
# Check installed packages
pip list

# Verify specific packages
pip show Flask
pip show Flask-SQLAlchemy
pip show reportlab
```

### Troubleshooting Package Installation

**Issue: pip not found**
```bash
python -m ensurepip --upgrade
```

**Issue: Permission denied (Linux/Mac)**
```bash
pip install --user -r requirements.txt
```

**Issue: SSL certificate error**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## 🗄️ Step 4: Database Initialization

### Method 1: Automatic (Recommended)

Just run the application - database will be created automatically:

```bash
python app.py
```

Look for this message in terminal:
```
Database initialized!
* Running on http://0.0.0.0:5000
```

### Method 2: Manual Initialization

If you prefer manual setup:

```bash
# Using Flask CLI
flask --app app init-db

# Seed exercise database (optional)
flask --app app seed-exercises
```

### Verify Database Creation

```bash
# Check if database.db file exists
ls -la database.db

# Expected output:
# -rw-r--r-- 1 user user 12288 Jan 19 10:30 database.db
```

### Database Structure Verification

```bash
# Open SQLite database (optional)
sqlite3 database.db

# List tables
.tables

# Expected tables:
# users
# workout_logs
# exercise_logs
# exercises
# nutrition_logs
# meals
# daily_stats

# Exit sqlite
.quit
```

---

## 🚀 Step 5: Run Application

### Start Flask Server

```bash
# Make sure you're in project directory
cd /workspace

# Activate virtual environment (if not already)
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Run application
python app.py
```

### Expected Output

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

### Alternative: Use Different Port

If port 5000 is already in use:

```bash
# Edit app.py and change port
# OR run with Flask CLI
flask run --port 5001
```

---

## 🌐 Step 6: Access Application

### Open in Browser

1. Open your web browser
2. Navigate to: **http://localhost:5000**
3. You should see the landing page

### Verify Pages

Visit each page to ensure they load:

- [ ] **Landing Page**: http://localhost:5000/
- [ ] **Register**: http://localhost:5000/register
- [ ] **Login**: http://localhost:5000/login

---

## 👤 Step 7: Test User Registration

### Create Test Account

1. Click **"Register"** button
2. Fill in the form:
   - **Username**: testuser
   - **Email**: test@example.com
   - **Password**: password123
   - **Confirm Password**: password123
3. Click **"Register"** button
4. You should see: "Registration successful! Please login."

### Login

1. Click **"Login"** button
2. Enter credentials:
   - **Username**: testuser
   - **Password**: password123
3. Click **"Login"** button
4. You should be redirected to **Dashboard**

---

## 📊 Step 8: Test Core Features

### Test Profile Setup

1. Click **"Profile"** in navbar
2. Fill in your information:
   - **Age**: 25
   - **Gender**: Male/Female
   - **Weight**: 70 (kg)
   - **Height**: 1.75 (meters)
   - **Experience Level**: Intermediate
3. Click **"Update Profile"**
4. You should see: **"Profile updated successfully!"**
5. **BMI should be calculated** automatically

### Test Workout Logging

1. Click **"Workout"** in navbar
2. Fill in workout details:
   - **Workout Type**: Strength
   - **Duration**: 1.5 (hours)
   - **Calories Burned**: 450
   - **Average BPM**: 140 (optional)
3. Click **"Log Workout"**
4. You should see: **"Workout logged successfully!"**
5. Workout should appear in **Recent Workouts** table

### Test Nutrition Logging

1. Click **"Nutrition"** in navbar
2. Fill in meal details:
   - **Meal Name**: Breakfast
   - **Meal Type**: Main
   - **Diet Type**: Balanced
   - **Calories**: 500
   - **Carbs**: 60 (grams)
   - **Proteins**: 20 (grams)
   - **Fats**: 15 (grams)
3. Click **"Log Meal"**
4. You should see: **"Meal logged successfully!"**
5. Today's summary should update

### Test Analytics

1. Click **"Analytics"** in navbar
2. Verify the following are displayed:
   - [ ] Current BMI card
   - [ ] Weight card
   - [ ] Consistency score
   - [ ] Weekly calories chart
   - [ ] Macro distribution chart
3. Charts should render properly

### Test Report Generation

1. Click **"Reports"** in navbar
2. Try downloading reports:
   - [ ] Click **"Download PDF Report"**
     - PDF file should download
     - Open and verify content
   - [ ] Click **"Download Excel Report"**
     - Excel file should download
     - Open and verify multiple sheets

---

## ✅ Step 9: Verification Checklist

### Application Status
- [ ] Flask server starts without errors
- [ ] Database file created (database.db exists)
- [ ] Application accessible at http://localhost:5000
- [ ] No error messages in terminal

### Pages Working
- [ ] Landing page loads
- [ ] Registration page loads
- [ ] Login page loads
- [ ] Dashboard loads (after login)
- [ ] Profile page loads
- [ ] Workout tracker loads
- [ ] Nutrition tracker loads
- [ ] Analytics page loads
- [ ] Reports page loads

### Features Working
- [ ] User can register
- [ ] User can login
- [ ] User can update profile
- [ ] BMI calculates automatically
- [ ] User can log workouts
- [ ] User can log meals
- [ ] Charts render on dashboard
- [ ] Analytics page shows data
- [ ] PDF report downloads
- [ ] Excel report downloads

### UI Elements
- [ ] Navigation bar displays correctly
- [ ] Cards display properly
- [ ] Forms are functional
- [ ] Buttons work
- [ ] Tables display data
- [ ] Charts render correctly
- [ ] Alerts/flash messages show
- [ ] Responsive on mobile (test by resizing browser)

---

## 🐛 Common Issues & Solutions

### Issue 1: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies again
pip install -r requirements.txt
```

### Issue 2: Database Error

**Error**: `OperationalError: no such table: users`

**Solution**:
```bash
# Delete database and recreate
rm database.db
python app.py  # Will recreate automatically
```

### Issue 3: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
flask run --port 5001
```

### Issue 4: Charts Not Displaying

**Error**: Charts show as blank

**Solution**:
1. Check browser console (F12)
2. Ensure Chart.js is loading from CDN
3. Check if data is being passed to template
4. Clear browser cache (Ctrl+Shift+Delete)

### Issue 5: CSS Not Loading

**Error**: Page looks unstyled

**Solution**:
```bash
# Check static files exist
ls static/css/style.css
ls static/js/charts.js

# Clear browser cache
# Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
```

### Issue 6: Permission Denied (Reports)

**Error**: Cannot create PDF/Excel files

**Solution**:
```bash
# Ensure reports directory exists and is writable
mkdir -p reports uploads static/charts
chmod 755 reports uploads static/charts
```

---

## 🔍 Testing Checklist

### Smoke Testing
- [ ] Application starts
- [ ] Landing page loads
- [ ] Can navigate between pages
- [ ] Can register and login

### Functional Testing
- [ ] Profile update works
- [ ] Workout logging works
- [ ] Nutrition logging works
- [ ] Data displays correctly
- [ ] Charts render properly
- [ ] Reports generate successfully

### UI Testing
- [ ] Desktop view (>992px)
- [ ] Tablet view (768-992px)
- [ ] Mobile view (<768px)
- [ ] All forms are usable
- [ ] Navigation is accessible

### Browser Testing
- [ ] Google Chrome
- [ ] Mozilla Firefox
- [ ] Safari (Mac)
- [ ] Microsoft Edge

---

## 📊 Sample Test Data

### Test User Profile
```
Username: testuser
Email: test@example.com
Password: password123
Age: 25
Gender: Male
Weight: 70 kg
Height: 1.75 m
Experience: Intermediate
```

### Test Workouts
```
Workout 1:
- Type: Strength
- Duration: 1.5 hours
- Calories: 450

Workout 2:
- Type: Cardio
- Duration: 0.75 hours
- Calories: 350

Workout 3:
- Type: HIIT
- Duration: 0.5 hours
- Calories: 500
```

### Test Meals
```
Breakfast:
- Calories: 500
- Carbs: 60g, Protein: 20g, Fat: 15g

Lunch:
- Calories: 700
- Carbs: 80g, Protein: 35g, Fat: 25g

Dinner:
- Calories: 600
- Carbs: 70g, Protein: 30g, Fat: 20g
```

---

## 🎓 Next Steps After Verification

Once all tests pass:

1. **Explore Features**
   - Log multiple workouts
   - Track nutrition for a week
   - View analytics trends
   - Generate reports

2. **Customize**
   - Update CSS styles
   - Add custom workout types
   - Modify chart colors
   - Add new features

3. **Deploy** (Optional)
   - Choose hosting platform
   - Configure production settings
   - Set up domain
   - Enable HTTPS

4. **Share**
   - Invite friends to test
   - Get feedback
   - Iterate and improve

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Documentation**
   - README_PROJECT.md
   - SETUP_GUIDE.md
   - API_DOCUMENTATION.md

2. **Review Logs**
   - Check terminal output
   - Check browser console (F12)
   - Look for error messages

3. **Debug**
   - Enable Flask debug mode
   - Add print statements
   - Test API endpoints

4. **Reset**
   - Delete database and recreate
   - Reinstall dependencies
   - Try on fresh environment

---

## ✅ Success Criteria

Your installation is successful when:

✅ All files are present  
✅ Dependencies installed  
✅ Database created  
✅ Application runs without errors  
✅ All pages load correctly  
✅ Can register and login  
✅ Can log workouts and meals  
✅ Charts display properly  
✅ Reports generate successfully  

---

## 🎉 Congratulations!

If all checks pass, your **Lifestyle Data Analytics Platform** is ready to use!

**Start tracking your fitness journey today! 💪📊**

---

*Last Updated: 2025-01-19*
