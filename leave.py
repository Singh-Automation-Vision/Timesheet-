# import smtplib
# from email.mime.text import MIMEText
# from pymongo import MongoClient
# from datetime import datetime

# def send_email_to_manager(employee_name, start_date, end_date, reason):
#     sender_email = "timesheetsystem2025@gmail.com"
#     sender_password = "mhuv nxdf ciqz igws"  
#     manager_email = "sudharshan@singhautomation.com"

#     subject = f"New Leave Request from {employee_name}"
#     body = f"""
#     Good day,

#     A new leave request has been submitted:

#     Employee: {employee_name}
#     From: {start_date}
#     To: {end_date}
#     Reason: {reason}

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

# def submit_leave_request(leave_data):
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     leave_collection = db["Leave_Requests"]

#     required_fields = ["employee_name", "leave_type", "start_date", "end_date", "reason"]
#     missing = [field for field in required_fields if not leave_data.get(field)]
#     if missing:
#         return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

#     try:
#         start = datetime.strptime(leave_data["start_date"], "%Y-%m-%d")
#         end = datetime.strptime(leave_data["end_date"], "%Y-%m-%d")
#     except ValueError:
#         return {"success": False, "message": "Date format should be YYYY-MM-DD"}

#     if end < start:
#         return {"success": False, "message": "End date must be after start date"}

#     days_requested = (end - start).days + 1

#     overlapping_request = leave_collection.find_one({
#         "employee_name": leave_data["employee_name"],
#         "status": {"$in": ["Pending", "Approved"]},
#         "$or": [
#             {
#                 "start_date": {"$lte": leave_data["end_date"]},
#                 "end_date": {"$gte": leave_data["start_date"]}
#             }
#         ]
#     })

#     if overlapping_request:
#         return {"success": False, "message": "A leave request already exists for the selected date range."}

#     employee = emp_collection.find_one({"name": leave_data["employee_name"]})
#     if not employee:
#         return {"success": False, "message": "Employee not found"}

#     if employee.get("Total_leave", 0) < days_requested:
#         return {"success": False, "message": "Not enough leave balance"}

#     leave_request = {
#         "employee_name": leave_data["employee_name"],
#         "leave_type": leave_data["leave_type"].lower(),
#         "start_date": leave_data["start_date"],
#         "end_date": leave_data["end_date"],
#         "reason": leave_data["reason"],
#         "status": "Pending",
#         "days_requested": days_requested,
#         "submitted_at": datetime.utcnow()
#     }

#     result = leave_collection.insert_one(leave_request)

#     # Send email to manager
#     send_email_to_manager(leave_data["employee_name"], leave_data["start_date"], leave_data["end_date"], leave_data["reason"])

#     return {
#         "success": True,
#         "message": "Leave request submitted and email sent to manager.",
#         "request_id": str(result.inserted_id)
#     }


# # # For testing
# if __name__ == "__main__":
#     leave_data = {
#         "employee_name": "clement",
#         "leave_type": "casual_leave",
#         "start_date": "2025-06-08",
#         "end_date": "2025-06-10",
#         "reason": "Medical leave"
#     }
#     result = submit_leave_request(leave_data)
#     print(result)


import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime

def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason):
    sender_email = "timesheetsystem2025@gmail.com"
    sender_password = "mhuv nxdf ciqz igws"  

    subject = f"New Leave Request from {employee_name}"
    body = f"""
    Good day,

    A new leave request has been submitted:

    Employee: {employee_name}
    From: {start_date}
    To: {end_date}
    Reason: {reason}

    Please log in to the system to review and take action.

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
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    emp_data_collection = db["Employee_data"]
    leave_collection = db["Leave_Requests"]

    required_fields = ["name", "email", "leaveType", "startDate", "endDate", "reason", "days", "submissionDate"]
    missing = [field for field in required_fields if not leave_data.get(field)]
    if missing:
        return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

    employee = emp_collection.find_one({"name": leave_data["name"]})
    if not employee:
        return {"success": False, "message": "Employee not found"}

    if employee.get("Total_leave", 0) < leave_data["days"]:
        return {"success": False, "message": "Not enough leave balance"}

    leave_request = {
        "employee_name": leave_data["name"],
        "leave_type": leave_data["leaveType"].lower(),
        "start_date": leave_data["startDate"],
        "end_date": leave_data["endDate"],
        "reason": leave_data["reason"],
        "status": "Pending",
        "days_requested": leave_data["days"],
        "submitted_at": leave_data["submissionDate"]  # Expecting just a date string like "2025-05-01"
    }

    result = leave_collection.insert_one(leave_request)

    # Fetch manager email using employee email
    emp_data = emp_data_collection.find_one({"email": leave_data["email"]})
    if emp_data and "manager_email" in emp_data:
        manager_email = emp_data["manager_email"]
        print (manager_email)
        send_email_to_manager(manager_email, leave_data["name"], leave_data["startDate"], leave_data["endDate"], leave_data["reason"])
    else:
        print("Manager email not found in Employee_data collection")

    return {
        "success": True,
        "message": "Leave request submitted and email sent to manager.",
        "request_id": str(result.inserted_id)
    }

# For testing
if __name__ == "__main__":
    leave_data = {
        "name": "Naveen",
        "email": "naveen@singhautomation.com",
        "days": 1,
        "startDate": "2025-06-10",
        "endDate": "2025-06-10",
        "leaveType": "Vacation",
        "reason": "Medical leave",
        "submissionDate": "2025-05-01"
    }
    result = submit_leave_request(leave_data)
    print(result)
