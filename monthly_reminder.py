import schedule
import time
import threading
from datetime import datetime, date
import pytz
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from datetime import timedelta
import calendar

IST = pytz.timezone('Asia/Kolkata')

def send_goal_completion_email(manager_email, employee_name, goal_title, completed=True):
    """Send email to manager when employee completes or misses goal"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_email or not smtp_password:
            print("Email configuration not found")
            return False
        
        if completed:
            subject = f"✅ Goal Completed: {employee_name}"
            status_color = "#10b981"
            status_icon = "✅"
            status_text = "COMPLETED"
            message_text = f"{employee_name} has successfully completed the goal"
        else:
            subject = f"⚠️ Goal Deadline Missed: {employee_name}"
            status_color = "#ef4444"
            status_icon = "⚠️"
            status_text = "DEADLINE MISSED"
            message_text = f"{employee_name} did not complete the goal by the deadline"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <div style="background: {status_color}; padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">{status_icon} Goal {status_text}</h1>
                    </div>
                    
                    <div style="padding: 30px 20px;">
                        <p style="font-size: 16px; margin-bottom: 20px;">{message_text}:</p>
                        
                        <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 0 0 10px 0;"><strong>Employee:</strong> {employee_name}</p>
                            <p style="margin: 0;"><strong>Goal:</strong> {goal_title}</p>
                        </div>
                        
                        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #64748b; font-size: 14px;">
                            Please review the goal details in the Performance Management System.
                        </p>
                    </div>
                    
                    <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 0 0 10px 10px;">
                        <p style="margin: 0; font-size: 12px; color: #64748b;">
                            This is an automated email from Performance Management System.<br>
                            Please do not reply to this email.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = smtp_email
        message["To"] = manager_email
        
        html_part = MIMEText(body, "html")
        message.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, manager_email, message.as_string())
        
        print(f"✅ Email sent to {manager_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False


def check_and_send_reminders(db):
    """Check if today is between 26th-31st and send reminders for incomplete goal sheets"""
    today = datetime.now(IST)
    
    # Only run between 26th and last day of month
    last_day = calendar.monthrange(today.year, today.month)[1]
    
    if not (26 <= today.day <= last_day):
        print(f"⏭️  Not between 26th-{last_day}th (today is {today.day}th) - skipping reminder")
        return
    
    print(f"📧 Running goal sheet completion check on {today.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Get all HR users for CC
        all_users = db.get_all_users()
        hr_users = [u for u in all_users if u['role'] == 'HR' and u.get('email')]
        hr_emails = [hr['email'] for hr in hr_users]
        
        print(f"📋 HR emails for CC: {hr_emails}")
        
        # Get all employees (including Manager, HR, VP, CMD)
        active_users = [u for u in all_users if u.get('email')]
        
        employee_incomplete_count = 0
        manager_notification_count = 0
        
        # Check each user's goal sheet for current month
        for user in active_users:
            # Get current month's goals
            current_year = today.year
            current_month = today.month
            current_quarter = ((current_month - 1) // 3) + 1
            
            goals = db.get_month_goals(user['id'], current_year, current_quarter, current_month)
            
            if not goals:
                # User has no goals for this month - skip
                continue
            
            # Check if goal sheet is incomplete
            incomplete_goals = []
            
            for goal in goals:
                is_incomplete = False
                missing_items = []
                
                # Check weekly achievements (check for None or 0)
                for week in range(1, 5):
                    week_achievement = goal.get(f'week{week}_achievement')
                    if week_achievement is None:
                        is_incomplete = True
                        missing_items.append(f"Week {week} achievement")
                
                # Check weekly remarks/ratings
                for week in range(1, 5):
                    week_remarks = goal.get(f'week{week}_remarks')
                    if not week_remarks or week_remarks == 0:
                        is_incomplete = True
                        missing_items.append(f"Week {week} rating")
                
                # Check monthly achievement
                monthly_achievement = goal.get('monthly_achievement')
                if monthly_achievement is None:
                    is_incomplete = True
                    missing_items.append("Monthly achievement")
                
                if is_incomplete:
                    incomplete_goals.append({
                        'goal_title': goal['goal_title'],
                        'goal_id': goal['goal_id'],
                        'department': goal.get('department', 'N/A'),
                        'kpi': goal.get('kpi', 'N/A'),
                        'monthly_target': goal.get('monthly_target', 0),
                        'missing_items': missing_items
                    })
            
            # If user has incomplete goals, send reminder
            if incomplete_goals:
                if user.get('email'):
                    # Send reminder to employee
                    send_goal_sheet_reminder_email(
                        user['email'],
                        user['name'],
                        incomplete_goals,
                        current_month,
                        current_year,
                        hr_emails
                    )
                    employee_incomplete_count += 1
                    print(f"📧 Sent reminder to {user['name']} ({user['email']}) - {len(incomplete_goals)} incomplete goals")
                
                # Notify manager about this employee's incomplete goals
                if user.get('manager_id'):
                    manager = db.get_user_by_id(user['manager_id'])
                    if manager and manager.get('email'):
                        send_manager_team_reminder_email(
                            manager['email'],
                            manager['name'],
                            user['name'],
                            incomplete_goals,
                            current_month,
                            current_year,
                            hr_emails
                        )
                        manager_notification_count += 1
                        print(f"📧 Notified manager {manager['name']} about {user['name']}'s incomplete goals")
        
        print(f"✅ Sent {employee_incomplete_count} employee reminders")
        print(f"✅ Sent {manager_notification_count} manager notifications")
        print(f"✅ All emails CC'd to {len(hr_emails)} HR member(s)")
        
    except Exception as e:
        print(f"❌ Error sending reminders: {str(e)}")
        import traceback
        traceback.print_exc()

def send_monthly_reminder_email(manager_email, manager_name, incomplete_goals):
    """Send email reminder to manager about incomplete goals"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_email or not smtp_password:
            print("Email configuration not found")
            return False
        
        subject = f"⏰ Monthly Reminder: Incomplete Goals in Your Team"
        
        # Build goals list HTML
        goals_html = ""
        for goal in incomplete_goals:
            goals_html += f"""
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 0 0 5px 0;"><strong>Employee:</strong> {goal['employee_name']}</p>
                <p style="margin: 0 0 5px 0;"><strong>Goal:</strong> {goal['goal_title']}</p>
                <p style="margin: 0;"><strong>Target:</strong> {goal['target']}</p>
            </div>
            """
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">⏰ Monthly Reminder</h1>
                    </div>
                    
                    <div style="padding: 30px 20px;">
                        <p style="font-size: 16px;">Hi {manager_name},</p>
                        
                        <p>This is a reminder that the following goals in your team have not been updated yet:</p>
                        
                        {goals_html}
                        
                        <p style="margin-top: 30px; padding: 15px; background: #e3f2fd; border-radius: 5px; border-left: 4px solid #2196f3;">
                            <strong>💡 Action Required:</strong> Please follow up with your team members to update their goal achievements.
                        </p>
                        
                        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #64748b; font-size: 14px;">
                            Log in to the Performance Management System to view and manage goals.
                        </p>
                    </div>
                    
                    <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 0 0 10px 10px;">
                        <p style="margin: 0; font-size: 12px; color: #64748b;">
                            This is an automated reminder from Performance Management System.<br>
                            Please do not reply to this email.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = smtp_email
        message["To"] = manager_email
        
        html_part = MIMEText(body, "html")
        message.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, manager_email, message.as_string())
        
        print(f"✅ Reminder email sent to {manager_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send reminder email: {str(e)}")
        return False

