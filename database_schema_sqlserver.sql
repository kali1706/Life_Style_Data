-- Lifestyle Analytics Database Schema for SQL Server
-- SQL Server Database Creation Script

-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'lifestyle_analytics')
BEGIN
    CREATE DATABASE lifestyle_analytics;
END
GO

USE lifestyle_analytics;
GO

-- Users table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[users] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [username] NVARCHAR(80) UNIQUE NOT NULL,
        [email] NVARCHAR(120) UNIQUE NOT NULL,
        [password_hash] NVARCHAR(255) NOT NULL,
        [age] INT,
        [gender] NVARCHAR(10),
        [weight] FLOAT,
        [height] FLOAT,
        [bmi] FLOAT,
        [experience_level] INT,
        [fat_percentage] FLOAT,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        [last_login] DATETIME2,
        [daily_reports] BIT DEFAULT 0,
        [weekly_reports] BIT DEFAULT 1,
        [monthly_reports] BIT DEFAULT 1
    );
    
    CREATE INDEX [IX_users_username] ON [dbo].[users] ([username]);
    CREATE INDEX [IX_users_email] ON [dbo].[users] ([email]);
END
GO

-- Exercises reference table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[exercises]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[exercises] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [name] NVARCHAR(100) UNIQUE NOT NULL,
        [benefit] NVARCHAR(MAX),
        [burns_calories_per_30min] INT,
        [target_muscle_group] NVARCHAR(50),
        [equipment_needed] NVARCHAR(100),
        [difficulty_level] NVARCHAR(20),
        [body_part] NVARCHAR(30),
        [type_of_muscle] NVARCHAR(30),
        [instructions] NVARCHAR(MAX),
        [created_at] DATETIME2 DEFAULT GETDATE()
    );
    
    CREATE INDEX [IX_exercises_name] ON [dbo].[exercises] ([name]);
    CREATE INDEX [IX_exercises_difficulty] ON [dbo].[exercises] ([difficulty_level]);
    CREATE INDEX [IX_exercises_body_part] ON [dbo].[exercises] ([body_part]);
END
GO

-- Workout logs table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[workout_logs]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[workout_logs] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [user_id] INT NOT NULL,
        [workout_type] NVARCHAR(50),
        [session_duration] FLOAT,
        [calories_burned] INT,
        [max_bpm] INT,
        [avg_bpm] INT,
        [resting_bpm] INT,
        [workout_frequency] INT,
        [workout_date] DATE DEFAULT CAST(GETDATE() AS DATE),
        [created_at] DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY ([user_id]) REFERENCES [dbo].[users]([id]) ON DELETE CASCADE
    );
    
    CREATE INDEX [IX_workout_logs_user_date] ON [dbo].[workout_logs] ([user_id], [workout_date]);
    CREATE INDEX [IX_workout_logs_type] ON [dbo].[workout_logs] ([workout_type]);
END
GO

-- Exercise logs table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[exercise_logs]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[exercise_logs] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [workout_id] INT NOT NULL,
        [name_of_exercise] NVARCHAR(100) NOT NULL,
        [sets] INT,
        [reps] INT,
        [benefit] NVARCHAR(MAX),
        [burns_calories_per_30min] INT,
        [target_muscle_group] NVARCHAR(50),
        [equipment_needed] NVARCHAR(100),
        [difficulty_level] NVARCHAR(20),
        [body_part] NVARCHAR(30),
        [type_of_muscle] NVARCHAR(30),
        [created_at] DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY ([workout_id]) REFERENCES [dbo].[workout_logs]([id]) ON DELETE CASCADE
    );
    
    CREATE INDEX [IX_exercise_logs_workout] ON [dbo].[exercise_logs] ([workout_id]);
    CREATE INDEX [IX_exercise_logs_name] ON [dbo].[exercise_logs] ([name_of_exercise]);
END
GO

-- Nutrition logs table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[nutrition_logs]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[nutrition_logs] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [user_id] INT NOT NULL,
        [daily_meals_frequency] INT,
        [carbs] INT,
        [proteins] INT,
        [fats] INT,
        [calories] INT,
        [water_intake] FLOAT,
        [log_date] DATE DEFAULT CAST(GETDATE() AS DATE),
        [created_at] DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY ([user_id]) REFERENCES [dbo].[users]([id]) ON DELETE CASCADE,
        CONSTRAINT [UQ_nutrition_logs_user_date] UNIQUE ([user_id], [log_date])
    );
    
    CREATE INDEX [IX_nutrition_logs_user_date] ON [dbo].[nutrition_logs] ([user_id], [log_date]);
END
GO

