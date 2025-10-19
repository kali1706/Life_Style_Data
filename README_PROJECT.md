# 🏋️ Lifestyle Data Analytics Platform

A comprehensive **Flask-based web application** for tracking fitness, nutrition, and health metrics with powerful analytics and reporting capabilities.

---

## 📋 Overview

यह एक complete lifestyle data analytics solution है जो:
- **Workout Tracking** - Exercise logging, heart rate monitoring, calorie tracking
- **Nutrition Monitoring** - Meal logging, macro tracking, calorie counting
- **Analytics Dashboard** - Interactive charts, trends, insights
- **Report Generation** - PDF and Excel exports
- **Personalized Recommendations** - AI-driven health insights

---

## 🚀 Features

### ✅ Core Features

1. **User Profile Management**
   - Personal information (age, gender, height, weight)
   - BMI automatic calculation
   - Body fat percentage tracking
   - Experience level tracking

2. **Workout Tracker**
   - Log workouts with type, duration, and intensity
   - Track heart rate (Max, Avg, Resting BPM)
   - Calculate calories burned
   - Workout history with trends
   - Exercise library database

3. **Nutrition Tracker**
   - Daily meal logging
   - Macro tracking (Carbs, Proteins, Fats)
   - Calorie counting
   - Water intake monitoring
   - Diet type selection (Keto, Vegan, Balanced, etc.)

4. **Analytics Dashboard**
   - BMI trend visualization
   - Weekly calorie burn vs intake
   - Macro breakdown pie charts
   - Heart rate trends
   - Workout frequency analysis
   - Progress score (0-100)

5. **Report Generation**
   - **PDF Reports**: Comprehensive analysis with charts
   - **Excel Reports**: Detailed data export with multiple sheets
   - **Email Reports**: Automated delivery (optional)
   - **Power BI Integration**: Excel export optimized for BI

6. **Insights & Recommendations**
   - Personalized health insights
   - Workout recommendations
   - Nutrition advice
   - Progress tracking

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask 2.3+** - Web framework
- **SQLAlchemy** - ORM for database
- **Flask-Login** - User authentication

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5** - Responsive UI
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

### Reports & Analytics
- **ReportLab** - PDF generation
- **openpyxl** - Excel export
- **Matplotlib** - Chart generation
- **Pandas & NumPy** - Data analysis

---

## 📁 Project Structure

