# 📡 API Documentation - Lifestyle Analytics Platform

## Base URL
```
http://localhost:5000
```

---

## 🔐 Authentication Endpoints

### Register New User
**Endpoint**: `POST /register`

**Request Body** (Form Data):
```
username: string (required)
email: string (required, valid email)
password: string (required, min 6 characters)
```

**Response**: Redirect to login page with success message

**Example**:
```html
<form method="POST" action="/register">
    <input name="username" value="john_doe">
    <input name="email" value="john@example.com">
    <input name="password" value="password123">
    <button type="submit">Register</button>
</form>
```

---

### User Login
**Endpoint**: `POST /login`

**Request Body** (Form Data):
```
username: string (required)
password: string (required)
```

**Response**: 
- Success: Redirect to dashboard
- Failure: Redirect to login with error message

**Example**:
```html
<form method="POST" action="/login">
    <input name="username" value="john_doe">
    <input name="password" value="password123">
    <button type="submit">Login</button>
</form>
```

---

### User Logout
**Endpoint**: `GET /logout`

**Authentication**: Required (login_required)

**Response**: Redirect to index page

---

## 👤 Profile Management

### Get/Update User Profile
**Endpoint**: `GET/POST /profile`

**Authentication**: Required

**GET Response**: Renders profile page with user data

**POST Request Body** (Form Data):
```
age: integer (required)
gender: string (Male/Female/Other)
weight: float (kg)
height: float (meters)
fat_percentage: float (optional)
experience_level: integer (1=Beginner, 2=Intermediate, 3=Advanced)
```

**POST Response**: Profile updated, BMI calculated, redirect to profile

**Example**:
```python
# POST request
{
    "age": 25,
    "gender": "Male",
    "weight": 70.5,
    "height": 1.75,
    "fat_percentage": 18.5,
    "experience_level": 2
}
```

---

## 📊 Dashboard

### Main Dashboard
**Endpoint**: `GET /dashboard`

**Authentication**: Required

**Response**: Renders dashboard with:
- Weekly statistics
- Progress score
- Insights and recommendations
- User profile summary

**Data Provided**:
```python
{
    "user": User object,
    "weekly_stats": {
        "total_workouts": int,
        "total_calories_burned": int,
        "avg_workout_duration": float (minutes),
        "total_calories_consumed": int,
        "avg_daily_intake": int,
        "total_meals": int,
        "macro_percentages": {
            "Carbs": float,
            "Protein": float,
            "Fat": float
        },
        "consistency_score": float,
        "calorie_balance": int
    },
    "insights": {
        "insights": [list of insight strings],
        "recommendations": [list of recommendation strings]
    },
    "progress_score": int (0-100)
}
```

---

## 🏋️ Workout Tracking

### Log Workout
**Endpoint**: `POST /workout_tracker`

**Authentication**: Required

**Request Body** (Form Data):
```
workout_type: string (Strength, Cardio, HIIT, Yoga, etc.)
session_duration: float (hours)
calories_burned: integer
max_bpm: integer (optional)
avg_bpm: integer (optional)
resting_bpm: integer (optional)
notes: string (optional)
```

**Response**: Redirect to workout tracker with success message

**Example**:
```python
{
    "workout_type": "Strength",
    "session_duration": 1.5,  # 1.5 hours
    "calories_burned": 450,
    "avg_bpm": 140,
    "max_bpm": 170,
    "resting_bpm": 65,
    "notes": "Great workout today!"
}
```

---

### View Workout History
**Endpoint**: `GET /workout_tracker`

**Authentication**: Required

**Response**: Renders workout tracker with recent 10 workouts

---

## 🍽️ Nutrition Tracking

### Log Meal
**Endpoint**: `POST /nutrition_tracker`

**Authentication**: Required

**Request Body** (Form Data):
```
meal_name: string (Breakfast, Lunch, Dinner, Snack)
meal_type: string (Main, Snack, Beverage)
diet_type: string (Balanced, Keto, Vegan, etc.)
calories: integer (required)
carbs: integer (grams, required)
proteins: integer (grams, required)
fats: integer (grams, required)
sugar: integer (grams, optional)
sodium: integer (mg, optional)
water_intake: float (liters, optional)
description: string (optional)
```

**Response**: Redirect to nutrition tracker with success message