-- Meals table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[meals]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[meals] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [user_id] INT NOT NULL,
        [nutrition_log_id] INT,
        [meal_name] NVARCHAR(50),
        [meal_type] NVARCHAR(30),
        [diet_type] NVARCHAR(30),
        [sugar] INT,
        [sodium] INT,
        [cholesterol] INT,
        [serving_size] INT,
        [calories] INT,
        [carbs] INT,
        [proteins] INT,
        [fats] INT,
        [cooking_method] NVARCHAR(30),
        [prep_time] INT,
        [cook_time] INT,
        [is_healthy] BIT DEFAULT 1,
        [meal_date] DATE DEFAULT CAST(GETDATE() AS DATE),
        [created_at] DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY ([user_id]) REFERENCES [dbo].[users]([id]) ON DELETE CASCADE,
        FOREIGN KEY ([nutrition_log_id]) REFERENCES [dbo].[nutrition_logs]([id]) ON DELETE CASCADE
    );
    
    CREATE INDEX [IX_meals_user_date] ON [dbo].[meals] ([user_id], [meal_date]);
    CREATE INDEX [IX_meals_name] ON [dbo].[meals] ([meal_name]);
END
GO

-- Daily stats table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[daily_stats]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[daily_stats] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [user_id] INT NOT NULL,
        [date] DATE DEFAULT CAST(GETDATE() AS DATE),
        [total_calories_burned] INT DEFAULT 0,
        [total_calories_consumed] INT DEFAULT 0,
        [total_workout_duration] FLOAT DEFAULT 0,
        [total_water_intake] FLOAT DEFAULT 0,
        [avg_heart_rate] INT,
        [consistency_score] INT DEFAULT 0,
        [caloric_balance] INT,
        [macro_carbs_percent] FLOAT,
        [macro_proteins_percent] FLOAT,
        [macro_fats_percent] FLOAT,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY ([user_id]) REFERENCES [dbo].[users]([id]) ON DELETE CASCADE,
        CONSTRAINT [UQ_daily_stats_user_date] UNIQUE ([user_id], [date])
    );
    
    CREATE INDEX [IX_daily_stats_user_date] ON [dbo].[daily_stats] ([user_id], [date]);
END
GO

-- Reports table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[reports]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[reports] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [user_id] INT NOT NULL,
        [report_type] NVARCHAR(20),
        [report_format] NVARCHAR(10),
        [file_path] NVARCHAR(255),
        [email_sent] BIT DEFAULT 0,
        [email_recipients] NVARCHAR(MAX),
        [start_date] DATE,
        [end_date] DATE,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY ([user_id]) REFERENCES [dbo].[users]([id]) ON DELETE CASCADE
    );
    
    CREATE INDEX [IX_reports_user_created] ON [dbo].[reports] ([user_id], [created_at]);
    CREATE INDEX [IX_reports_type] ON [dbo].[reports] ([report_type]);
END
GO

-- Insert sample exercises
INSERT INTO [dbo].[exercises] ([name], [benefit], [burns_calories_per_30min], [target_muscle_group], [equipment_needed], [difficulty_level], [body_part], [type_of_muscle], [instructions])
VALUES
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
GO

-- Create views for common queries
IF EXISTS (SELECT * FROM sys.views WHERE name = 'user_workout_summary')
    DROP VIEW [dbo].[user_workout_summary];
GO

CREATE VIEW [dbo].[user_workout_summary] AS
SELECT 
    u.[id] as [user_id],
    u.[username],
    COUNT(wl.[id]) as [total_workouts],
    SUM(wl.[session_duration]) as [total_duration_hours],
    SUM(wl.[calories_burned]) as [total_calories_burned],
    AVG(CAST(wl.[calories_burned] AS FLOAT)) as [avg_calories_per_workout]
FROM [dbo].[users] u
LEFT JOIN [dbo].[workout_logs] wl ON u.[id] = wl.[user_id]
GROUP BY u.[id], u.[username];
GO

IF EXISTS (SELECT * FROM sys.views WHERE name = 'user_nutrition_summary')
    DROP VIEW [dbo].[user_nutrition_summary];
GO

CREATE VIEW [dbo].[user_nutrition_summary] AS
SELECT 
    u.[id] as [user_id],
    u.[username],
    COUNT(nl.[id]) as [total_nutrition_logs],
    AVG(CAST(nl.[calories] AS FLOAT)) as [avg_daily_calories],
    AVG(CAST(nl.[carbs] AS FLOAT)) as [avg_daily_carbs],
    AVG(CAST(nl.[proteins] AS FLOAT)) as [avg_daily_proteins],
    AVG(CAST(nl.[fats] AS FLOAT)) as [avg_daily_fats]
FROM [dbo].[users] u
LEFT JOIN [dbo].[nutrition_logs] nl ON u.[id] = nl.[user_id]
GROUP BY u.[id], u.[username];
GO

-- Show completion message
SELECT 'Database schema created successfully!' as [status];

