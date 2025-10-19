# 🏋️‍♀️ Lifestyle Data Analytics Platform

A comprehensive web application for tracking fitness, nutrition, and health metrics with advanced analytics, reporting, and insights.

## 📊 Features

### 🎯 Core Functionality
- **User Management**: Registration, login, profile management with BMI calculation
- **Workout Tracking**: Log workouts with duration, calories, heart rate, and intensity
- **Nutrition Monitoring**: Track meals, macros, water intake, and dietary preferences
- **Analytics Dashboard**: Interactive charts and visualizations of your progress
- **Report Generation**: PDF and Excel reports with comprehensive data analysis
- **Email Reports**: Automated email delivery of reports to users or healthcare providers

### 📈 Analytics & Insights
- BMI trends and health metrics tracking
- Calorie balance analysis (intake vs. burned)
- Macro breakdown visualization (carbs, proteins, fats)
- Heart rate zone analysis
- Workout type distribution
- Progress scoring algorithm
- AI-powered personalized recommendations

### 📋 Report Features
- **PDF Reports**: Professional formatted reports with charts and insights
- **Excel Export**: Multi-sheet workbooks with raw data and embedded charts
- **Email Integration**: Send reports to trainers, doctors, or family members
- **Scheduled Reports**: Automatic weekly/monthly report generation
- **Custom Date Ranges**: Generate reports for specific time periods

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **ReportLab**: PDF generation
- **OpenPyXL**: Excel file generation
- **Pandas**: Data analysis and manipulation

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Interactive charts and visualizations
- **Font Awesome**: Icons and visual elements
- **Custom CSS**: Modern design with gradients and animations

### Database
- **SQLite**: Development database (easily upgradeable to PostgreSQL/MySQL)
- **Comprehensive Schema**: Users, workouts, nutrition, meals, exercises, daily stats

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lifestyle-analytics-platform
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
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "MAIL_USERNAME=your-email@gmail.com" >> .env
   echo "MAIL_PASSWORD=your-app-password" >> .env
   ```

5. **Initialize database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Register a new account or use demo credentials

## 📁 Project Structure

```
lifestyle_analytics/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── utils.py                    # Utility functions
├── report_generator.py         # PDF/Excel report generation
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── profile.html           # User profile
│   ├── workout_tracker.html   # Workout logging
│   ├── nutrition_tracker.html # Nutrition logging
│   ├── analytics.html         # Analytics dashboard
│   └── reports.html           # Reports section
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── charts.js         # Chart configurations
└── reports/                   # Generated reports (auto-created)
```

## 🎨 User Interface

### Dashboard
- Clean, modern design with gradient cards
- Real-time metrics and progress tracking
- Quick action buttons for common tasks
- Recent activity feed

### Analytics
- Interactive charts with Chart.js
- Multiple visualization types (line, bar, pie, radar)
- Filterable data by date ranges
- AI-powered insights and recommendations

### Reports
- Professional PDF generation with charts
- Excel exports with multiple worksheets
- Email scheduling and delivery
- Report history and management

## 📊 Database Schema

### Core Tables
- **Users**: Profile information, BMI, experience level
- **WorkoutLog**: Exercise sessions with metrics
- **NutritionLog**: Meal tracking with macros
- **Meal**: Food database with nutritional info
- **Exercise**: Exercise library with details
- **DailyStats**: Aggregated daily metrics

### Key Relationships
- One-to-many: User → Workouts, Nutrition, DailyStats
- Lookup tables: Meals, Exercises for reference data

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///lifestyle_analytics.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Email Setup (Gmail)
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use app password in MAIL_PASSWORD

## 📈 Analytics Features

### Progress Scoring Algorithm
- BMI status (20 points)
- Workout consistency (30 points)
- Nutrition balance (25 points)
- Activity level (15 points)
- Hydration (10 points)

### Health Insights
- BMI category and recommendations
- Macro ratio analysis
- Heart rate zone optimization
- Calorie balance tracking
- Hydration monitoring

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection
- Input validation and sanitization
- Secure file handling for reports

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📱 Mobile Responsiveness

- Bootstrap 5 responsive grid system
- Mobile-first design approach
- Touch-friendly interface elements
- Optimized charts for mobile viewing

## 🎯 Future Enhancements

### Planned Features
- [ ] Mobile app (React Native)
- [ ] Integration with fitness trackers (Fitbit, Apple Health)
- [ ] Social features and challenges
- [ ] AI-powered meal recommendations
- [ ] Barcode scanning for food logging
- [ ] Integration with gym equipment
- [ ] Telemedicine integration
- [ ] Advanced machine learning insights

### Technical Improvements
- [ ] Redis caching for better performance
- [ ] PostgreSQL for production database
- [ ] Elasticsearch for advanced search
- [ ] WebSocket for real-time updates
- [ ] API rate limiting
- [ ] Advanced security features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**Database Issues**
```bash
# Reset database
rm lifestyle_analytics.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**Email Issues**
- Ensure Gmail app password is used (not regular password)
- Check firewall settings for SMTP ports
- Verify environment variables are set correctly

**Chart Display Issues**
- Clear browser cache
- Check JavaScript console for errors
- Ensure Chart.js CDN is accessible

### Getting Help
- Check the [Issues](../../issues) page for known problems
- Create a new issue with detailed description
- Include error messages and system information

## 🏆 Acknowledgments

- Bootstrap team for the excellent UI framework
- Chart.js for beautiful visualizations
- Flask community for comprehensive documentation
- ReportLab for PDF generation capabilities
- All contributors and testers

---

**Built with ❤️ for a healthier lifestyle**

*Transform your fitness journey with comprehensive data analytics and insights.*