**Example**:
```python
{
    "meal_name": "Breakfast",
    "meal_type": "Main",
    "diet_type": "Balanced",
    "calories": 500,
    "carbs": 60,
    "proteins": 20,
    "fats": 15,
    "sugar": 10,
    "sodium": 300,
    "water_intake": 2.5,
    "description": "Oatmeal with fruits"
}
```

---

### View Nutrition History
**Endpoint**: `GET /nutrition_tracker`

**Authentication**: Required

**Response**: Renders nutrition tracker with:
- Today's nutrition summary
- Recent 7 days of nutrition logs
- Meals breakdown

---

## 📈 Analytics

### View Analytics Dashboard
**Endpoint**: `GET /analytics`

**Authentication**: Required

**Response**: Renders analytics page with:
- User health metrics (BMI, weight, body fat)
- Weekly statistics
- 30-day trends
- Multiple charts

**Data Provided**:
```python
{
    "user": User object,
    "weekly_stats": {...},
    "trends": {
        "dates": [list of date strings],
        "weights": [list of weight values],
        "bmis": [list of BMI values],
        "calories_burned": [list of calorie burn values],
        "calories_consumed": [list of calorie intake values]
    }
}
```

---

## 🔌 JSON API Endpoints

### Get Dashboard Data (JSON)
**Endpoint**: `GET /api/dashboard_data`

**Authentication**: Required

**Response** (JSON):
```json
{
    "weekly_stats": {
        "total_workouts": 5,
        "total_calories_burned": 2500,
        "avg_workout_duration": 45.5,
        "total_calories_consumed": 12000,
        "avg_daily_intake": 2000,
        "total_meals": 21,
        "macro_percentages": {
            "Carbs": 50.5,
            "Protein": 25.3,
            "Fat": 24.2
        },
        "consistency_score": 85.7,
        "calorie_balance": 500
    },
    "insights": {
        "insights": ["Your BMI is 23.5 (Normal)", "Great consistency!"],
        "recommendations": ["Increase protein intake"]
    },
    "progress_score": 87,
    "user": {
        "bmi": 23.5,
        "weight": 70.5,
        "height": 1.75,
        "age": 25
    }
}
```

**Usage Example** (JavaScript):
```javascript
fetch('/api/dashboard_data')
    .then(response => response.json())
    .then(data => {
        console.log(data.progress_score);
        console.log(data.weekly_stats);
    });
```

---

### Get Workout History (JSON)
**Endpoint**: `GET /api/workout_history?days=30`

**Authentication**: Required

**Query Parameters**:
- `days` (optional, default=30): Number of days to retrieve

**Response** (JSON):
```json
{
    "dates": ["2025-01-15", "2025-01-16", "2025-01-17"],
    "calories": [450, 300, 500],
    "durations": [60, 45, 90],
    "types": ["Strength", "Cardio", "HIIT"]
}
```

**Usage Example** (JavaScript):
```javascript
fetch('/api/workout_history?days=7')
    .then(response => response.json())
    .then(data => {
        // Create chart with data
        createWorkoutChart(data);
    });
```

---

## 📄 Report Generation

### Generate PDF Report
**Endpoint**: `GET /generate_report/pdf`

**Authentication**: Required

**Response**: Binary PDF file download

**File Name Format**: `report_username_YYYYMMDD_HHMMSS.pdf`

**Content Includes**:
- User profile summary
- Weekly statistics
- Macronutrient breakdown
- Insights and recommendations
- Progress score

**Usage Example** (HTML):
```html
<a href="/generate_report/pdf" download>
    Download PDF Report
</a>
```

---

### Generate Excel Report
**Endpoint**: `GET /generate_report/excel`

**Authentication**: Required

**Response**: Binary Excel file (.xlsx) download

**File Name Format**: `report_username_YYYYMMDD_HHMMSS.xlsx`

**Sheets Included**:
1. User Profile
2. Weekly Statistics
3. Macronutrients
4. Workout History (Last 30 days)
5. Nutrition History (Last 30 days)

**Usage Example** (HTML):
```html
<a href="/generate_report/excel" download>
    Download Excel Report
</a>
```

---

## 📊 Reports Page

### View Reports Page
**Endpoint**: `GET /reports`

**Authentication**: Required

**Response**: Renders reports page with:
- Report generation options
- PDF report details
- Excel report details
- Power BI integration guide

---

## 🔢 Data Models

