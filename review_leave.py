from pymongo import MongoClient
from email.message import EmailMessage
import smtplib

def send_leave_email(recipient_email, employee_name, status, hours, start_date):
    msg = EmailMessage()
    msg['Subject'] = f"Your Leave Request has been {status}"
    msg['From'] = "timesheetsystem2025@gmail.com"  
    msg['To'] = recipient_email

    msg.set_content(
        f"Hi {employee_name},\n\n"
        f"Your leave request starting from {start_date} for {hours} hour(s) has been {status.lower()}.\n\n"
        f"Regards,\nAdmin"
    )

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "timesheetsystem2025@gmail.com"
    sender_password = "mhuv nxdf ciqz igws"  # Gmail App Password

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


# def review_leave_request(employee_name, status):
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     leave_collection = db["Leave_Requests"]
#     emp_data_collection= db["employee_data"]
#     # client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     # db = client["Timesheet"]
#     # emp_collection = db["Employee_leavedetails"]
#     # emp_data_collection = db["Employee_data"]
#     # leave_collection = db["Leave_Requests"]
    

#     # Find the latest pending leave request
#     leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
#     if not leave_request:
#         return {"success": False, "message": "No pending leave request found for this employee."}

#     days = leave_request["days_requested"]
#     start_date = leave_request["start_date"]

#     # Get employee email
#     emp_record = emp_data_collection.find_one({"name": employee_name})
#     if not emp_record or "email" not in emp_record:
#         return {"success": False, "message": "Employee email not found."}

#     recipient_email = emp_record["email"]

#     # Based on status directly
#     if status == "Approved":
#         # Update leave balances
#         emp_collection.update_one(
#             {"name": employee_name},
#             {
#                 "$inc": {
#                     "Remmaining_leave": -days,
#                     "Leave_taken": days
#                 }
#             }
#         )
#         destination_collection = db["Approved_request"]

#     elif status == "Rejected":
#         destination_collection = db["Rejected_request"]

#     else:
#         return {"success": False, "message": "Invalid status. Must be 'Approved' or 'Rejected'."}

#     # Prepare leave request for moving
#     leave_request.pop("_id", None)
#     leave_request["status"] = status

#     # Move leave request
#     leave_collection.delete_one({"employee_name": employee_name, "status": "Pending"})
#     destination_collection.insert_one(leave_request)

#     # Send email
#     send_leave_email(recipient_email, employee_name, status, days, start_date)

#     return {"success": True, "message": f"Leave request for {employee_name} {status.lower()} and email sent."}

def review_leave_request(employee_name, status):
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    leave_collection = db["Leave_Requests"]
    emp_data_collection = db["employee_data"]

    # Find the latest pending leave request
    leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
    if not leave_request:
        return {"success": False, "message": "No pending leave request found for this employee."}

    hours_requested = leave_request.get("hours_requested", 0)
    start_date = leave_request["start_date"]
    leave_type = leave_request.get("leave_type", "").lower()

    # Get employee email
    emp_record = emp_data_collection.find_one({"name": employee_name})
    if not emp_record or "email" not in emp_record:
        return {"success": False, "message": "Employee email not found."}

    recipient_email = emp_record["email"]

    # Based on approval or rejection
    if status == "Approved":
        update_query = {"$inc": {"Remaining_leave_hours": -hours_requested}}
        
        if leave_type == "Medical Leave":
            update_query["$inc"]["Sick_leave_hours_used"] = hours_requested
        else:
            update_query["$inc"]["Casual_leave_hours_used"] = hours_requested

        emp_collection.update_one({"name": employee_name}, update_query)
        destination_collection = db["Approved_request"]

    elif status == "Rejected":
        destination_collection = db["Rejected_request"]

    else:
        return {"success": False, "message": "Invalid status. Must be 'Approved' or 'Rejected'."}

    # Prepare the request to move
    leave_request.pop("_id", None)
    leave_request["status"] = status

    leave_collection.delete_one({"employee_name": employee_name, "status": "Pending"})
    destination_collection.insert_one(leave_request)

    # Send notification email
    send_leave_email(recipient_email, employee_name, status, hours_requested, start_date)

    return {"success": True, "message": f"Leave request for {employee_name} {status.lower()} and email sent."}


# if __name__ == "__main__":
#     # Example test input
#     employee_name = "Sudharshan"
#     status = "Approved"  # or "Rejected"

#     result = review_leave_request(employee_name, status)
#     print(result)

def get_leave_requests():
    # client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    # db = client["Timesheet"]
    # emp_collection = db["Employee_leavedetails"]
    # emp_data_collection = db["Employee_data"]
    # leave_collection = db["Leave_Requests"]
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    leave_collection = db["Leave_Requests"]
    emp_data_collection = db["employee_data"]

    leave_requests = list(leave_collection.find())

    # Now fetch manager names from employee_data collection
    for leave in leave_requests:
        employee_name = leave.get('employee_name')
        if employee_name:
            emp_data = emp_data_collection.find_one({'name': employee_name})
            if emp_data and 'manager' in emp_data:
                leave['manager'] = emp_data['manager']
            else:
                leave['manager'] = None  # Manager not found

        # Remove _id if needed
        leave.pop('_id', None)

    return leave_requests




def get_leave_request_by_name(employee_name):
    # client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    # db = client["Timesheet"]
    # emp_collection = db["Employee_leavedetails"]
    # emp_data_collection = db["Employee_data"]
    # leave_collection = db["Leave_Requests"]
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    leave_collection = db["Leave_Requests"]
    emp_data_collection = db["employee_data"]


    leave = leave_collection.find_one({'employee_name': employee_name})

    if leave:
        leave.pop('_id', None)  # 🔥 Remove _id from the response
        return leave
    else:
        return {"error": "Leave request not found"}, 404
# # get_leave_request_by_name("Sudharshan")