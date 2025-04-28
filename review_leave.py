# from pymongo import MongoClient
# from bson import ObjectId

# def review_leave_request(request_id, decision):
#     # client = MongoClient("mongodb://localhost:27017/")
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     leave_collection = db["Leave_Requests"]

#     leave_request = leave_collection.find_one({"employee_name": name, "status": "Pending"})
#     if not leave_request:
#         return {"success": False, "message": "Leave request not found"}

#     if leave_request["status"] != "Pending":
#         return {"success": False, "message": "Leave request already reviewed"}

#     employee_name = leave_request["employee_name"]
#     days = leave_request["days_requested"]

#     if decision.lower() == "approve":
#         emp_collection.update_one(
#             {"name": employee_name},
#             {"$inc": {"Total_leave": -days,
#                       "Leave_taken":days}}
#         )
#         new_status = "Approved"
#     elif decision.lower() == "reject":
#         new_status = "Rejected"
#     else:
#         return {"success": False, "message": "Invalid decision. Use 'approve' or 'reject'"}

#     leave_collection.update_one(
#         {"_id": ObjectId(request_id)},
#         {"$set": {"status": new_status}}
#     )

#     return {"success": True, "message": f"Leave request {new_status.lower()} successfully."}



# if __name__ == "__main__":
#     # Example call to approve or reject
#     request_id = "6808e66414485111f121ab60"  # Replace with actual ID
#     decision = "approve"  # or "reject"
#     result = review_leave_request(request_id, decision)
#     print(result)





# from pymongo import MongoClient

# def review_leave_request(employee_name, decision):
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     leave_collection = db["Leave_Requests"]

#     # Find the latest pending leave request for this employee
#     leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
#     if not leave_request:
#         return {"success": False, "message": "No pending leave request found for this employee."}

#     days = leave_request["days_requested"]

#     if decision.lower() == "approve":
#         # Deduct from Total_leave and increment Leave_taken
#         emp_collection.update_one(
#             {"name": employee_name},
#             {
#                 "$inc": {
#                     "Total_leave": -days,
#                     "Leave_taken": days
#                 }
#             }
#         )
#         new_status = "Approved"

#     elif decision.lower() == "reject":
#         new_status = "Rejected"

#     else:
#         return {"success": False, "message": "Invalid decision. Use 'approve' or 'reject'"}

#     # Update leave request status
#     leave_collection.update_one(
#         {"employee_name": employee_name, "status": "Pending"},
#         {"$set": {"status": new_status}}
#     )

#     return {"success": True, "message": f"Leave request for {employee_name} {new_status.lower()} successfully."}

# # Example usage
# if __name__ == "__main__":
#     employee_name = "Naveen"  # Replace with actual name
#     decision = "reject"  # or "reject"
#     result = review_leave_request(employee_name, decision)
#     print(result)





from pymongo import MongoClient
from email.message import EmailMessage
import smtplib

def send_leave_email(recipient_email, employee_name, status, days, start_date):
    msg = EmailMessage()
    msg['Subject'] = f"Your Leave Request has been {status}"
    msg['From'] = "timesheetsystem2025@gmail.com"  # your email
    msg['To'] = recipient_email

    msg.set_content(
        f"Hi {employee_name},\n\n"
        f"Your leave request starting from {start_date} for {days} day(s) has been {status.lower()}.\n\n"
        f"Regards,\nAdmin"
    )

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "timesheetsystem2025@gmail.com"
    sender_password = "mhuv nxdf ciqz igws"  # your Gmail App Password

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


# def review_leave_request(employee_name, decision):
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     leave_collection = db["Leave_Requests"]
#     employee_data = db["employee_data"]

#     # Find the latest pending leave request for this employee
#     leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
#     if not leave_request:
#         return {"success": False, "message": "No pending leave request found for this employee."}

#     days = leave_request["days_requested"]
#     start_date = leave_request["start_date"]

