import smtplib
from datetime import datetime
from email.message import EmailMessage
from email.mime.text import MIMEText
import logging
from pymongo import MongoClient

from Emp_timesheet import get_manager_details


def send_safety_matrix_prompt(employee_email, employee_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = "Please Fill Out Your Daily Safety Matrix"
        msg['From'] = "timesheetsystem2025@gmail.com"
        msg['To'] = employee_email

        msg.set_content(
            f"Hi {employee_name},\n\n"
            f"Please remember to follow all safety protocols during your workday.\n"
            f"• Wear appropriate PPE.\n"
            f"• Follow operational guidelines.\n"
            f"• Report any hazards immediately.\n\n"
            f"Stay safe!\n\n"
            f"Regards,\n"
            f"Safety & Timesheet Management System"
        )

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "timesheetsystem2025@gmail.com"
        sender_password = "mhuv nxdf ciqz igws"  # Use App Password

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        logging.info(f"📧 Safety matrix prompt sent to {employee_email}")
        print(f"📧 Prompt email sent to {employee_email}")

    except Exception as e:
        logging.error(f"❌ Failed to send safety matrix prompt: {e}")
        print(f"❌ Error sending prompt email: {e}")


def send_alert_safety_email(user_input_AM, flag_count, manager, mail):
    sender_email = "timesheetsystem2025@gmail.com"
    receiver_email = mail
    smtp_password = "mhuv nxdf ciqz igws"  # Gmail App Password

    subject = "⚠ Safety Alert: Employee Safety Issue"

    # Build list of failed checks
    failed_checks = [
        question for question, answer in user_input_AM.get("safety_matrix", {}).items()
        if str(answer).strip().lower() == "red"
    ]
    failed_list = "\n".join(f"- {q}" for q in failed_checks)

    body = (
        f"Dear {manager},\n\n"
        f"Employee {user_input_AM.get('employee_name')} has {flag_count} safety issue(s) flagged today:\n\n"
        f"{failed_list}\n\n"
        f"Please review and take appropriate action.\n\n"
        f"Best regards,\n"
        f"Timesheet System"
    )

    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"📨 Safety alert email sent to {receiver_email}")
        return "Success"
    except Exception as e:
        print(f"❌ Failed to send safety alert email: {e}")
        return f"Failed to send safety alert email: {e}"


def review_safety(user_input_AM, manager, mail):    
    try:
        performance_params = [
            user_input_AM["safety_matrix"]["Are you wearing all required Personal Protective Equipment (PPE) for your task today?"],
            user_input_AM["safety_matrix"]["Have you inspected your tools, machines, or equipment for any visible damage or malfunction?"],
            user_input_AM["safety_matrix"]["Is your work area clean, organized, and free from slip/trip hazards?"],
            user_input_AM["safety_matrix"]["Are all emergency stop buttons and safety interlocks functional and accessible?"],
            user_input_AM["safety_matrix"]["Are all wires, cables, and hoses properly managed to avoid entanglement or tripping?"],
            user_input_AM["safety_matrix"]["Have you seen or experienced anything unsafe today that should be reported?"],
            user_input_AM["safety_matrix"]["Have you reviewed and acknowledged today's safety briefing or posted instructions?"],
        ]

        # Normalize input to lowercase and strip whitespace
        red_count = sum(1 for item in performance_params if item.strip().lower() == "red")

        if red_count >= 1:
            send_alert_safety_email(user_input_AM, red_count, manager, mail)
        else:
            print("✅ No safety issues flagged.")
 
    except KeyError as e:
        return(f"KeyError: Missing field {e}")

