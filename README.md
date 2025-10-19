# Lifestyle Data Analytics Platform

A comprehensive Flask-based web application for tracking and analyzing lifestyle data including fitness, nutrition, and health metrics.

## 🚀 Features

### Core Functionality
- **User Management**: Registration, login, and profile management
- **Workout Tracking**: Log workouts, exercises, heart rate, and calories burned
- **Nutrition Tracking**: Track meals, macros, water intake, and dietary preferences
- **Analytics Dashboard**: Real-time charts and insights
- **Report Generation**: PDF and Excel reports with detailed analysis
- **Email Reports**: Automated email delivery of reports

### Data Fields Tracked
- **User Profile**: Age, gender, weight, height, BMI, experience level, body fat percentage
- **Workout Data**: Type, duration, calories burned, heart rate (max/avg/resting), frequency
- **Exercise Details**: Name, sets, reps, muscle groups, difficulty, equipment needed
- **Nutrition Data**: Daily meals, calories, macros (carbs/proteins/fats), water intake
- **Meal Details**: Name, type, diet type, nutritional content, cooking method, health status

### Analytics & Insights
- BMI trend analysis
- Calorie balance tracking
- Macro nutrient distribution
- Workout type analysis
- Heart rate trends
- Consistency scoring
- Personalized recommendations

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (development) / MySQL/PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **Reports**: ReportLab (PDF), openpyxl (Excel)
- **Email**: SMTP with APScheduler
- **Authentication**: Flask-Login

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lifestyle-analytics
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-app-password"
   ```

5. **Initialize database**
   ```bash
   python app.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## 🗄️ Database Schema

### Core Tables
- **users**: User profiles and authentication
- **workout_logs**: Daily workout sessions
- **exercise_logs**: Individual exercises within workouts
- **nutrition_logs**: Daily nutrition intake
- **meals**: Individual meal details
- **daily_stats**: Aggregated daily statistics
- **exercises**: Exercise library
- **reports**: Generated report history

## 📊 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### User Management
- `GET/POST /profile` - User profile management
- `GET /api/dashboard_data` - Dashboard data API

### Data Logging
- `POST /log_workout` - Log workout session
- `POST /log_nutrition` - Log nutrition data

### Analytics
- `GET /analytics` - Analytics dashboard
- `GET /api/chart_data/<type>` - Chart data API

### Reports
- `POST /generate_report` - Generate reports
- `GET /reports` - View report history

## 📈 Usage Guide

### 1. User Registration
- Visit the homepage and click "Register"
- Fill in username, email, and password
- Complete profile setup with physical metrics

### 2. Logging Workouts
- Navigate to "Workout Tracker"
- Click "Log Workout" to add a new session
- Fill in workout details and add individual exercises
- Track heart rate, duration, and calories burned

### 3. Tracking Nutrition
- Go to "Nutrition Tracker"
- Click "Log Nutrition" to add daily intake
- Record meals with detailed nutritional information
- Monitor macro distribution and water intake

### 4. Viewing Analytics
- Access the "Analytics" page for detailed insights
- View BMI trends, calorie balance, and workout distribution
- Monitor progress with interactive charts

### 5. Generating Reports
- Visit the "Reports" section
- Choose report type (daily/weekly/monthly)
- Select format (PDF/Excel)
- Schedule email delivery if needed

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///lifestyle_analytics.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Configuration
- **Development**: SQLite (default)
- **Production**: MySQL or PostgreSQL
- Update `DATABASE_URL` in `config.py`

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-factor authentication
2. Generate app-specific password
3. Set `MAIL_USERNAME` and `MAIL_PASSWORD`

### Email Features
- Daily/weekly/monthly automated reports
- Custom email scheduling
- PDF report attachments
- HTML email templates

## 🚀 Deployment

### Heroku Deployment
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Add buildpacks:
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### Docker Deployment
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

2. Build and run:
   ```bash
   docker build -t lifestyle-analytics .
   docker run -p 5000:5000 lifestyle-analytics
   ```

## 🧪 Testing

### Run Tests
```bash
python -m pytest tests/
```

### Test Coverage
```bash
python -m pytest --cov=app tests/
```

## 📝 API Documentation

### Sample API Calls

#### Register User
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

#### Log Workout
```bash
curl -X POST http://localhost:5000/log_workout \
  -H "Content-Type: application/json" \
  -d '{
    "workout_type": "Cardio",
    "session_duration": 45,
    "calories_burned": 350,
    "max_bpm": 160,
    "avg_bpm": 140
  }'
```

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy
- Input validation and sanitization
- Secure session management

## 📊 Performance Optimization

- Database indexing on frequently queried fields
- Chart data caching
- Lazy loading for large datasets
- Responsive design for mobile devices
- Optimized database queries

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Email: support@lifestyleanalytics.com
- Documentation: [Wiki](https://github.com/username/lifestyle-analytics/wiki)

## 🗺️ Roadmap

### Upcoming Features
- [ ] Mobile app (React Native)
- [ ] Social features and challenges
- [ ] Integration with fitness trackers (Fitbit, Apple Health)
- [ ] AI-powered recommendations
- [ ] Advanced analytics with machine learning
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Voice logging capabilities

### Version History
- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added email reports and scheduling
- **v1.2.0** - Enhanced analytics and chart visualizations
- **v2.0.0** - Mobile app and social features (planned)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap team for responsive UI components
- Chart.js for beautiful data visualizations
- ReportLab for PDF generation capabilities
- All contributors and users who provided feedback

---

**Made with ❤️ for health and fitness enthusiasts**