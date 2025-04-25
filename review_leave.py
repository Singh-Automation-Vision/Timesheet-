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
from pymongo import MongoClient

def review_leave_request(employee_name, decision):
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    leave_collection = db["Leave_Requests"]

    # Find the latest pending leave request for this employee
    leave_request = leave_collection.find_one({"employee_name": employee_name, "status": "Pending"})
    if not leave_request:
        return {"success": False, "message": "No pending leave request found for this employee."}

    days = leave_request["days_requested"]

    if decision.lower() == "approve":
        # Deduct from Total_leave and increment Leave_taken
        emp_collection.update_one(
            {"name": employee_name},
            {
                "$inc": {
                    "Total_leave": -days,
                    "Leave_taken": days
                }
            }
        )
        new_status = "Approved"

    elif decision.lower() == "reject":
        new_status = "Rejected"

    else:
        return {"success": False, "message": "Invalid decision. Use 'approve' or 'reject'"}

    # Update leave request status
    leave_collection.update_one(
        {"employee_name": employee_name, "status": "Pending"},
        {"$set": {"status": new_status}}
    )

    return {"success": True, "message": f"Leave request for {employee_name} {new_status.lower()} successfully."}

# Example usage
if __name__ == "__main__":
    employee_name = "Naveen"  # Replace with actual name
    decision = "reject"  # or "reject"
    result = review_leave_request(employee_name, decision)
    print(result)

