import pymysql
import os

def create_mysql_database():
    """Create MySQL database for the lifestyle analytics project"""

    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Add your MySQL password here if needed
        'database': None
    }

    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )

        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS lifestyle_analytics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✓ Database 'lifestyle_analytics' created successfully!")

            # Use the database
            cursor.execute("USE lifestyle_analytics")

            # Create tables
            tables_sql = [
                """
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
                    monthly_reports BOOLEAN DEFAULT TRUE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                    INDEX idx_user_date (user_id, workout_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                    FOREIGN KEY (workout_id) REFERENCES workout_logs(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                    INDEX idx_user_date (user_id, meal_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """,

                """
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
                    INDEX idx_user_created (user_id, created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
            ]

            # Execute table creation
            for table_sql in tables_sql:
                cursor.execute(table_sql)

            print("✓ All tables created successfully!")

            # Insert sample exercises
            sample_exercises = [
                ('Push-ups', 'Builds upper body strength, improves core stability', 200, 'Chest, Shoulders, Triceps', 'None', 'Beginner', 'Arms', 'Upper', 'Start in plank position, lower body to ground, push back up'),
                ('Squats', 'Builds leg strength, improves mobility', 180, 'Quadriceps, Glutes, Hamstrings', 'None', 'Beginner', 'Legs', 'Lower', 'Stand with feet shoulder-width apart, lower as if sitting in chair, return to standing'),
                ('Plank', 'Strengthens core, improves posture', 150, 'Core, Shoulders', 'None', 'Beginner', 'Core', 'Core', 'Hold plank position with straight body line, engage core'),
                ('Burpees', 'Full body workout, improves cardiovascular fitness', 300, 'Full Body', 'None', 'Intermediate', 'Full Body', 'Full Body', 'Squat down, jump back to plank, do push-up, jump feet forward, jump up'),
                ('Mountain Climbers', 'Cardio workout, strengthens core and shoulders', 250, 'Core, Shoulders, Legs', 'None', 'Intermediate', 'Full Body', 'Full Body', 'Start in plank, alternate bringing knees to chest rapidly')
            ]

            cursor.executemany("""
                INSERT IGNORE INTO exercises
                (name, benefit, burns_calories_per_30min, target_muscle_group, equipment_needed, difficulty_level, body_part, type_of_muscle, instructions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_exercises)

            print("✓ Sample exercises inserted successfully!")

        connection.commit()
        print("\n🎉 MySQL database setup completed successfully!")
        print("Database: lifestyle_analytics")
        print("Host: localhost")
        print("User: root")

    except pymysql.Error as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

    return True

if __name__ == '__main__':
    create_mysql_database()
