# from pymongo import MongoClient
# from email.message import EmailMessage
# import smtplib

# def send_leave_email(recipient_email, employee_name, status, hours, start_date):
#     msg = EmailMessage()
#     msg['Subject'] = f"Your Leave Request has been {status}"
#     msg['From'] = "timesheetsystem2025@gmail.com"  
#     msg['To'] = recipient_email

#     msg.set_content(
#         f"Hi {employee_name},\n\n"
#         f"Your leave request starting from {start_date} for {hours} hour(s) has been {status.lower()}.\n\n"
#         f"Regards,\nAdmin"
#     )

#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     sender_email = "timesheetsystem2025@gmail.com"
#     sender_password = "mhuv nxdf ciqz igws"  # Gmail App Password

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(msg)



# def send_email_to_manager_zero_leave(manager_email, employee_name):
#     msg = EmailMessage()
#     msg['Subject'] = f"Leave Balance Exhausted for {employee_name}"
#     msg['From'] = "timesheetsystem2025@gmail.com"
#     msg['To'] = manager_email

#     msg.set_content(
#         f"Dear Manager,\n\n"
#         f"This is to inform you that {employee_name} has exhausted their total remaining leave hours.\n"
#         f"Please take note in case further action or approval is needed.\n\n"
#         f"Regards,\nLeave Management System"
#     )

#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     sender_email = "timesheetsystem2025@gmail.com"
#     sender_password = "mhuv nxdf ciqz igws"  # Gmail App Password

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(msg)
#         print(f"Zero leave notification sent to manager: {manager_email}")
#     except Exception as e:
#         print(f"Failed to send zero leave email to manager: {e}")


# def review_leave_request(employee_name, status):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     # client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     leave_collection = db["Leave_Requests"]
#     emp_data_collection = db["employee_data"]

#     # Find the latest pending leave request
#     leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
#     if not leave_request:
#         return {"success": False, "message": "No pending leave request found for this employee."}

#     hours_requested = leave_request.get("hours_requested", 0)
#     start_date = leave_request["start_date"]
#     leave_type = leave_request.get("leave_type", "").lower()

#     # Get employee email
#     emp_record = emp_data_collection.find_one({"name": employee_name})
#     if not emp_record or "email" not in emp_record:
#         return {"success": False, "message": "Employee email not found."}

#     recipient_email = emp_record["email"]
#     manager_email = emp_record.get("manager_email")

#     # Based on approval or rejection
#     if status == "Approved":
#         update_query = {
#             "$inc": {
#                 "Remaining_leave_hours": -hours_requested
#             }
#         }

#         if leave_type == "medical leave":
#             update_query["$inc"]["Sick_leave_hours_used"] = hours_requested
#             update_query["$inc"]["Sick_leave_hours"] = -hours_requested
#         else:
#             update_query["$inc"]["Casual_leave_hours_used"] = hours_requested
#             update_query["$inc"]["Casual_leave_hours"] = -hours_requested

#         emp_collection.update_one({"name": employee_name}, update_query)

#     # if status == "Approved":
#     #     update_query = {"$inc": {"Remaining_leave_hours": -hours_requested}}
        
#     #     if leave_type == "medical leave":
#     #         update_query["$inc"]["Sick_leave_hours_used":+ hours_requested]
#     #         update_query = {"$inc": {"Sick_leave_hours": -hours_requested}}
#     #     else:
#     #         update_query["$inc"]["Casual_leave_hours_used": + hours_requested]
#     #         update_query = {"$inc": {"Casual_leave_hours": -hours_requested}}

#     #     emp_collection.update_one({"name": employee_name}, update_query)
#         destination_collection = db["Approved_request"]
#         updated_emp = emp_collection.find_one({"name": employee_name})
#         if updated_emp and updated_emp.get("Remaining_leave_hours", 0) <= 0:
#             if manager_email:
#                 send_email_to_manager_zero_leave(manager_email, employee_name)
#             else:
#                 print("Manager email not available for zero leave alert")

#     elif status == "Rejected":
#         destination_collection = db["Rejected_request"]

#     else:
#         return {"success": False, "message": "Invalid status. Must be 'Approved' or 'Rejected'."}

#     # Prepare the request to move
#     leave_request.pop("_id", None)
#     leave_request["status"] = status

#     leave_collection.delete_one({"employee_name": employee_name, "status": "Pending"})
#     destination_collection.insert_one(leave_request)

#     # Send notification email
#     send_leave_email(recipient_email, employee_name, status, hours_requested, start_date)

#     return {"success": True, "message": f"Leave request for {employee_name} {status.lower()} and email sent."}


# # if __name__ == "__main__":
# #     # Example test input
# #     employee_name = "Sudharshan"
# #     status = "Approved"  # or "Rejected"

# #     result = review_leave_request(employee_name, status)
# #     print(result)

# def get_leave_requests():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     emp_data_collection = db["Employee_data"]
#     leave_collection = db["Leave_Requests"]
#     # client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     # db = client["Timesheet"]
#     # emp_collection = db["Employee_leavedetails"]
#     # leave_collection = db["Leave_Requests"]
#     # emp_data_collection = db["employee_data"]

#     leave_requests = list(leave_collection.find())

#     # Now fetch manager names from employee_data collection
#     for leave in leave_requests:
#         employee_name = leave.get('employee_name')
#         if employee_name:
#             emp_data = emp_data_collection.find_one({'name': employee_name})
#             if emp_data and 'manager' in emp_data:
#                 leave['manager'] = emp_data['manager']
#             else:
#                 leave['manager'] = None  # Manager not found

#         # Remove _id if needed
#         leave.pop('_id', None)

#     return leave_requests