### User Model
```python
{
    "id": integer,
    "username": string,
    "email": string,
    "age": integer,
    "gender": string,
    "weight": float,
    "height": float,
    "bmi": float,
    "experience_level": integer,
    "fat_percentage": float,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Workout Log Model
```python
{
    "id": integer,
    "user_id": integer,
    "workout_type": string,
    "session_duration": float,
    "calories_burned": integer,
    "max_bpm": integer,
    "avg_bpm": integer,
    "resting_bpm": integer,
    "notes": string,
    "date": datetime
}
```

### Nutrition Log Model
```python
{
    "id": integer,
    "user_id": integer,
    "date": date,
    "total_calories": integer,
    "total_carbs": integer,
    "total_proteins": integer,
    "total_fats": integer,
    "water_intake": float,
    "meals": [list of Meal objects]
}
```

### Meal Model
```python
{
    "id": integer,
    "nutrition_log_id": integer,
    "meal_name": string,
    "meal_type": string,
    "diet_type": string,
    "calories": integer,
    "carbs": integer,
    "proteins": integer,
    "fats": integer,
    "sugar": integer,
    "sodium": integer,
    "description": string,
    "timestamp": datetime
}
```

---

## 🔒 Authentication & Authorization

### Session Management
- Uses Flask-Login for session management
- Session cookie stored in browser
- Expires after 7 days (configurable)

### Protected Routes
All routes except `/`, `/login`, `/register` require authentication.

If not authenticated, user is redirected to `/login`.

### Password Security
- Passwords hashed using Werkzeug's `generate_password_hash`
- Uses pbkdf2:sha256 method
- Salt automatically added

---

## ⚠️ Error Handling

### Common HTTP Status Codes

**200 OK**: Request successful
```json
{
    "status": "success",
    "data": {...}
}
```

**400 Bad Request**: Invalid input
```json
{
    "status": "error",
    "message": "Invalid input data"
}
```

**401 Unauthorized**: Not logged in
- Redirects to login page

**404 Not Found**: Resource not found
```json
{
    "status": "error",
    "message": "Resource not found"
}
```

**500 Internal Server Error**: Server error
```json
{
    "status": "error",
    "message": "Internal server error"
}
```

---

## 🧪 Testing API Endpoints

### Using cURL

**Register User**:
```bash
curl -X POST http://localhost:5000/register \
  -d "username=testuser&email=test@example.com&password=test123"
```

**Login**:
```bash
curl -X POST http://localhost:5000/login \
  -d "username=testuser&password=test123" \
  -c cookies.txt
```

**Get Dashboard Data**:
```bash
curl http://localhost:5000/api/dashboard_data \
  -b cookies.txt
```

**Log Workout**:
```bash
curl -X POST http://localhost:5000/workout_tracker \
  -b cookies.txt \
  -d "workout_type=Strength&session_duration=1.5&calories_burned=450"
```

---

### Using Python Requests

```python
import requests

# Base URL
BASE_URL = 'http://localhost:5000'

# Create session
session = requests.Session()

# Register
response = session.post(f'{BASE_URL}/register', data={
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'test123'
})

# Login
response = session.post(f'{BASE_URL}/login', data={
    'username': 'testuser',
    'password': 'test123'
})

# Get dashboard data
response = session.get(f'{BASE_URL}/api/dashboard_data')
data = response.json()
print(data['progress_score'])

# Log workout
response = session.post(f'{BASE_URL}/workout_tracker', data={
    'workout_type': 'Cardio',
    'session_duration': 1.0,
    'calories_burned': 500
})
```

---

### Using Postman

1. **Import Collection**: Create new collection "Lifestyle Analytics"
2. **Set Base URL**: `http://localhost:5000`
3. **Enable Cookies**: Settings → Enable cookie jar
4. **Test Endpoints**:
   - POST /register
   - POST /login
   - GET /api/dashboard_data
   - POST /workout_tracker

---

## 📚 Rate Limiting

Currently, no rate limiting is implemented. For production:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## 🔐 CORS Configuration

For cross-origin requests (if building separate frontend):

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 📝 API Best Practices

1. **Always authenticate** protected endpoints
2. **Validate input data** before processing
3. **Use HTTPS** in production
4. **Implement rate limiting** to prevent abuse
5. **Log API requests** for debugging
6. **Return consistent JSON** format
7. **Handle errors gracefully**
8. **Document all endpoints**

---

## 🆘 Support

For API issues:
1. Check authentication status
2. Verify request format
3. Check response status code
4. Review server logs
5. Test with curl/Postman

---

**API Version**: 1.0.0  
**Last Updated**: 2025-01-19
