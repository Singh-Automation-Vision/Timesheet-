# # # import smtplib
# # # from email.mime.text import MIMEText
# # # from pymongo import MongoClient
# # # from datetime import datetime

# # # def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason, leave_type):
# # #     sender_email = "timesheetsystem2025@gmail.com"
# # #     sender_password = "mhuv nxdf ciqz igws"  

# # #     subject = f"New Leave Request from {employee_name}"
# # #     body = f"""
# # #     Good day,

# # #     A new leave request has been submitted:

# # #     Employee: {employee_name}
# # #     From: {start_date}
# # #     To: {end_date}
# # #     Reason: {reason}
# # #     Leave Type:{leave_type}

# # #     Please log in to the system to review and take action.

# # #     Regards,
# # #     Timesheet System
# # #     """

# # #     msg = MIMEText(body)
# # #     msg["Subject"] = subject
# # #     msg["From"] = sender_email
# # #     msg["To"] = manager_email

# # #     try:
# # #         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
# # #             server.login(sender_email, sender_password)
# # #             server.sendmail(sender_email, manager_email, msg.as_string())
# # #         print("Email sent successfully to manager.")
# # #     except Exception as e:
# # #         print(f"Failed to send email: {e}")

# # # def submit_leave_request(leave_data):
# # #     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
# # #     db = client["Timesheet"]
# # #     emp_collection = db["Employee_leavedetails"]
# # #     emp_data_collection = db["Employee_data"]
# # #     leave_collection = db["Leave_Requests"]

# # #     required_fields = ["name", "leaveType", "startDate", "endDate", "reason", "days", "submissionDate"]
# # #     missing = [field for field in required_fields if not leave_data.get(field)]
# # #     if missing:
# # #         return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

# # #     employee = emp_collection.find_one({"name": leave_data["name"]})
# # #     if not employee:
# # #         return {"success": False, "message": "Employee not found"}

# # #     if employee.get("Total_leave", 0) < leave_data["days"]:
# # #         return {"success": False, "message": "Not enough leave balance"}

# # #     leave_request = {
# # #         "employee_name": leave_data["name"],
# # #         "leave_type": leave_data["leaveType"].lower(),
# # #         "start_date": leave_data["startDate"],
# # #         "end_date": leave_data["endDate"],
# # #         "reason": leave_data["reason"],
# # #         "status": "Pending",
# # #         "days_requested": leave_data["days"],
# # #         "submitted_at": leave_data["submissionDate"]
# # #     }

# # #     result = leave_collection.insert_one(leave_request)

# # #     # Get manager's email using employee's name
# # #     emp_data = emp_data_collection.find_one({"name": leave_data["name"]})
# # #     if emp_data and "manager_email" in emp_data:
# # #         manager_email = emp_data["manager_email"]
# # #         send_email_to_manager(manager_email, leave_data["name"], leave_data["startDate"], leave_data["endDate"], leave_data["reason"], leave_data["leaveType"])
# # #     else:
# # #         print("Manager email not found in Employee_data collection")

# # #     return {
# # #         "success": True,
# # #         "message": "Leave request submitted and email sent to manager.",
# # #         "request_id": str(result.inserted_id)
# # #     }


# # # # For testing
# # # # if __name__ == "__main__":
# # # #     leave_data = {
# # # #         "name": "Sudharshan",
# # # #         "days": 1,
# # # #         "startDate": "2025-07-17",
# # # #         "endDate": "2025-07-17",
# # # #         "leaveType": "Vacation",
# # # #         "reason": "Medical leave",
# # # #         "submissionDate": "2025-05-01"
# # # #     }
# # # #     result = submit_leave_request(leave_data)
# # # #     print(result)







# # from pymongo import MongoClient
# # from email.mime.text import MIMEText
# # import smtplib

# # def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason, leave_type, leave_hours=None, leave_days=None):
# #     sender_email = "timesheetsystem2025@gmail.com"
# #     sender_password = "mhuv nxdf ciqz igws"

# #     subject = f"New Leave Request from {employee_name}"

# #     if leave_hours is not None:
# #         duration_line = f"Requested: {leave_hours} hour(s)"
# #     elif leave_days is not None:
# #         duration_line = f"Requested: {leave_days} day(s)"
# #     else:
# #         duration_line = "Requested: Unknown duration"

