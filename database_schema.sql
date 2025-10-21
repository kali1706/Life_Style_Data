-- Lifestyle Analytics Database Schema
-- MySQL Database Creation Script

-- Create database
CREATE DATABASE IF NOT EXISTS lifestyle_analytics 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE lifestyle_analytics;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(10),
    weight FLOAT,
    height FLOAT,
    bmi FLOAT,
    experience_level INT,
    fat_percentage FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    daily_reports BOOLEAN DEFAULT FALSE,
    weekly_reports BOOLEAN DEFAULT TRUE,
    monthly_reports BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exercises reference table
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    benefit TEXT,
    burns_calories_per_30min INT,
    target_muscle_group VARCHAR(50),
    equipment_needed VARCHAR(100),
    difficulty_level VARCHAR(20),
    body_part VARCHAR(30),
    type_of_muscle VARCHAR(30),
    instructions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_body_part (body_part)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Workout logs table
CREATE TABLE IF NOT EXISTS workout_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    workout_type VARCHAR(50),
    session_duration FLOAT,
    calories_burned INT,
    max_bpm INT,
    avg_bpm INT,
    resting_bpm INT,
    workout_frequency INT,
    workout_date DATE DEFAULT (CURRENT_DATE),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, workout_date),
    INDEX idx_workout_type (workout_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exercise logs table
CREATE TABLE IF NOT EXISTS exercise_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workout_id INT NOT NULL,
    name_of_exercise VARCHAR(100) NOT NULL,
    sets INT,
    reps INT,
    benefit TEXT,
    burns_calories_per_30min INT,
    target_muscle_group VARCHAR(50),
    equipment_needed VARCHAR(100),
    difficulty_level VARCHAR(20),
    body_part VARCHAR(30),
    type_of_muscle VARCHAR(30),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workout_id) REFERENCES workout_logs(id) ON DELETE CASCADE,
    INDEX idx_workout_id (workout_id),
    INDEX idx_exercise_name (name_of_exercise)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Nutrition logs table
CREATE TABLE IF NOT EXISTS nutrition_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    daily_meals_frequency INT,
    carbs INT,
    proteins INT,
    fats INT,
    calories INT,
    water_intake FLOAT,
    log_date DATE DEFAULT (CURRENT_DATE),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, log_date),
    INDEX idx_user_date (user_id, log_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Meals table
CREATE TABLE IF NOT EXISTS meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nutrition_log_id INT,
    meal_name VARCHAR(50),
    meal_type VARCHAR(30),
    diet_type VARCHAR(30),
    sugar INT,
    sodium INT,
    cholesterol INT,
    serving_size INT,
    calories INT,
    carbs INT,
    proteins INT,
    fats INT,
    cooking_method VARCHAR(30),
    prep_time INT,
    cook_time INT,
    is_healthy BOOLEAN DEFAULT TRUE,
    meal_date DATE DEFAULT (CURRENT_DATE),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (nutrition_log_id) REFERENCES nutrition_logs(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, meal_date),
    INDEX idx_meal_name (meal_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Daily stats table
CREATE TABLE IF NOT EXISTS daily_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE DEFAULT (CURRENT_DATE),
    total_calories_burned INT DEFAULT 0,
    total_calories_consumed INT DEFAULT 0,
    total_workout_duration FLOAT DEFAULT 0,
    total_water_intake FLOAT DEFAULT 0,
    avg_heart_rate INT,
    consistency_score INT DEFAULT 0,
    caloric_balance INT,
    macro_carbs_percent FLOAT,
    macro_proteins_percent FLOAT,
    macro_fats_percent FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, date),
    INDEX idx_user_date (user_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    report_type VARCHAR(20),
    report_format VARCHAR(10),
    file_path VARCHAR(255),
    email_sent BOOLEAN DEFAULT FALSE,
    email_recipients TEXT,
    start_date DATE,
    end_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_report_type (report_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample exercises
INSERT IGNORE INTO exercises (name, benefit, burns_calories_per_30min, target_muscle_group, equipment_needed, difficulty_level, body_part, type_of_muscle, instructions) VALUES
('Push-ups', 'Builds upper body strength, improves core stability', 200, 'Chest, Shoulders, Triceps', 'None', 'Beginner', 'Arms', 'Upper', 'Start in plank position, lower body to ground, push back up'),
('Squats', 'Builds leg strength, improves mobility', 180, 'Quadriceps, Glutes, Hamstrings', 'None', 'Beginner', 'Legs', 'Lower', 'Stand with feet shoulder-width apart, lower as if sitting in chair, return to standing'),
('Plank', 'Strengthens core, improves posture', 150, 'Core, Shoulders', 'None', 'Beginner', 'Core', 'Core', 'Hold plank position with straight body line, engage core'),
('Burpees', 'Full body workout, improves cardiovascular fitness', 300, 'Full Body', 'None', 'Intermediate', 'Full Body', 'Full Body', 'Squat down, jump back to plank, do push-up, jump feet forward, jump up'),
('Mountain Climbers', 'Cardio workout, strengthens core and shoulders', 250, 'Core, Shoulders, Legs', 'None', 'Intermediate', 'Full Body', 'Full Body', 'Start in plank, alternate bringing knees to chest rapidly'),
('Lunges', 'Builds leg strength, improves balance', 160, 'Quadriceps, Glutes, Hamstrings', 'None', 'Beginner', 'Legs', 'Lower', 'Step forward into lunge position, lower back knee toward ground, push back to starting position'),
('Jumping Jacks', 'Cardio exercise, improves coordination', 220, 'Full Body', 'None', 'Beginner', 'Full Body', 'Full Body', 'Jump feet apart while raising arms overhead, return to starting position'),
('Crunches', 'Strengthens abdominal muscles', 140, 'Core', 'None', 'Beginner', 'Core', 'Core', 'Lie on back, lift shoulders off ground by contracting abs'),
('High Knees', 'Cardio workout, improves coordination', 280, 'Legs, Core', 'None', 'Beginner', 'Full Body', 'Lower', 'Run in place while lifting knees high toward chest'),
('Tricep Dips', 'Builds tricep strength', 170, 'Triceps, Shoulders', 'Chair or bench', 'Intermediate', 'Arms', 'Upper', 'Sit on edge of chair, lower body by bending elbows, push back up');

-- Create views for common queries
CREATE OR REPLACE VIEW user_workout_summary AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(wl.id) as total_workouts,
    SUM(wl.session_duration) as total_duration_hours,
    SUM(wl.calories_burned) as total_calories_burned,
    AVG(wl.calories_burned) as avg_calories_per_workout
FROM users u
LEFT JOIN workout_logs wl ON u.id = wl.user_id
GROUP BY u.id, u.username;

CREATE OR REPLACE VIEW user_nutrition_summary AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(nl.id) as total_nutrition_logs,
    AVG(nl.calories) as avg_daily_calories,
    AVG(nl.carbs) as avg_daily_carbs,
    AVG(nl.proteins) as avg_daily_proteins,
    AVG(nl.fats) as avg_daily_fats
FROM users u
LEFT JOIN nutrition_logs nl ON u.id = nl.user_id
GROUP BY u.id, u.username;

-- Create indexes for better performance
CREATE INDEX idx_workout_logs_user_date ON workout_logs(user_id, workout_date);
CREATE INDEX idx_nutrition_logs_user_date ON nutrition_logs(user_id, log_date);
CREATE INDEX idx_meals_user_date ON meals(user_id, meal_date);
CREATE INDEX idx_daily_stats_user_date ON daily_stats(user_id, date);

-- Show completion message
SELECT 'Database schema created successfully!' as status;