```
lifestyle-analytics/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models (SQLAlchemy)
├── utils.py                    # Utility functions (calculations, insights)
├── report_generator.py         # PDF & Excel report generation
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database (auto-generated)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── profile.html           # User profile
│   ├── workout_tracker.html   # Workout logging
│   ├── nutrition_tracker.html # Nutrition logging
│   ├── analytics.html         # Analytics & charts
│   └── reports.html           # Report generation
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── charts.js          # Chart configurations
│   └── charts/                # Generated chart images
│
├── uploads/                    # File uploads (if needed)
├── reports/                    # Generated reports (PDF/Excel)
└── README_PROJECT.md          # This file
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Clone or Download Project
```bash
cd /path/to/project
```

### 3. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize Database
```bash
flask --app app init-db
flask --app app seed-exercises
```

Or using Python:
```bash
python app.py
# Database will be auto-created on first run
```

### 6. Run the Application
```bash
python app.py
```

Or using Flask CLI:
```bash
flask --app app run --debug
```

The application will be available at: **http://localhost:5000**

---

## 📊 Database Models

### User
- id, username, email, password_hash
- age, gender, weight, height, bmi
- experience_level, fat_percentage
- created_at, updated_at

### WorkoutLog
- id, user_id, workout_type
- session_duration, calories_burned
- max_bpm, avg_bpm, resting_bpm
- date, notes

### ExerciseLog
- id, workout_id, name_of_exercise
- sets, reps, weight_used
- target_muscle_group, body_part

### NutritionLog
- id, user_id, date
- total_calories, total_carbs, total_proteins, total_fats
- water_intake

### Meal
- id, nutrition_log_id
- meal_name, meal_type, diet_type
- calories, carbs, proteins, fats
- sugar, sodium, cholesterol

### DailyStats
- id, user_id, date
- total_workouts, total_calories_burned
- total_calories_consumed, calorie_balance

---

## 🎯 Usage Guide

### 1. Register & Login
- Create an account with username, email, and password
- Login to access the dashboard

### 2. Setup Profile
- Navigate to **Profile** page
- Enter: Age, Gender, Weight, Height, Experience Level
- BMI will be calculated automatically

### 3. Log Workouts
- Go to **Workout Tracker**
- Select workout type, duration, calories
- Optionally add heart rate data
- View recent workout history

### 4. Log Nutrition
- Go to **Nutrition Tracker**
- Log meals with calorie and macro information
- Track daily water intake
- View today's summary

### 5. View Analytics
- **Dashboard**: Quick overview with key metrics
- **Analytics**: Detailed charts and trends
- Progress score, consistency tracking
- Macro distribution analysis

### 6. Generate Reports
- Go to **Reports** page
- Download **PDF Report** for comprehensive analysis
- Download **Excel Report** for detailed data
- Use Excel export for Power BI integration

---

## 📈 Key Metrics Calculated

### BMI (Body Mass Index)
```
BMI = Weight (kg) / Height (m)²
```
- **<18.5**: Underweight
- **18.5-24.9**: Normal
- **25-29.9**: Overweight
- **≥30**: Obese

### Calorie Balance
```
Balance = Calories Consumed - Calories Burned
```
- **Positive**: Calorie surplus (weight gain)
- **Negative**: Calorie deficit (weight loss)
- **~0**: Maintenance

### Macro Percentages
```
Carbs (%) = (Carbs × 4) / Total Calories × 100
Protein (%) = (Protein × 4) / Total Calories × 100
Fat (%) = (Fat × 9) / Total Calories × 100
```

### Progress Score (0-100)
- **30 points**: BMI status (Normal = 30, Overweight/Underweight = 15)
- **40 points**: Consistency score (workout frequency)
- **30 points**: Macro balance (ideal ratios)

### Consistency Score
```
Consistency = (Workout Days / 7) × 100
```

---

## 📱 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Profile & Dashboard
- `GET /dashboard` - Main dashboard
- `GET/POST /profile` - User profile management

### Tracking
- `GET/POST /workout_tracker` - Log and view workouts
- `GET/POST /nutrition_tracker` - Log and view nutrition

### Analytics
- `GET /analytics` - Analytics page with charts
- `GET /api/dashboard_data` - JSON dashboard data
- `GET /api/workout_history?days=30` - Workout history JSON

### Reports
- `GET /reports` - Reports page
- `GET /generate_report/pdf` - Generate & download PDF
- `GET /generate_report/excel` - Generate & download Excel

---

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Real-time data visualization with Chart.js
- **Color-coded Metrics**: Visual feedback for progress
- **Card-based Layout**: Modern, clean interface
- **Bootstrap Components**: Professional UI elements
- **Smooth Animations**: Enhanced user experience

---

## 🔒 Security Features

- Password hashing using Werkzeug
- Flask-Login for session management
- CSRF protection (Flask default)
- SQL injection prevention (SQLAlchemy ORM)
- Secure file uploads

---

## 📊 Sample Data & Testing

### Create Test User
1. Register: username=`testuser`, email=`test@example.com`
2. Setup profile with sample data

### Add Sample Workouts
```python
Workout 1: Strength, 1.0 hours, 400 calories
Workout 2: Cardio, 0.5 hours, 300 calories
Workout 3: HIIT, 0.75 hours, 500 calories
```

### Add Sample Meals
```python
Breakfast: 500 cal, 60g carbs, 20g protein, 15g fat
Lunch: 700 cal, 80g carbs, 35g protein, 25g fat
Dinner: 600 cal, 70g carbs, 30g protein, 20g fat
```

---

## 🚀 Deployment

### Option 1: Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
heroku run flask --app app init-db
```

### Option 2: Digital Ocean / AWS
- Use gunicorn as WSGI server
- Setup nginx as reverse proxy
- Configure SSL certificate

### Option 3: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Migration (if needed)
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 📝 Future Enhancements

1. **Mobile App** - React Native version
2. **Social Features** - Share progress, leaderboards
3. **Goal Setting** - Set and track fitness goals
4. **AI Recommendations** - ML-based personalized suggestions
5. **Integration** - Fitbit, Apple Health, Google Fit sync
6. **Community** - User forums and tips
7. **Meal Plans** - Pre-designed nutrition plans
8. **Workout Programs** - Structured training programs

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete and recreate database
rm database.db
flask --app app init-db
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use different port
flask run --port 5001
```

---

## 📄 License

MIT License - Feel free to use for personal or commercial projects.

---

## 👨‍💻 Developer

**Project**: Lifestyle Data Analytics Platform  
**Framework**: Flask  
**Version**: 1.0.0  
**Date**: 2025

---

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review the code comments
3. Test with sample data
4. Check browser console for errors

---

## 🎯 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access application
http://localhost:5000

# Register account → Setup profile → Start tracking!
```

---

**Happy Tracking! 🏋️‍♂️🥗📊**