# #     body = f"""
# #     Good day,

# #     A new leave request has been submitted:

# #     Employee: {employee_name}
# #     From: {start_date}
# #     To: {end_date}
# #     Reason: {reason}
# #     Leave Type: {leave_type}
# #     {duration_line}

# #     Please log in to the system to review and take action.

# #     Regards,
# #     Timesheet System
# #     """

# #     msg = MIMEText(body)
# #     msg["Subject"] = subject
# #     msg["From"] = sender_email
# #     msg["To"] = manager_email

# #     try:
# #         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
# #             server.login(sender_email, sender_password)
# #             server.sendmail(sender_email, manager_email, msg.as_string())
# #         print("Email sent successfully to manager.")
# #     except Exception as e:
# #         print(f"Failed to send email: {e}")

# # def submit_leave_request(leave_data):
# #     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# #     db = client["Timesheet"]
# #     emp_collection = db["Employee_leavedetails"]
# #     emp_data_collection = db["employee_data"]
# #     leave_collection = db["Leave_Requests"]

# #     required_fields = ["name", "leaveType", "startDate", "endDate", "reason", "submissionDate"]
# #     missing = [field for field in required_fields if not leave_data.get(field)]
# #     if missing:
# #         return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

# #     employee = emp_collection.find_one({"name": leave_data["name"]})
# #     if not employee:
# #         return {"success": False, "message": "Employee not found"}

# #     # Determine leave hours from input
# #     if "hours" in leave_data:
# #         leave_hours = leave_data["hours"]
# #     elif "days" in leave_data:
# #         leave_hours = leave_data["days"] * 8
# #     else:
# #         return {"success": False, "message": "Either 'hours' or 'days' must be provided"}

# #     leave_type = leave_data["leaveType"].lower()

# #     total_allocated = employee.get("Total_leave_hours", 0)
# #     remaining_total = employee.get("remaining_leave_hours", total_allocated)
# #     sick_hours = employee.get("sick_leave_hours", 0)
# #     casual_hours = employee.get("casual_leave_hours", 0)

# #     if remaining_total < leave_hours:
# #         return {"success": False, "message": "Not enough remaining leave hours"}

# #     updated_remaining = remaining_total - leave_hours
# #     updated_sick = sick_hours
# #     updated_casual = casual_hours

# #     if leave_type == "sick":
# #         if sick_hours < leave_hours:
# #             return {"success": False, "message": "Not enough sick leave hours"}
# #         updated_sick -= leave_hours
# #     elif leave_type != "sick":
# #         if casual_hours < leave_hours:
# #             return {"success": False, "message": "Not enough casual leave hours"}
# #         updated_casual -= leave_hours
# #     else:
# #         return {"success": False, "message": "Invalid leave type"}

# #     # Insert leave request
# #     leave_request = {
# #         "employee_name": leave_data["name"],
# #         "leave_type": leave_type,
# #         "start_date": leave_data["startDate"],
# #         "end_date": leave_data["endDate"],
# #         "reason": leave_data["reason"],
# #         "status": "Pending",
# #         "days_requested": leave_data.get("days"),
# #         "hours_requested": leave_hours,
# #         "submitted_at": leave_data["submissionDate"],
# #         "remaining_leave_hours": {
# #             "total": updated_remaining,
# #             "sick": updated_sick,
# #             "casual": updated_casual
# #         }
# #     }

# #     result = leave_collection.insert_one(leave_request)

# #     # Update employee's remaining leave hours
# #     emp_collection.update_one(
# #         {"name": leave_data["name"]},
# #         {"$set": {
# #             "remaining_leave_hours": updated_remaining,
# #             "sick_leave_hours": updated_sick,
# #             "casual_leave_hours": updated_casual
# #         }}
# #     )

# #     # Email to manager
# #     emp_data = emp_data_collection.find_one({"name": leave_data["name"]})
# #     if emp_data and "manager_email" in emp_data:
# #         send_email_to_manager(
# #             emp_data["manager_email"],
# #             leave_data["name"],
# #             leave_data["startDate"],
# #             leave_data["endDate"],
# #             leave_data["reason"],
# #             leave_data["leaveType"],
# #             leave_hours=leave_hours,
# #             leave_days=leave_data.get("days")
# #         )
# #     else:
# #         print("Manager email not found in Employee_data collection")

