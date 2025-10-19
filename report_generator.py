from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
import openpyxl
from openpyxl.chart import LineChart, BarChart, PieChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime, date, timedelta
import os
import json
from io import BytesIO
import base64

class ReportGenerator:
    """Generate PDF and Excel reports for lifestyle analytics"""
    
    def __init__(self, user, start_date, end_date):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for reports"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#34495e')
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        ))

    def generate_pdf_report(self, file_path):
        """Generate PDF report"""
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        story = []
        
        # Title
        story.append(Paragraph("Lifestyle Analytics Report", self.styles['CustomTitle']))
        story.append(Paragraph(f"Generated for: {self.user.username}", self.styles['BodyText']))
        story.append(Paragraph(f"Date Range: {self.start_date} to {self.end_date}", self.styles['BodyText']))
        story.append(Spacer(1, 20))
        
        # User Summary
        story.append(Paragraph("User Profile Summary", self.styles['SectionHeader']))
        user_data = self.get_user_summary_data()
        story.append(self.create_user_summary_table(user_data))
        story.append(Spacer(1, 20))
        
        # Workout Analysis
        story.append(Paragraph("Workout Analysis", self.styles['SectionHeader']))
        workout_data = self.get_workout_analysis_data()
        story.append(self.create_workout_analysis_table(workout_data))
        story.append(Spacer(1, 20))
        
        # Nutrition Analysis
        story.append(Paragraph("Nutrition Analysis", self.styles['SectionHeader']))
        nutrition_data = self.get_nutrition_analysis_data()
        story.append(self.create_nutrition_analysis_table(nutrition_data))
        story.append(Spacer(1, 20))
        
        # Health Metrics
        story.append(Paragraph("Health Metrics", self.styles['SectionHeader']))
        health_data = self.get_health_metrics_data()
        story.append(self.create_health_metrics_table(health_data))
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Personalized Recommendations", self.styles['SectionHeader']))
        recommendations = self.get_recommendations()
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['BodyText']))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              self.styles['BodyText']))
        
        doc.build(story)
        return file_path

    def generate_excel_report(self, file_path):
        """Generate Excel report with multiple sheets"""
        wb = openpyxl.Workbook()
        
        # Remove default sheet
        wb.remove(wb.active)
        
        # User Profile Sheet
        self.create_user_profile_sheet(wb)
        
        # Workout Data Sheet
        self.create_workout_data_sheet(wb)
        
        # Nutrition Data Sheet
        self.create_nutrition_data_sheet(wb)
        
        # Daily Stats Sheet
        self.create_daily_stats_sheet(wb)
        
        # Summary Sheet
        self.create_summary_sheet(wb)
        
        # Charts Sheet
        self.create_charts_sheet(wb)
        
        wb.save(file_path)
        return file_path

    def create_user_profile_sheet(self, wb):
        """Create user profile sheet"""
        ws = wb.create_sheet("User Profile")
        
        # Headers
        headers = ["Metric", "Value", "Category", "Target Range"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # User data
        user_data = [
            ["Age", self.user.age or "N/A", "Demographics", "18-65"],
            ["Gender", self.user.gender or "N/A", "Demographics", "Male/Female/Other"],
            ["Weight (kg)", self.user.weight or "N/A", "Physical", "45-100 kg"],
            ["Height (m)", self.user.height or "N/A", "Physical", "1.5-2.0 m"],
            ["BMI", f"{self.user.bmi:.1f}" if self.user.bmi else "N/A", "Health", "18.5-24.9"],
            ["Body Fat %", f"{self.user.fat_percentage:.1f}%" if self.user.fat_percentage else "N/A", "Health", "10-25%"],
            ["Experience Level", self.get_experience_level_text(), "Fitness", "Beginner-Advanced"]
        ]
        
        for row, data in enumerate(user_data, 2):
            for col, value in enumerate(data, 1):
                ws.cell(row=row, column=col, value=value)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

    def create_workout_data_sheet(self, wb):
        """Create workout data sheet"""
        ws = wb.create_sheet("Workout Data")
        
        # Headers
        headers = ["Date", "Type", "Duration (min)", "Calories Burned", "Max BPM", "Avg BPM", "Resting BPM"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="28a745", end_color="28a745", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # Sample workout data (in real implementation, fetch from database)
        workout_data = self.get_sample_workout_data()
        
        for row, data in enumerate(workout_data, 2):
            for col, value in enumerate(data, 1):
                ws.cell(row=row, column=col, value=value)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 30)
            ws.column_dimensions[column_letter].width = adjusted_width

    def create_nutrition_data_sheet(self, wb):
        """Create nutrition data sheet"""
        ws = wb.create_sheet("Nutrition Data")
        
        # Headers
        headers = ["Date", "Meals", "Calories", "Carbs (g)", "Proteins (g)", "Fats (g)", "Water (L)"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="17a2b8", end_color="17a2b8", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # Sample nutrition data
        nutrition_data = self.get_sample_nutrition_data()
        
        for row, data in enumerate(nutrition_data, 2):
            for col, value in enumerate(data, 1):
                ws.cell(row=row, column=col, value=value)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            ws.column_dimensions[column_letter].width = adjusted_width

    def create_daily_stats_sheet(self, wb):
        """Create daily stats sheet"""
        ws = wb.create_sheet("Daily Stats")
        
        # Headers
        headers = ["Date", "Calories Burned", "Calories Consumed", "Caloric Balance", "Workout Duration", "Water Intake", "Consistency Score"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="ffc107", end_color="ffc107", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # Sample daily stats
        daily_stats = self.get_sample_daily_stats()
        
        for row, data in enumerate(daily_stats, 2):
            for col, value in enumerate(data, 1):
                ws.cell(row=row, column=col, value=value)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            ws.column_dimensions[column_letter].width = adjusted_width

    def create_summary_sheet(self, wb):
        """Create summary sheet with key metrics"""
        ws = wb.create_sheet("Summary")
        
        # Title
        ws.merge_cells('A1:D1')
        ws['A1'] = f"Lifestyle Analytics Summary - {self.user.username}"
        ws['A1'].font = Font(size=16, bold=True)
        ws['A1'].alignment = Alignment(horizontal="center")
        
        # Summary data
        summary_data = self.get_summary_data()
        
        row = 3
        for category, metrics in summary_data.items():
            # Category header
            ws.cell(row=row, column=1, value=category).font = Font(bold=True, size=12)
            row += 1
            
            # Metrics
            for metric, value in metrics.items():
                ws.cell(row=row, column=1, value=metric)
                ws.cell(row=row, column=2, value=value)
                row += 1
            
            row += 1  # Space between categories

    def create_charts_sheet(self, wb):
        """Create charts sheet with visualizations"""
        ws = wb.create_sheet("Charts")
        
        # Add some sample charts (in real implementation, create actual charts)
        ws['A1'] = "Charts and Visualizations"
        ws['A1'].font = Font(size=16, bold=True)
        
        # This would contain actual chart creation code
        # For now, just add placeholder text
        ws['A3'] = "BMI Trend Chart"
        ws['A4'] = "Calorie Balance Chart"
        ws['A5'] = "Macro Distribution Chart"
        ws['A6'] = "Workout Type Distribution Chart"

    # Helper methods for data retrieval
    def get_user_summary_data(self):
        """Get user summary data for PDF"""
        return {
            "Username": self.user.username,
            "Email": self.user.email,
            "Age": self.user.age or "N/A",
            "Gender": self.user.gender or "N/A",
            "Weight": f"{self.user.weight} kg" if self.user.weight else "N/A",
            "Height": f"{self.user.height} m" if self.user.height else "N/A",
            "BMI": f"{self.user.bmi:.1f}" if self.user.bmi else "N/A",
            "Body Fat %": f"{self.user.fat_percentage:.1f}%" if self.user.fat_percentage else "N/A"
        }

    def get_workout_analysis_data(self):
        """Get workout analysis data"""
        return {
            "Total Workouts": "15",
            "Total Calories Burned": "3,500",
            "Average Duration": "45 minutes",
            "Most Common Type": "Cardio",
            "Consistency Score": "85%"
        }

    def get_nutrition_analysis_data(self):
        """Get nutrition analysis data"""
        return {
            "Average Daily Calories": "2,100",
            "Average Carbs": "250g",
            "Average Proteins": "120g",
            "Average Fats": "80g",
            "Average Water Intake": "2.2L"
        }

    def get_health_metrics_data(self):
        """Get health metrics data"""
        return {
            "Current BMI": f"{self.user.bmi:.1f}" if self.user.bmi else "N/A",
            "BMI Category": self.get_bmi_category(),
            "Body Fat %": f"{self.user.fat_percentage:.1f}%" if self.user.fat_percentage else "N/A",
            "Fitness Level": self.get_experience_level_text()
        }

    def get_recommendations(self):
        """Get personalized recommendations"""
        recommendations = []
        
        if self.user.bmi and self.user.bmi > 25:
            recommendations.append("Consider increasing cardio workouts to help with weight management")
        
        if self.user.fat_percentage and self.user.fat_percentage > 25:
            recommendations.append("Focus on strength training to build muscle mass")
        
        recommendations.append("Maintain consistent workout schedule for better results")
        recommendations.append("Ensure adequate protein intake for muscle recovery")
        recommendations.append("Stay hydrated by drinking at least 2.5L of water daily")
        
        return recommendations

    def get_experience_level_text(self):
        """Get experience level as text"""
        if self.user.experience_level == 1:
            return "Beginner"
        elif self.user.experience_level == 2:
            return "Intermediate"
        elif self.user.experience_level == 3:
            return "Advanced"
        else:
            return "N/A"

    def get_bmi_category(self):
        """Get BMI category"""
        if not self.user.bmi:
            return "Unknown"
        if self.user.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.user.bmi < 25:
            return "Normal"
        elif 25 <= self.user.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_sample_workout_data(self):
        """Get sample workout data for Excel"""
        data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            if current_date.weekday() < 5:  # Weekdays
                data.append([
                    current_date.strftime('%Y-%m-%d'),
                    'Cardio',
                    45,
                    350,
                    160,
                    140,
                    70
                ])
            current_date += timedelta(days=1)
        return data

    def get_sample_nutrition_data(self):
        """Get sample nutrition data for Excel"""
        data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            data.append([
                current_date.strftime('%Y-%m-%d'),
                3,
                2100,
                250,
                120,
                80,
                2.2
            ])
            current_date += timedelta(days=1)
        return data

    def get_sample_daily_stats(self):
        """Get sample daily stats for Excel"""
        data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            calories_burned = 300 + (current_date.weekday() * 50)
            calories_consumed = 2100
            data.append([
                current_date.strftime('%Y-%m-%d'),
                calories_burned,
                calories_consumed,
                calories_consumed - calories_burned,
                45,
                2.2,
                85
            ])
            current_date += timedelta(days=1)
        return data

    def get_summary_data(self):
        """Get summary data for Excel"""
        return {
            "User Profile": {
                "Username": self.user.username,
                "Email": self.user.email,
                "Age": self.user.age or "N/A",
                "Gender": self.user.gender or "N/A"
            },
            "Physical Metrics": {
                "Weight": f"{self.user.weight} kg" if self.user.weight else "N/A",
                "Height": f"{self.user.height} m" if self.user.height else "N/A",
                "BMI": f"{self.user.bmi:.1f}" if self.user.bmi else "N/A",
                "Body Fat %": f"{self.user.fat_percentage:.1f}%" if self.user.fat_percentage else "N/A"
            },
            "Activity Summary": {
                "Total Workouts": "15",
                "Total Calories Burned": "3,500",
                "Average Duration": "45 minutes",
                "Consistency Score": "85%"
            },
            "Nutrition Summary": {
                "Average Daily Calories": "2,100",
                "Average Carbs": "250g",
                "Average Proteins": "120g",
                "Average Fats": "80g"
            }
        }

    # Table creation methods for PDF
    def create_user_summary_table(self, data):
        """Create user summary table for PDF"""
        table_data = [["Metric", "Value"]]
        for key, value in data.items():
            table_data.append([key, str(value)])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def create_workout_analysis_table(self, data):
        """Create workout analysis table for PDF"""
        table_data = [["Metric", "Value"]]
        for key, value in data.items():
            table_data.append([key, str(value)])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def create_nutrition_analysis_table(self, data):
        """Create nutrition analysis table for PDF"""
        table_data = [["Metric", "Value"]]
        for key, value in data.items():
            table_data.append([key, str(value)])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17a2b8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def create_health_metrics_table(self, data):
        """Create health metrics table for PDF"""
        table_data = [["Metric", "Value"]]
        for key, value in data.items():
            table_data.append([key, str(value)])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffc107')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table