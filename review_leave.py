from pymongo import MongoClient
from bson import ObjectId

def review_leave_request(request_id, decision):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]
    leave_collection = db["Leave_Requests"]

    leave_request = leave_collection.find_one({"_id": ObjectId(request_id)})
    if not leave_request:
        return {"success": False, "message": "Leave request not found"}

    if leave_request["status"] != "Pending":
        return {"success": False, "message": "Leave request already reviewed"}

    employee_name = leave_request["employee_name"]
    days = leave_request["days_requested"]

    if decision.lower() == "approve":
        emp_collection.update_one(
            {"name": employee_name},
            {"$inc": {"Total_leave": -days,
                      "Leave_taken":days}}
        )
        new_status = "Approved"
    elif decision.lower() == "reject":
        new_status = "Rejected"
    else:
        return {"success": False, "message": "Invalid decision. Use 'approve' or 'reject'"}

    leave_collection.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": new_status}}
    )

    return {"success": True, "message": f"Leave request {new_status.lower()} successfully."}



if __name__ == "__main__":
    # Example call to approve or reject
    request_id = "6808e66414485111f121ab60"  # Replace with actual ID
    decision = "approve"  # or "reject"
    result = review_leave_request(request_id, decision)
    print(result)

