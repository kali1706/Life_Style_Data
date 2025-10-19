"""Report generation module for PDF and Excel exports"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from datetime import datetime, timedelta
import os
from config import Config
from models import User, WorkoutLog, NutritionLog, Meal, db
from utils import get_weekly_stats, get_monthly_trends, generate_insights, calculate_progress_score
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt


def generate_pdf_report(user_id, period='weekly'):
    """Generate PDF report for user"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Create filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(Config.REPORTS_FOLDER, f'report_{user.username}_{timestamp}.pdf')
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3498DB'),
        spaceAfter=12
    )
    
    # Title
    title = Paragraph(f"Lifestyle Analytics Report", title_style)
    story.append(title)
    
    subtitle = Paragraph(f"Generated for: {user.username}<br/>{datetime.now().strftime('%B %d, %Y')}", 
                        styles['Normal'])
    story.append(subtitle)
    story.append(Spacer(1, 0.3*inch))
    
    # User Profile Section
    story.append(Paragraph("Personal Profile", heading_style))
    
    profile_data = [
        ['Age', str(user.age) if user.age else 'N/A'],
        ['Gender', user.gender or 'N/A'],
        ['Weight', f"{user.weight} kg" if user.weight else 'N/A'],
        ['Height', f"{user.height} m" if user.height else 'N/A'],
        ['BMI', f"{user.bmi} ({user.get_bmi_category()})" if user.bmi else 'N/A'],
        ['Body Fat %', f"{user.fat_percentage}%" if user.fat_percentage else 'N/A'],
        ['Experience Level', ['Beginner', 'Intermediate', 'Advanced'][user.experience_level-1] if user.experience_level else 'N/A']
    ]
    
    profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    story.append(profile_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Weekly Statistics
    story.append(Paragraph("Weekly Performance Summary", heading_style))
    weekly_stats = get_weekly_stats(user_id)
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Workouts', str(weekly_stats['total_workouts'])],
        ['Total Calories Burned', f"{weekly_stats['total_calories_burned']} kcal"],
        ['Avg Workout Duration', f"{weekly_stats['avg_workout_duration']} min"],
        ['Total Meals Logged', str(weekly_stats['total_meals'])],
        ['Total Calories Consumed', f"{weekly_stats['total_calories_consumed']} kcal"],
        ['Avg Daily Intake', f"{weekly_stats['avg_daily_intake']} kcal"],
        ['Consistency Score', f"{weekly_stats['consistency_score']}%"],
        ['Calorie Balance', f"{weekly_stats['calorie_balance']} kcal"]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')])
    ]))
    
    story.append(stats_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Macro Breakdown
    story.append(Paragraph("Macronutrient Distribution", heading_style))
    macro_pct = weekly_stats['macro_percentages']
    
    macro_data = [
        ['Nutrient', 'Percentage', 'Ideal Range'],
        ['Carbohydrates', f"{macro_pct['Carbs']}%", '45-65%'],
        ['Proteins', f"{macro_pct['Protein']}%", '10-35%'],
        ['Fats', f"{macro_pct['Fat']}%", '20-35%']
    ]
    
    macro_table = Table(macro_data, colWidths=[2*inch, 2*inch, 2*inch])
    macro_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    story.append(macro_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Insights and Recommendations
    story.append(Paragraph("Personalized Insights & Recommendations", heading_style))
    insights_data = generate_insights(user)
    
    insights_text = "<b>Key Insights:</b><br/>"
    for insight in insights_data['insights']:
        insights_text += f"✓ {insight}<br/>"
    
    insights_text += "<br/><b>Recommendations:</b><br/>"
    for rec in insights_data['recommendations']:
        insights_text += f"• {rec}<br/>"
    
    story.append(Paragraph(insights_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Progress Score
    progress_score = calculate_progress_score(user)
    story.append(Paragraph(f"Overall Progress Score", heading_style))
    score_text = f"<font size=24 color='#27AE60'><b>{progress_score}/100</b></font>"
    story.append(Paragraph(score_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    return filename


def generate_excel_report(user_id):
    """Generate Excel report for user"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Create filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(Config.REPORTS_FOLDER, f'report_{user.username}_{timestamp}.xlsx')
    
    # Create workbook
    wb = Workbook()
    
    # Remove default sheet
    wb.remove(wb.active)
    
    # Header styling
    header_fill = PatternFill(start_color='3498DB', end_color='3498DB', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF')
    center_align = Alignment(horizontal='center', vertical='center')
    
    # Sheet 1: User Profile
    ws1 = wb.create_sheet('User Profile')
    ws1.append(['Lifestyle Analytics Report'])
    ws1.append([f'Generated for: {user.username}'])
    ws1.append([f'Date: {datetime.now().strftime("%B %d, %Y")}'])
    ws1.append([])
    
    ws1.append(['Profile Information', ''])
    ws1.append(['Field', 'Value'])
    profile_data = [
        ['Username', user.username],
        ['Email', user.email],
        ['Age', user.age or 'N/A'],
        ['Gender', user.gender or 'N/A'],
        ['Weight (kg)', user.weight or 'N/A'],
        ['Height (m)', user.height or 'N/A'],
        ['BMI', user.bmi or 'N/A'],
        ['BMI Category', user.get_bmi_category() if user.bmi else 'N/A'],
        ['Body Fat %', user.fat_percentage or 'N/A'],
        ['Experience Level', ['Beginner', 'Intermediate', 'Advanced'][user.experience_level-1] if user.experience_level else 'N/A']
    ]
    
    for row in profile_data:
        ws1.append(row)
    
    # Apply styling
    ws1['A6'].fill = header_fill
    ws1['A6'].font = header_font
    ws1['B6'].fill = header_fill
    ws1['B6'].font = header_font
    
    # Sheet 2: Weekly Statistics
    ws2 = wb.create_sheet('Weekly Statistics')
    weekly_stats = get_weekly_stats(user_id)
    
    ws2.append(['Weekly Performance Summary'])
    ws2.append([])
    ws2.append(['Metric', 'Value'])
    
    stats_data = [
        ['Total Workouts', weekly_stats['total_workouts']],
        ['Total Calories Burned', weekly_stats['total_calories_burned']],
        ['Avg Workout Duration (min)', weekly_stats['avg_workout_duration']],
        ['Total Meals Logged', weekly_stats['total_meals']],
        ['Total Calories Consumed', weekly_stats['total_calories_consumed']],
        ['Avg Daily Intake', weekly_stats['avg_daily_intake']],
        ['Consistency Score (%)', weekly_stats['consistency_score']],
        ['Calorie Balance', weekly_stats['calorie_balance']]
    ]
    
    for row in stats_data:
        ws2.append(row)
    
    ws2['A3'].fill = header_fill
    ws2['A3'].font = header_font
    ws2['B3'].fill = header_fill
    ws2['B3'].font = header_font
    
    # Sheet 3: Macronutrient Breakdown
    ws3 = wb.create_sheet('Macronutrients')
    macro_pct = weekly_stats['macro_percentages']
    
    ws3.append(['Macronutrient Distribution'])
    ws3.append([])
    ws3.append(['Nutrient', 'Percentage (%)', 'Ideal Range'])
    
    macro_data = [
        ['Carbohydrates', macro_pct['Carbs'], '45-65%'],
        ['Proteins', macro_pct['Protein'], '10-35%'],
        ['Fats', macro_pct['Fat'], '20-35%']
    ]
    
    for row in macro_data:
        ws3.append(row)
    
    ws3['A3'].fill = header_fill
    ws3['A3'].font = header_font
    ws3['B3'].fill = header_fill
    ws3['B3'].font = header_font
    ws3['C3'].fill = header_fill
    ws3['C3'].font = header_font
    
    # Sheet 4: Workout History
    ws4 = wb.create_sheet('Workout History')
    ws4.append(['Workout History (Last 30 Days)'])
    ws4.append([])
    ws4.append(['Date', 'Type', 'Duration (min)', 'Calories Burned', 'Avg BPM', 'Max BPM'])
    
    start_date = datetime.utcnow() - timedelta(days=30)
    workouts = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        WorkoutLog.date >= start_date
    ).order_by(WorkoutLog.date.desc()).all()
    
    for workout in workouts:
        ws4.append([
            workout.date.strftime('%Y-%m-%d'),
            workout.workout_type,
            round(workout.session_duration * 60, 1) if workout.session_duration else 0,
            workout.calories_burned or 0,
            workout.avg_bpm or 0,
            workout.max_bpm or 0
        ])
    
    ws4['A3'].fill = header_fill
    ws4['A3'].font = header_font
    for cell in ws4[3]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    # Sheet 5: Nutrition History
    ws5 = wb.create_sheet('Nutrition History')
    ws5.append(['Nutrition History (Last 30 Days)'])
    ws5.append([])
    ws5.append(['Date', 'Total Calories', 'Carbs (g)', 'Proteins (g)', 'Fats (g)', 'Water (L)'])
    
    nutrition_logs = NutritionLog.query.filter(
        NutritionLog.user_id == user_id,
        NutritionLog.date >= start_date.date()
    ).order_by(NutritionLog.date.desc()).all()
    
    for log in nutrition_logs:
        ws5.append([
            log.date.strftime('%Y-%m-%d'),
            log.total_calories or 0,
            log.total_carbs or 0,
            log.total_proteins or 0,
            log.total_fats or 0,
            log.water_intake or 0
        ])
    
    for cell in ws5[3]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    # Save workbook
    wb.save(filename)
    return filename


def generate_chart_image(user_id, chart_type='calories'):
    """Generate chart image for reports"""
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'calories':
        # Get workout data
        start_date = datetime.utcnow() - timedelta(days=7)
        workouts = WorkoutLog.query.filter(
            WorkoutLog.user_id == user_id,
            WorkoutLog.date >= start_date
        ).order_by(WorkoutLog.date).all()
        
        dates = [w.date.strftime('%Y-%m-%d') for w in workouts]
        calories = [w.calories_burned for w in workouts]
        
        plt.bar(dates, calories, color='#3498DB')
        plt.xlabel('Date')
        plt.ylabel('Calories Burned')
        plt.title('Weekly Calorie Burn')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    # Save chart
    filename = os.path.join(Config.CHART_EXPORT_PATH, f'chart_{user_id}_{chart_type}.png')
    plt.savefig(filename)
    plt.close()
    
    return filename