#     # Get employee's email from Employee_data
#     emp_record = employee_data.find_one({"name": employee_name})
#     if not emp_record or "email" not in emp_record:
#         return {"success": False, "message": "Employee email not found."}

#     recipient_email = emp_record["email"]

#     if decision.lower() == "approve":
#         # Update leave balances
#         emp_collection.update_one(
#             {"name": employee_name},
#             {
#                 "$inc": {
#                     "Total_leave": -days,
#                     "Leave_taken": days
#                 }
#             }
#         )
#         new_status = "Approved"
#         destination_collection = db["Approved_request"]

#     elif decision.lower() == "reject":
#         new_status = "Rejected"
#         destination_collection = db["Rejected_request"]
#     else:
#         return {"success": False, "message": "Invalid decision. Use 'approve' or 'reject'"}

#     # Update status of original request
#     leave_collection.update_one(
#         {"employee_name": employee_name, "status": "Pending"},
#         {"$set": {"status": new_status}}
#     )

#     # Move to Approved/Rejected collection without _id
#     leave_request.pop("_id", None)
#     leave_request["status"] = new_status
#     destination_collection.insert_one(leave_request)

#     # Send email
#     send_leave_email(recipient_email, employee_name, new_status, days, start_date)

#     return {"success": True, "message": f"Leave request for {employee_name} {new_status.lower()} and email sent."}

def review_leave_request(employee_name, decision):
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    leave_collection = db["Leave_Requests"]
    employee_data = db["employee_data"]

    # Find the latest pending leave request
    leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
    if not leave_request:
        return {"success": False, "message": "No pending leave request found for this employee."}

    days = leave_request["days_requested"]
    start_date = leave_request["start_date"]

    # Get email from employee_data
    emp_record = employee_data.find_one({"name": employee_name})
    if not emp_record or "email" not in emp_record:
        return {"success": False, "message": "Employee email not found."}

    recipient_email = emp_record["email"]

    # Decision logic
    if decision.lower() == "approve":
        # Update leave balances
        emp_collection.update_one(
            {"name": employee_name},
            {
                "$inc": {
                    "Remmaining_leave": -days,
                    "Leave_taken": days
                }
            }
        )
        new_status = "Approved"
        destination_collection = db["Approved_request"]

    elif decision.lower() == "reject":
        new_status = "Rejected"
        destination_collection = db["Rejected_request"]

    else:
        return {"success": False, "message": "Invalid decision. Use 'approve' or 'reject'"}

    # Remove _id to avoid DuplicateKeyError
    leave_request.pop("_id", None)
    leave_request["status"] = new_status

    # Delete from Leave_Requests and move to destination
    leave_collection.delete_one({"employee_name": employee_name, "status": "Pending"})
    destination_collection.insert_one(leave_request)

    # Send email to employee
    send_leave_email(recipient_email, employee_name, new_status, days, start_date)

    return {"success": True, "message": f"Leave request for {employee_name} {new_status.lower()} and email sent."}

# Example usage
# if __name__ == "__main__":
#     employee_name = "Sudharshan" 
#     decision = "approve"      # or "reject"
#     result = review_leave_request(employee_name, decision)
#     print(result)

# from pymongo import MongoClient
# def get_leave_requests():
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     emp_data_collection = db["employee_data"]
#     leave_collection = db["Leave_Requests"]
    
#     leave_requests = list(leave_collection.find())
#     print(leave_requests)
# get_leave_requests()

def get_leave_requests():
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    emp_data_collection = db["employee_data"]
    leave_collection = db["Leave_Requests"]
    
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




# def get_leave_request_by_name(employee_name):
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     leave_collection = db["Leave_Requests"]

#     leave = leave_collection.find_one({'employee_name': employee_name})

#     if leave:
#         leave.pop('_id', None)  # 🔥 Remove _id from the response
#         print(leave)
#     else:
#         print({"error": "Leave request not found"}), 404
# get_leave_request_by_name("Sudharshan")