# def review_safety(user_input_AM, manager, mail):    
    # try:
    #     performance_params = [
    #         user_input_AM["safety_matrix"]["Are you wearing all required Personal Protective Equipment (PPE) for your task today?"],
    #         user_input_AM["safety_matrix"]["Have you inspected your tools, machines, or equipment for any visible damage or malfunction?"],
    #         user_input_AM["safety_matrix"]["Is your work area clean, organized, and free from slip/trip hazards?"],
    #         user_input_AM["safety_matrix"]["Are all emergency stop buttons and safety interlocks functional and accessible?"],
    #         user_input_AM["safety_matrix"]["Are all wires, cables, and hoses properly managed to avoid entanglement or tripping?"],
    #         user_input_AM["safety_matrix"]["Have you seen or experienced anything unsafe today that should be reported?"],
    #         user_input_AM["safety_matrix"]["Have you reviewed and acknowledged today's safety briefing or posted instructions?"],
    #     ]

    #     # Normalize answers
    #     normalized = [str(ans).strip().lower() for ans in performance_params]
    #     red_count = normalized.count("Red")

    #     if red_count >= 1:
    #         print(f"⚠️ Found {red_count} RED flag(s). Sending alert to {manager}")
    #         send_alert_safety_email(user_input_AM, red_count, manager, mail)
    #     else:
    #         print(f"✅ No safety issues for {user_input_AM['employee_name']}")

    # except KeyError as e:
    #     print(f"❌ KeyError in review_safety: Missing field {e}")


def get_latest_date_for_safety(employee_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_am = db["Employee_AM"]

    latest_am_entry = collection_am.find_one(
        {"employee_name": employee_name},
        sort=[("date", -1)]
    )

    if latest_am_entry and "date" in latest_am_entry:
        try:
            date_val = latest_am_entry["date"]
            if isinstance(date_val, datetime):
                return date_val.strftime("%Y-%m-%d")
            elif isinstance(date_val, str):
                return datetime.strptime(date_val, "%Y-%m-%d").strftime("%Y-%m-%d")
        except Exception as e:
            print("Error parsing AM date:", e)
            return None
    return None


def save_safety_matrix(employee_name, date, safety_ratings):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_AM"]
    employee_collection = db["Employee_data"]

    recent_date = get_latest_date_for_safety(employee_name)
    if not recent_date:
        logging.warning(f"No recent AM sheet found for {employee_name}. Cannot save safety matrix.")
        return

    result = collection.update_one(
        {"employee_name": employee_name, "date": recent_date},
        {"$set": {"safety_matrix": safety_ratings}}
    )
    emp_name = employee_name
    manager, mail = get_manager_details(emp_name)
    user_input = collection.find_one({"employee_name": employee_name, "date": recent_date})

    # Call the review performance function
    review_safety(user_input, manager, mail)
    # Fetch employee and manager info
    # employee = employee_collection.find_one({"name": employee_name})
    # if employee:
    #     employee_email = employee.get("email")
    #     manager_name = employee.get("manager_name")
    #     manager_email = employee.get("manager_email")

    #     user_input_AM = {
    #         "employee_name": employee_name,
    #         "safety_matrix": safety_ratings
    #     }

    #     # Optional confirmation to employee
    #     # if employee_email:
    #     #     send_safety_matrix_prompt(employee_email, employee_name)

    #     # Check for issues and notify manager
    #     if manager_email and manager_name:
    #         print(f"🔍 Triggering safety review for {employee_name}")
    #         review_safety(user_input_AM, manager_name, manager_email)

    # if result.modified_count:
    #     logging.info(f"✅ Safety matrix updated for {employee_name} on {recent_date}")
    #     print(f"✅ Safety matrix updated for {employee_name} on {recent_date}")
    # else:
    #     logging.warning(f"⚠️ No updates made. Entry may already be up-to-date.")
    #     print(f"⚠️ No updates made for {employee_name}")



# if __name__ == "__main__":
#     employee_name = "John Doe"
#     manager_name = "Jane Smith"
#     manager_email = "naveen@singhautomation.com"  # Replace with real manager email

#     user_input_AM = {
#         "employee_name": employee_name,
#         "safety_matrix": {
#             "Are you wearing all required Personal Protective Equipment (PPE) for your task today?": "Green",
#             "Have you inspected your tools, machines, or equipment for any visible damage or malfunction?":"Red",
#             "Is your work area clean, organized, and free from slip/trip hazards?": "Green",
#             "Are all emergency stop buttons and safety interlocks functional and accessible?": "Green",
#             "Are all wires, cables, and hoses properly managed to avoid entanglement or tripping?": "Green",
#             "Have you seen or experienced anything unsafe today that should be reported?": "Green",
#             "Have you reviewed and acknowledged today's safety briefing or posted instructions?": "Green"
#         }
#     }

#     # Trigger manual safety alert
#     review_safety(user_input_AM, manager_name, manager_email)