# #     return {
# #         "success": True,
# #         "message": "Leave request submitted and email sent to manager.",
# #         "request_id": str(result.inserted_id),
# #         "remaining_hours": {
# #             "total": updated_remaining,
# #             "sick": updated_sick,
# #             "casual": updated_casual
# #         }
# #     }
# # if __name__ == "__main__":
# #     leave_data = {
# #         "name": "Sudharshan",  # Must match an existing record in your DB
# #         "leaveType": "vote",
# #         "startDate": "2025-07-05",
# #         "endDate": "2025-07-05",
# #         "reason": "Half-day medical appointment",
# #         "hours": 4,  # or use "days": 1 if testing in days
# #         "submissionDate": "2025-05-01"
# #     }

# #     result = submit_leave_request(leave_data)
# #     print(result)


# import smtplib
# from email.mime.text import MIMEText
# from pymongo import MongoClient
# from datetime import datetime

# def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason, leave_type, leave_hours):
#     sender_email = "timesheetsystem2025@gmail.com"
#     sender_password = "mhuv nxdf ciqz igws"  # Replace with your app password

#     subject = f"New Leave Request from {employee_name}"
#     body = f"""
#     Good day,

#     A new leave request has been submitted:

#     Employee: {employee_name}
#     From: {start_date}
#     To: {end_date}
#     Reason: {reason}
#     Leave Type: {leave_type}
#     Leave Hours: {leave_hours}

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
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB connection
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     emp_data_collection = db["employee_data"]
#     leave_collection = db["Leave_Requests"]

#     required_fields = ["name", "leaveType", "startDate", "endDate", "reason", "hours", "submissionDate"]
#     missing = [field for field in required_fields if not leave_data.get(field)]
#     if missing:
#         return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

#     employee = emp_collection.find_one({"name": leave_data["name"]})
#     if not employee:
#         return {"success": False, "message": "Employee not found"}

#     # Logic for sick leave first, then casual leave if sick leave is insufficient
#     requested_hours = leave_data["hours"]
#     if leave_data["leaveType"].lower() == "sick":
#         sick_leave_hours = employee.get("Sick_leave_hours", 0)
#         casual_leave_hours = employee.get("Casual_leave_hours", 0)

#         if sick_leave_hours >= requested_hours:
#             # Deduct from sick leave if enough hours
#             updated = emp_collection.update_one(
#                 {"name": leave_data["name"]},
#                 {"$inc": {"Sick_leave_hours": -requested_hours, "Remaining_leave_hours": -requested_hours}}
#             )
#             if updated.matched_count == 0:
#                 return {"success": False, "message": "Failed to update sick leave balance"}
#         else:
#             remaining_hours = requested_hours - sick_leave_hours
#             if casual_leave_hours >= remaining_hours:
#                 # Deduct remaining from casual leave
#                 updated = emp_collection.update_one(
#                     {"name": leave_data["name"]},
#                     {"$inc": {"Sick_leave_hours": -sick_leave_hours, "Casual_leave_hours": -remaining_hours, "Remaining_leave_hours": -requested_hours}}
#                 )
#                 if updated.matched_count == 0:
#                     return {"success": False, "message": "Failed to update sick and casual leave balances"}
#             else:
#                 return {"success": False, "message": "Not enough leave hours (sick or casual)"}

#     # Proceed with leave request submission if all validations pass
#     leave_request = {
#         "employee_name": leave_data["name"],
#         "leave_type": leave_data["leaveType"].lower(),
#         "start_date": leave_data["startDate"],
#         "end_date": leave_data["endDate"],
#         "reason": leave_data["reason"],
#         "status": "Pending",
#         "hours_requested": leave_data["hours"],
#         "submitted_at": leave_data["submissionDate"]
#     }

#     result = leave_collection.insert_one(leave_request)

#     # Get manager's email using employee's name
#     emp_data = emp_data_collection.find_one({"name": leave_data["name"]})
#     if emp_data and "manager_email" in emp_data:
#         manager_email = emp_data["manager_email"]
#         send_email_to_manager(manager_email, leave_data["name"], leave_data["startDate"], leave_data["endDate"], leave_data["reason"], leave_data["leaveType"], leave_data["hours"])
#     else:
#         print("Manager email not found in Employee_data collection")

#     return {
#         "success": True,
#         "message": "Leave request submitted and email sent to manager.",
#         "request_id": str(result.inserted_id)
#     }

