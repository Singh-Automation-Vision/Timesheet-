import json
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText

# Send the alert mail to the manager if the performance is red
def send_alert_email(user_input_PM, red_count,manager,mail):
    sender_email = "timesheetsystem2025@gmail.com"
    receiver_email = mail
    smtp_email = sender_email  # Using the same email for SMTP login
    smtp_password = "mhuv nxdf ciqz igws"  # Use an app password instead of your actual password

    subject = "⚠ Alert: Employee Performance Issue"
    body = f"Dear {manager},\n\nEmployee {user_input_PM['employee_name']} has {red_count} performance issues marked as RED today.\nPlease review the timesheet for further action.\n\nBest regards,\nTimesheet System"

    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)  # Use sender email and app password
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Check if any of the performance matrices is red  
def review_performance(user_input_PM,manager,mail):    
    try:
         performance_params = [
             user_input_PM["ratings"]["Performance of the Day"],
             user_input_PM["ratings"]["First Time Quality"],
             user_input_PM["ratings"]["On-Time Delivery"],
             user_input_PM["ratings"]["Engagement and Support"]
         ]
         
         red_count = performance_params.count("Red")
         #print(f"Red Count: {red_count}")
 
         if red_count >= 1:
             send_alert_email(user_input_PM, red_count, manager, mail)
         else:
             pass  # Explicitly do nothing (optional)
 
    except KeyError as e:
         print(f"KeyError: Missing field {e}")