def send_goal_sheet_reminder_email(user_email, user_name, incomplete_goals, month, year, hr_emails):
    """Send reminder email to employee about incomplete goal sheet"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_email or not smtp_password:
            print("Email configuration not found")
            return False
        
        # Get month name
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        month_name = month_names[month]
        
        subject = f"⏰ Reminder: Complete Your {month_name} {year} Goal Sheet"
        
        # Build incomplete goals list HTML
        goals_html = ""
        for goal in incomplete_goals:
            missing_items_html = "<ul style='margin: 5px 0; padding-left: 20px;'>"
            for item in goal['missing_items']:
                missing_items_html += f"<li style='color: #dc2626;'>{item}</li>"
            missing_items_html += "</ul>"
            
            goals_html += f"""
            <div style="background: #fef3c7; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #f59e0b;">
                <p style="margin: 0 0 5px 0;"><strong>Goal:</strong> {goal['goal_title']}</p>
                <p style="margin: 0 0 5px 0;"><strong>Department:</strong> {goal['department']}</p>
                <p style="margin: 0 0 5px 0;"><strong>KPI:</strong> {goal['kpi']}</p>
                <p style="margin: 0 0 10px 0;"><strong>Target:</strong> {goal['monthly_target']}</p>
                <p style="margin: 0 0 5px 0; font-weight: bold; color: #dc2626;">Missing:</p>
                {missing_items_html}
            </div>
            """
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <div style="background: linear-gradient(135deg, #f59e0b 0%, #dc2626 100%); 
                                padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">⏰ Goal Sheet Incomplete</h1>
                    </div>
                    
                    <div style="padding: 30px 20px;">
                        <p style="font-size: 16px;">Hi {user_name},</p>
                        
                        <p>This is a reminder that your <strong>{month_name} {year}</strong> goal sheet is not yet complete.</p>
                        
                        <p style="background: #fee2e2; padding: 12px; border-radius: 5px; border-left: 4px solid #ef4444;">
                            <strong>⚠️ Action Required:</strong> Please update your goal sheet with achievements and ratings for all weeks by the end of this month.
                        </p>
                        
                        <h3 style="color: #dc2626; margin-top: 20px;">Incomplete Goals:</h3>
                        {goals_html}
                        
                        <div style="margin-top: 30px; padding: 15px; background: #dbeafe; border-radius: 5px; border-left: 4px solid #3b82f6;">
                            <strong>📋 What to complete:</strong>
                            <ul style="margin: 10px 0; padding-left: 20px;">
                                <li>Weekly achievements (Week 1, 2, 3, 4)</li>
                                <li>Weekly ratings (1-4 scale)</li>
                                <li>Monthly achievement (auto-calculated)</li>
                            </ul>
                        </div>
                        
                        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #64748b; font-size: 14px;">
                            Log in to the Performance Management System to complete your goal sheet.
                        </p>
                    </div>
                    
                    <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 0 0 10px 10px;">
                        <p style="margin: 0; font-size: 12px; color: #64748b;">
                            This is an automated reminder from Performance Management System.<br>
                            You will receive this reminder daily until your goal sheet is complete.<br>
                            Please do not reply to this email.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = smtp_email
        message["To"] = user_email
        
        # Add HR as CC
        if hr_emails:
            message["Cc"] = ", ".join(hr_emails)
        
        html_part = MIMEText(body, "html")
        message.attach(html_part)
        
        # Send to employee + CC to all HR
        recipients = [user_email] + hr_emails
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, recipients, message.as_string())
        
        print(f"✅ Goal sheet reminder sent to {user_email} (CC: HR)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send goal sheet reminder: {str(e)}")
        return False

def send_manager_team_reminder_email(manager_email, manager_name, employee_name, incomplete_goals, month, year, hr_emails):
    """Send reminder email to manager about employee's incomplete goal sheet"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_email or not smtp_password:
            print("Email configuration not found")
            return False
        
        # Get month name
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        month_name = month_names[month]
        
        subject = f"⚠️ Team Alert: {employee_name}'s {month_name} Goal Sheet Incomplete"
        
        # Build incomplete goals list HTML
        goals_html = ""
        for goal in incomplete_goals:
            missing_items_html = "<ul style='margin: 5px 0; padding-left: 20px;'>"
            for item in goal['missing_items']:
                missing_items_html += f"<li style='color: #dc2626;'>{item}</li>"
            missing_items_html += "</ul>"
            
            goals_html += f"""
            <div style="background: #fff7ed; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #f97316;">
                <p style="margin: 0 0 5px 0;"><strong>Goal:</strong> {goal['goal_title']}</p>
                <p style="margin: 0 0 5px 0;"><strong>Department:</strong> {goal['department']}</p>
                <p style="margin: 0 0 5px 0;"><strong>KPI:</strong> {goal['kpi']}</p>
                <p style="margin: 0 0 10px 0;"><strong>Target:</strong> {goal['monthly_target']}</p>
                <p style="margin: 0 0 5px 0; font-weight: bold; color: #dc2626;">Missing Updates:</p>
                {missing_items_html}
            </div>
            """
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <div style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); 
                                padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">⚠️ Team Member Goal Sheet Alert</h1>
                    </div>
                    
                    <div style="padding: 30px 20px;">
                        <p style="font-size: 16px;">Hi {manager_name},</p>
                        
                        <p>This is to inform you that <strong>{employee_name}</strong> from your team has not completed their <strong>{month_name} {year}</strong> goal sheet.</p>
                        
                        <div style="background: #fef2f2; padding: 15px; border-radius: 5px; border-left: 4px solid #ef4444; margin: 20px 0;">
                            <p style="margin: 0;"><strong>👤 Employee:</strong> {employee_name}</p>
                            <p style="margin: 10px 0 0 0;"><strong>📅 Period:</strong> {month_name} {year}</p>
                            <p style="margin: 10px 0 0 0;"><strong>📊 Incomplete Goals:</strong> {len(incomplete_goals)}</p>
                        </div>
                        
                        <h3 style="color: #dc2626; margin-top: 20px;">{employee_name}'s Incomplete Goals:</h3>
                        {goals_html}
                        
                        <div style="margin-top: 30px; padding: 15px; background: #dbeafe; border-radius: 5px; border-left: 4px solid #3b82f6;">
                            <strong>💡 Action Required:</strong>
                            <ul style="margin: 10px 0; padding-left: 20px;">
                                <li>Follow up with {employee_name} to complete their goal sheet</li>
                                <li>Ensure all weekly achievements are updated</li>
                                <li>Verify weekly ratings are provided (1-4 scale)</li>
                                <li>Goal sheet must be completed by end of month</li>
                            </ul>
                        </div>
                        
                        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #64748b; font-size: 14px;">
                            Log in to the Performance Management System to review and track your team's progress.
                        </p>
                    </div>
                    
                    <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 0 0 10px 10px;">
                        <p style="margin: 0; font-size: 12px; color: #64748b;">
                            This is an automated reminder from Performance Management System.<br>
                            You will receive this reminder daily until your team member's goal sheet is complete.<br>
                            Please do not reply to this email.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = smtp_email
        message["To"] = manager_email
        
        # Add HR as CC
        if hr_emails:
            message["Cc"] = ", ".join(hr_emails)
        
        html_part = MIMEText(body, "html")
        message.attach(html_part)
        
        # Send to manager + CC to all HR
        recipients = [manager_email] + hr_emails
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, recipients, message.as_string())
        
        print(f"✅ Manager alert sent to {manager_email} about {employee_name} (CC: HR)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send manager alert: {str(e)}")
        return False
    
