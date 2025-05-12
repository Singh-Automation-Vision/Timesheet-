import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime


# def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason, leave_type, hours):
#     sender_email = "timesheetsystem2025@gmail.com"
#     sender_password = "mhuv nxdf ciqz igws"  # Use your actual password or app password here

#     subject = f"New Leave Request from {employee_name}"
#     body = f"""
#     Good day,

#     A new leave request has been submitted:

#     Employee: {employee_name}
#     From: {start_date}
#     To: {end_date}
#     Reason: {reason}
#     Leave Type: {leave_type}
#     Hours Requested: {hours} hours

#     Please log in to the system to review and take action.

#     Regards,
#     Timesheet System
#     """

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = sender_email
#     msg["To"] = manager_email

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, manager_email, msg.as_string())
#         print("Email sent successfully to manager.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

import smtplib
from email.mime.text import MIMEText

def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason, leave_type, hours):
    sender_email = "timesheetsystem2025@gmail.com"
    sender_password = "mhuv nxdf ciqz igws"  # Gmail App Password

    subject = f"New Leave Request from {employee_name}"
    body = f"""\
Good day,

A new leave request has been submitted:

Employee: {employee_name}
From: {start_date}
To: {end_date}
Reason: {reason}
Leave Type: {leave_type}
Hours Requested: {hours} hours
please login as : f"Username: admin\n"
f"Password: admin\n\n"

Please login as an admin to approve or reject the leave request:
https://satimesheet.netlify.app/login

Regards,
Timesheet System
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = manager_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, manager_email, msg.as_string())
        print("Email sent successfully to manager.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def submit_leave_request(leave_data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    # client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    emp_data_collection = db["Employee_data"]
    leave_collection = db["Leave_Requests"]

    required_fields = ["name", "leaveType", "startDate", "endDate", "reason", "submissionDate"]
    missing = [field for field in required_fields if not leave_data.get(field)]
    if missing:
        return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

    # If leave is provided in days, convert to hours (assuming 1 day = 8 hours)
    if 'days' in leave_data and leave_data['days']:
        requested_hours = leave_data['days'] * 8
    elif 'hours' in leave_data and leave_data['hours']:
        requested_hours = leave_data['hours']
    else:
        return {"success": False, "message": "No leave duration specified (hours or days)"}

    employee = emp_collection.find_one({"name": leave_data["name"]})
    if not employee:
        return {"success": False, "message": "Employee not found"}

    # Check if the leave type is valid and if there's enough leave balance
    if leave_data["leaveType"] == "Medical Leave":
        sick_leave_hours = employee.get("Sick_leave_hours", 0)
        if sick_leave_hours < requested_hours:
            return {"success": False, "message": "Not enough sick leave hours"}
        # else:
        #     # Deduct from sick leave hours
        #     emp_collection.update_one({"name": leave_data["name"]}, {"$inc": {"Sick_leave_hours": -requested_hours}})
    elif leave_data["leaveType"] != "Medical Leave":
        casual_leave_hours = employee.get("Casual_leave_hours", 0)
        if casual_leave_hours < requested_hours:
            return {"success": False, "message": "Not enough casual leave hours"}
        # else:
        #     # Deduct from casual leave hours
        #     emp_collection.update_one({"name": leave_data["name"]}, {"$inc": {"Casual_leave_hours": -requested_hours}})
    else:
        return {"success": False, "message": "Invalid leave type"}

    # Insert leave request to DB (pending for approval)
    leave_request = {
        "employee_name": leave_data["name"],
        "leave_type": leave_data["leaveType"],
        "start_date": leave_data["startDate"],
        "end_date": leave_data["endDate"],
        "reason": leave_data["reason"],
        "status": "Pending",  # Admin needs to approve this
        "hours_requested": requested_hours,
        "submitted_at": leave_data["submissionDate"]
    }

    result = leave_collection.insert_one(leave_request)

    # Send email to manager for approval
    emp_data = emp_data_collection.find_one({"name": leave_data["name"]})
    if emp_data and "manager_email" in emp_data:
        manager_email = emp_data["manager_email"]
        print(manager_email)  # For debugging purposes
        send_email_to_manager(manager_email, leave_data["name"], leave_data["startDate"], leave_data["endDate"], leave_data["reason"], leave_data["leaveType"], requested_hours)
        return {
            "success": True,
            "message": "Leave request submitted and email sent to manager.",
            "request_id": str(result.inserted_id)
        }
    else:
        print("Manager email not found in Employee_data collection")
        return {
            "success": False,
            "message": "Manager email not found. Leave request not submitted.",
            "request_id": None
        }
    

# Main function for testing
# if __name__ == "__main__":
#     # Sample leave data for testing (with days instead of hours)
#     leave_data = {
#         "name": "Sudharshan", 
#         "leaveType": "Medical Leave", 
#         "startDate": "2025-06-15", 
#         "endDate": "2025-06-15", 
#         "reason": "Medical",
#         "days": 2,  
#         "submissionDate": str(datetime.now().date())  
#     }

#     # Call the function to submit the leave request
#     result = submit_leave_request(leave_data)

#     # Print the result of the leave request submission
#     print(result)