# def get_leave_request_by_name(employee_name):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]
#     emp_data_collection = db["Employee_data"]
#     leave_collection = db["Leave_Requests"]
#     # client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     # db = client["Timesheet"]
#     # emp_collection = db["Employee_leavedetails"]
#     # leave_collection = db["Leave_Requests"]
#     # emp_data_collection = db["employee_data"]


#     leave = leave_collection.find_one({'employee_name': employee_name})

#     if leave:
#         leave.pop('_id', None)  # 🔥 Remove _id from the response
#         return leave
#     else:
#         return {"error": "Leave request not found"}, 404
# # # get_leave_request_by_name("Sudharshan")



import logging
from pymongo import MongoClient
from email.message import EmailMessage
import smtplib 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Function used to send mail to the user regarding the status of the request 
def send_leave_email(recipient_email, employee_name, status, hours, start_date):
    try:
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
        logging.info(f"Leave status email sent to {recipient_email}")
    except Exception as e:
        logging.error(f"Failed to send leave email: {e}")



#Function used to send mail to the manager regarding the employee leaves became zero , it used for the send notification to manager
def send_email_to_manager_zero_leave(manager_email, employee_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Leave Balance Exhausted for {employee_name}"
        msg['From'] = "timesheetsystem2025@gmail.com"
        msg['To'] = manager_email

        msg.set_content(
            f"Dear Manager,\n\n"
            f"This is to inform you that {employee_name} has exhausted their total remaining leave hours.\n"
            f"Please take note in case further action or approval is needed.\n\n"
            f"Regards,\nLeave Management System"
        )

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "timesheetsystem2025@gmail.com"
        sender_password = "mhuv nxdf ciqz igws"

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logging.info(f"Zero leave notification sent to manager: {manager_email}")
    except Exception as e:
        logging.error(f"Failed to send zero leave email to manager: {e}")

#Function to approve or reject the leave request 
def review_leave_request(employee_name, status):
    try:
        client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
        db = client["Timesheet"]
        emp_collection = db["Employee_leavedetails"]
        leave_collection = db["Leave_Requests"]
        emp_data_collection = db["Employee_data"]

        leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
        if not leave_request:
            logging.warning(f"No pending leave request for {employee_name}")
            return {"success": False, "message": "No pending leave request found for this employee."}

        hours_requested = leave_request.get("hours_requested", 0)
        start_date = leave_request["start_date"]
        leave_type = leave_request.get("leave_type", "").lower()

        emp_record = emp_data_collection.find_one({"name": employee_name})
        if not emp_record or "email" not in emp_record:
            logging.error(f"Email not found for employee: {employee_name}")
            return {"success": False, "message": "Employee email not found."}

        recipient_email = emp_record["email"]
        manager_email = emp_record.get("manager_email")

        if status == "Approved":
            update_query = {
                "$inc": {
                    "Remaining_leave_hours": -hours_requested
                }
            }
            if leave_type == "medical leave":
                update_query["$inc"]["Sick_leave_hours_used"] = hours_requested
                update_query["$inc"]["Sick_leave_hours"] = -hours_requested
            else:
                update_query["$inc"]["Casual_leave_hours_used"] = hours_requested
                update_query["$inc"]["Casual_leave_hours"] = -hours_requested

            emp_collection.update_one({"name": employee_name}, update_query)
            destination_collection = db["Approved_request"]
            logging.info(f"Leave approved for {employee_name}")

            updated_emp = emp_collection.find_one({"name": employee_name})
            if updated_emp and updated_emp.get("Remaining_leave_hours", 0) <= 0:
                if manager_email:
                    send_email_to_manager_zero_leave(manager_email, employee_name)
                else:
                    logging.warning(f"Manager email not available for {employee_name}")

        elif status == "Rejected":
            destination_collection = db["Rejected_request"]
            logging.info(f"Leave rejected for {employee_name}")

        else:
            logging.error("Invalid status provided")
            return {"success": False, "message": "Invalid status. Must be 'Approved' or 'Rejected'."}

        leave_request.pop("_id", None)
        leave_request["status"] = status

        leave_collection.delete_one({"employee_name": employee_name, "status": "Pending"})
        destination_collection.insert_one(leave_request)

        send_leave_email(recipient_email, employee_name, status, hours_requested, start_date)

        return {"success": True, "message": f"Leave request for {employee_name} {status.lower()} and email sent."}

    except Exception as e:
        logging.error(f"Error in review_leave_request: {e}")
        return {"success": False, "message": "Internal server error."}
    

#This Function is used to fetch the leave request of all the employees who have applied for the leave     
def get_leave_requests():
    try:
        client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
        db = client["Timesheet"]
        leave_collection = db["Leave_Requests"]
        emp_data_collection = db["Employee_data"]

        leave_requests = list(leave_collection.find())
        for leave in leave_requests:
            employee_name = leave.get('employee_name')
            emp_data = emp_data_collection.find_one({'name': employee_name})
            leave['manager'] = emp_data.get('manager') if emp_data else None
            leave.pop('_id', None)

        logging.info("Fetched all leave requests")
        return leave_requests

    except Exception as e:
        logging.error(f"Error in get_leave_requests: {e}")
        return []

#This Function is used to get the leave request of the particular employee
def get_leave_request_by_name(employee_name):
    try:
        client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
        db = client["Timesheet"]
        leave_collection = db["Leave_Requests"]

        leave = leave_collection.find_one({'employee_name': employee_name})
        if leave:
            leave.pop('_id', None)
            logging.info(f"Leave request fetched for {employee_name}")
            return leave
        else:
            logging.warning(f"No leave request found for {employee_name}")
            return {"error": "Leave request not found"}, 404
    except Exception as e:
        logging.error(f"Error in get_leave_request_by_name: {e}")
        return {"error": "Server error"}, 500