def test_send_reminder(db, test_email=None):
    """Test function to send reminder immediately"""
    try:
        if test_email:
            # Send to specific email
            incomplete_goals = [
                {
                    'goal_title': 'Test Goal 1',
                    'goal_id': 'test_1',
                    'department': 'Test Dept',
                    'kpi': 'Test KPI',
                    'monthly_target': 100,
                    'missing_items': ['Week 1 achievement', 'Week 2 rating', 'Week 3 achievement']
                },
                {
                    'goal_title': 'Test Goal 2',
                    'goal_id': 'test_2',
                    'department': 'Test Dept 2',
                    'kpi': 'Test KPI 2',
                    'monthly_target': 200,
                    'missing_items': ['Week 4 achievement', 'Monthly achievement']
                }
            ]
            
            # Get HR emails
            all_users = db.get_all_users()
            hr_emails = [u['email'] for u in all_users if u['role'] == 'HR' and u.get('email')]
            
            today = datetime.now(IST)
            send_goal_sheet_reminder_email(
                test_email,
                "Test User",
                incomplete_goals,
                today.month,
                today.year,
                hr_emails
            )
            print(f"✅ Test reminder email sent to {test_email}")
        else:
            # Send to all users with incomplete goals
            check_and_send_reminders(db)
            print("✅ Test reminders sent to all users with incomplete goal sheets")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

def start_reminder_scheduler(db):
    """Start background scheduler for reminders and deadline checks"""
    
    # Monthly reminder on 26th at 9:00 AM
    schedule.every().day.at("09:00").do(check_and_send_reminders, db)
    

    
    print("🕐 Scheduler started:")
    print("  📧 Monthly reminders: 26th at 9:00 AM")
   
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()