# # For testing purposes
# if __name__ == "__main__":
#     leave_data = {
#         "name": "Sudharshan",
#         "hours": 4,  # Requesting 4 hours of sick leave
#         "startDate": "2025-07-17",
#         "endDate": "2025-07-17",
#         "leaveType": "Sick",  # Leave type is sick
#         "reason": "Medical leave",
#         "submissionDate": "2025-05-01"
#     }
#     result = submit_leave_request(leave_data)
#     print(result)

# import smtplib
# from email.mime.text import MIMEText
# from pymongo import MongoClient
# from datetime import datetime

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

# def submit_leave_request(leave_data):
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB connection
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     emp_data_collection = db["employee_data"]
#     leave_collection = db["Leave_Requests"]

#     required_fields = ["name", "leaveType", "startDate", "endDate", "reason", "hours", "submissionDate"]
#     missing = [field for field in required_fields if not leave_data.get(field)]
#     if missing:
#         return {"success": False, "message": f"Missing fields: {', '.join(missing)}"}

#     employee = emp_collection.find_one({"name": leave_data["name"]})
#     if not employee:
#         return {"success": False, "message": "Employee not found"}

#     requested_hours = leave_data["hours"]

#     # Check if the leave type is valid and if there's enough leave balance
#     if leave_data["leaveType"].lower() == "sick":
#         sick_leave_hours = employee.get("Sick_leave_hours", 0)
#         casual_leave_hours = employee.get("Casual_leave_hours", 0)

#         if sick_leave_hours + casual_leave_hours < requested_hours:
#             return {"success": False, "message": "Not enough leave hours (sick or casual)"}

#     # Insert leave request to DB (pending for approval)
#     leave_request = {
#         "employee_name": leave_data["name"],
#         "leave_type": leave_data["leaveType"].lower(),
#         "start_date": leave_data["startDate"],
#         "end_date": leave_data["endDate"],
#         "reason": leave_data["reason"],
#         "status": "Pending",  # Admin needs to approve this
#         "hours_requested": leave_data["hours"],
#         "submitted_at": leave_data["submissionDate"]
#     }

#     result = leave_collection.insert_one(leave_request)

#     # Send email to manager for approval
#     emp_data = emp_data_collection.find_one({"name": leave_data["name"]})
#     if emp_data and "manager_email" in emp_data:
#         manager_email = emp_data["manager_email"]
#         print(manager_email)
#         send_email_to_manager(manager_email, leave_data["name"], leave_data["startDate"], leave_data["endDate"], leave_data["reason"], leave_data["leaveType"], leave_data["hours"])
#         return {
#             "success": True,
#             "message": "Leave request submitted and email sent to manager.",
#             "request_id": str(result.inserted_id)
#         }
#     else:
#         print("Manager email not found in Employee_data collection")
#         return {
#             "success": False,
#             "message": "Manager email not found. Leave request not submitted.",
#             "request_id": None
#         }


# if __name__ == "__main__":
#     # Sample leave data for testing
#     leave_data = {
#         "name": "Sudharshan",  # Employee name
#         "leaveType": "Sick",  # Leave type (e.g., Sick, Casual)
#         "startDate": "2025-06-15",  # Start date of leave
#         "endDate": "2025-06-15",  # End date of leave
#         "reason": "Medical",  # Reason for the leave
#         "hours": 4,  # Hours requested for leave
#         "submissionDate": str(datetime.now().date())  # Current date as submission date
#     }
    
#     # Call the function to submit the leave request
#     result = submit_leave_request(leave_data)
    
#     # Print the result of the leave request submission
#     print(result)





import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime


def send_email_to_manager(manager_email, employee_name, start_date, end_date, reason, leave_type, hours):
    sender_email = "timesheetsystem2025@gmail.com"
    sender_password = "mhuv nxdf ciqz igws"  # Use your actual password or app password here

    subject = f"New Leave Request from {employee_name}"
    body = f"""
    Good day,

    A new leave request has been submitted:

    Employee: {employee_name}
    From: {start_date}
    To: {end_date}
    Reason: {reason}
    Leave Type: {leave_type}
    Hours Requested: {hours} hours

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
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    emp_data_collection = db["employee_data"]
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
#         "name": "Naveen", 
#         "leaveType": "Vote", 
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
