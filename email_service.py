import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from models import User, Report
from report_generator import ReportGenerator
from utils import EmailTemplate

class EmailService:
    """Service for sending email reports"""
    
    def __init__(self, app=None):
        self.app = app
        self.scheduler = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app"""
        self.app = app
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
        # Register cleanup function
        atexit.register(lambda: self.scheduler.shutdown())
        
        # Schedule email reports
        self.schedule_email_reports()
    
    def send_email_report(self, user, report_type='weekly', recipients=None, file_path=None):
        """Send email report to specified recipients"""
        try:
            # Generate report if file_path not provided
            if not file_path:
                file_path = self.generate_report_file(user, report_type)
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = ', '.join(recipients) if recipients else user.email
            msg['Subject'] = f"Your {report_type.title()} Lifestyle Report - {datetime.now().strftime('%B %d, %Y')}"
            
            # Get report data for email template
            report_data = self.get_report_data(user, report_type)
            
            # Create HTML email body
            html_body = EmailTemplate.generate_weekly_report_email(user.username, report_data)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach PDF report
            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(file_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
            server.starttls()
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            
            text = msg.as_string()
            server.sendmail(current_app.config['MAIL_USERNAME'], recipients, text)
            server.quit()
            
            # Log email sent
            self.log_email_sent(user.id, report_type, recipients, file_path)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def generate_report_file(self, user, report_type):
        """Generate report file and return path"""
        # Calculate date range
        end_date = datetime.now().date()
        if report_type == 'daily':
            start_date = end_date
        elif report_type == 'weekly':
            start_date = end_date - timedelta(days=7)
        else:  # monthly
            start_date = end_date - timedelta(days=30)
        
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(current_app.root_path, 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Generate PDF report
        file_path = os.path.join(reports_dir, f"{user.id}_{report_type}_{end_date}.pdf")
        generator = ReportGenerator(user, start_date, end_date)
        generator.generate_pdf_report(file_path)
        
        return file_path
    
    def get_report_data(self, user, report_type):
        """Get report data for email template"""
        # This would fetch actual data from database
        # For now, return sample data
        return {
            'total_workouts': 5,
            'total_calories_burned': 2500,
            'avg_daily_intake': 2100,
            'bmi': user.bmi or 23.5,
            'bmi_category': self.get_bmi_category(user.bmi),
            'consistency_score': 92,
            'insights': [
                "✓ Excellent workout consistency this week!",
                "✓ Your calorie balance is optimal for weight maintenance",
                "✓ Macro ratios are well-balanced",
                "! Water intake slightly below recommended 2.5L daily"
            ]
        }
    
    def get_bmi_category(self, bmi):
        """Get BMI category"""
        if not bmi:
            return "Unknown"
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def log_email_sent(self, user_id, report_type, recipients, file_path):
        """Log email sent in database"""
        try:
            report = Report(
                user_id=user_id,
                report_type=report_type,
                report_format='pdf',
                file_path=file_path,
                email_sent=True,
                email_recipients=','.join(recipients) if recipients else '',
                start_date=datetime.now().date() - timedelta(days=7),
                end_date=datetime.now().date()
            )
            
            from models import db
            db.session.add(report)
            db.session.commit()
        except Exception as e:
            print(f"Error logging email: {e}")
    
    def schedule_email_reports(self):
        """Schedule automatic email reports"""
        # Schedule daily reports at 8 AM
        self.scheduler.add_job(
            func=self.send_daily_reports,
            trigger=CronTrigger(hour=8, minute=0),
            id='daily_reports',
            name='Send daily reports',
            replace_existing=True
        )
        
        # Schedule weekly reports on Mondays at 9 AM
        self.scheduler.add_job(
            func=self.send_weekly_reports,
            trigger=CronTrigger(day_of_week=0, hour=9, minute=0),
            id='weekly_reports',
            name='Send weekly reports',
            replace_existing=True
        )
        
        # Schedule monthly reports on the 1st at 10 AM
        self.scheduler.add_job(
            func=self.send_monthly_reports,
            trigger=CronTrigger(day=1, hour=10, minute=0),
            id='monthly_reports',
            name='Send monthly reports',
            replace_existing=True
        )
    
    def send_daily_reports(self):
        """Send daily reports to all users who have opted in"""
        with self.app.app_context():
            # Get users who want daily reports
            users = User.query.filter_by(daily_reports=True).all()
            
            for user in users:
                try:
                    self.send_email_report(user, 'daily', [user.email])
                except Exception as e:
                    print(f"Error sending daily report to {user.username}: {e}")
    
    def send_weekly_reports(self):
        """Send weekly reports to all users who have opted in"""
        with self.app.app_context():
            # Get users who want weekly reports
            users = User.query.filter_by(weekly_reports=True).all()
            
            for user in users:
                try:
                    self.send_email_report(user, 'weekly', [user.email])
                except Exception as e:
                    print(f"Error sending weekly report to {user.username}: {e}")
    
    def send_monthly_reports(self):
        """Send monthly reports to all users who have opted in"""
        with self.app.app_context():
            # Get users who want monthly reports
            users = User.query.filter_by(monthly_reports=True).all()
            
            for user in users:
                try:
                    self.send_email_report(user, 'monthly', [user.email])
                except Exception as e:
                    print(f"Error sending monthly report to {user.username}: {e}")
    
    def send_custom_email_report(self, user_id, report_type, recipients, frequency='once'):
        """Send custom email report"""
        with self.app.app_context():
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            # Send immediate report
            success, message = self.send_email_report(user, report_type, recipients)
            
            if success and frequency != 'once':
                # Schedule recurring reports
                self.schedule_user_reports(user_id, report_type, recipients, frequency)
            
            return success, message
    
    def schedule_user_reports(self, user_id, report_type, recipients, frequency):
        """Schedule recurring reports for a specific user"""
        if frequency == 'daily':
            trigger = CronTrigger(hour=8, minute=0)
        elif frequency == 'weekly':
            trigger = CronTrigger(day_of_week=0, hour=9, minute=0)
        elif frequency == 'monthly':
            trigger = CronTrigger(day=1, hour=10, minute=0)
        else:
            return
        
        job_id = f"user_{user_id}_{report_type}_{frequency}"
        
        self.scheduler.add_job(
            func=self.send_user_report,
            trigger=trigger,
            args=[user_id, report_type, recipients],
            id=job_id,
            name=f"Send {frequency} {report_type} report to user {user_id}",
            replace_existing=True
        )
    
    def send_user_report(self, user_id, report_type, recipients):
        """Send report to specific user"""
        with self.app.app_context():
            user = User.query.get(user_id)
            if user:
                self.send_email_report(user, report_type, recipients)
    
    def cancel_user_reports(self, user_id, report_type, frequency):
        """Cancel scheduled reports for a user"""
        job_id = f"user_{user_id}_{report_type}_{frequency}"
        try:
            self.scheduler.remove_job(job_id)
            return True, "Reports cancelled successfully"
        except Exception as e:
            return False, f"Error cancelling reports: {e}"
    
    def get_scheduled_reports(self, user_id):
        """Get scheduled reports for a user"""
        jobs = []
        for job in self.scheduler.get_jobs():
            if f"user_{user_id}_" in job.id:
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None
                })
        return jobs

# Email templates
class EmailTemplates:
    """Email templates for different types of reports"""
    
    @staticmethod
    def daily_report_template(user_name, data):
        """Daily report email template"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Your Daily Lifestyle Report</h2>
                <p>Hello {user_name},</p>
                
                <p>Here's your daily lifestyle summary:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">Today's Highlights:</h3>
                    <ul>
                        <li>Workouts: {data.get('workouts', 0)}</li>
                        <li>Calories Burned: {data.get('calories_burned', 0)}</li>
                        <li>Calories Consumed: {data.get('calories_consumed', 0)}</li>
                        <li>Water Intake: {data.get('water_intake', 0)}L</li>
                    </ul>
                </div>
                
                <p>Keep up the great work!</p>
                
                <p>Best Regards,<br>
                Lifestyle Analytics Team</p>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def monthly_report_template(user_name, data):
        """Monthly report email template"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Your Monthly Lifestyle Report</h2>
                <p>Hello {user_name},</p>
                
                <p>Here's your comprehensive monthly analysis:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">Monthly Summary:</h3>
                    <ul>
                        <li>Total Workouts: {data.get('total_workouts', 0)}</li>
                        <li>Total Calories Burned: {data.get('total_calories_burned', 0)}</li>
                        <li>Average Daily Intake: {data.get('avg_daily_intake', 0)}</li>
                        <li>Consistency Score: {data.get('consistency_score', 0)}%</li>
                        <li>BMI Progress: {data.get('bmi_progress', 'N/A')}</li>
                    </ul>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3 style="color: #2c3e50;">Monthly Insights:</h3>
                    <ul>
                        {''.join([f'<li>{insight}</li>' for insight in data.get('insights', [])])}
                    </ul>
                </div>
                
                <p>Your detailed monthly report is attached as a PDF.</p>
                
                <p>Best Regards,<br>
                Lifestyle Analytics Team</p>
            </div>
        </body>
        </html>
        """