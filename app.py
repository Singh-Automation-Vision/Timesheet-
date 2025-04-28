from flask import Flask, request, jsonify
from pymongo import MongoClient
from Emp_timesheet import add_PM_data, add_AM_data, employee_login,performance_matrices, get_latest_employee_am_data
#from Emp_info import add_emp_info
from flask_cors import CORS
import logging
from admin import add_new_user,delete_emp,show_user, get_timesheet_between_dates, get_am_timesheet_between_dates,get_pm_timesheet_between_dates,get_performance_between_dates, user_details,update_user,resource_management
from Project import retrieve_project,add_project, get_project_list, get_project_hours_pm, get_project_detail, delete_project, update_project,project_details_between_dates
from leave import *
#from pyngrok import ngrok
from datetime import datetime
import os

# Initialize Flask app
application = Flask(__name__)

# Logging setup
CORS(application) 
#CORS(application, resources={r"/": {"origins": ""}}) # Enable CORS for frontend-backend communication
#
## Start ngrok tunnel
#port = 8000  # Set the same port as Flask
#public_url = ngrok.connect(port).public_url
#print(f"Ngrok Tunnel URL: {public_url}")

# Root route to verify backend is working
@application.route("/")
def home():
    return jsonify({"message": "Backend is running successfully!"})

# Route to fetch all available API routes
@application.route("/api/routes", methods=["GET"])
def get_routes():
    return jsonify([str(rule) for rule in application.url_map.iter_rules()])

logging.basicConfig(level=logging.DEBUG)

#@application.errorhandler(Exception)  # Capture all unhandled errors
#def handle_exception(e):
#    application.logger.error(f"Error: {e}", exc_info=True)
#    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

# Login route for employee/admin authentication
@application.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("email")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user_data = employee_login(username, password)  # Check credentials

    if user_data:
        if username =="admin":
            return jsonify({"user": user_data, "message": "Admin login successful"}), 200
        else:
            return jsonify({"user": user_data, "message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# Route to submit AM timesheet
@application.route("/api/AM", methods=["POST"])
def add_AM_timesheet():
    data = request.json
    add_AM_data(data)
    return jsonify({"message": "Timesheet added successfully"})

# Route to submit PM timesheet
@application.route("/api/PM", methods=["POST"])
def add_PM_timesheet():
    data = request.json
    #print(data)
    add_PM_data(data)
    return jsonify({"message": "Timesheet added successfully"})

# Add a new user (admin functionality)
@application.route("/api/users", methods=["POST"])
def new_users():
    data = request.json
    add_new_user(data)
    return jsonify({"message": "Timesheet added successfully"})

# Delete user by email (admin functionality)
@application.route("/api/users/email/<string:email>", methods=["DELETE"])
def delete_user(email):
    
    delete_emp(email)
    return jsonify({"message": "Employee deleted successfully"})

# Update performance matrices
@application.route("/api/matrices", methods=["POST"])
def matrices():
    data = request.json
    email = data.get("email")
    date = data.get("date")
    ratings = data.get("ratings")
    performance_matrices(email, date, ratings)
    return jsonify({"message": "Performance matrices updated successfully"})

# Add new employee
#@application.route("/api/add_employee", methods=["POST"])  # Fixed: Added missing route
#def add_employee():
#    emp_name = request.json
#    add_emp_info(emp_name)
#    return jsonify({"message": "Employee added successfully"})

# @application.route("/api/timesheet/admin/<string:username>/<string:date>", methods=["GET"])
# def get_timesheet(username, date):
#     data = get_emp_data(username,date)
#     return jsonify({"message": "Employee data fetched successfully", "data": data})

# Fetch timesheet for employee between two dates (admin)
@application.route("/api/timesheet/admin/<string:username>/<string:startDate>/<string:endDate>", methods=["GET"])
def get_timesheet(username, startDate,endDate):
    data = get_timesheet_between_dates(username,startDate,endDate)
    return jsonify({"message": "Employee data fetched successfully", "data": data})

# @application.route("/api/timesheet/user/<string:username>/<string:date>", methods=["GET"])
# def get_user_timesheet(username, date):
#     """
#     Fetch timesheet data for a specific user and date.
#     """
#     try:
#         # Convert the date string to the expected format
#         timesheet_entry = get_latest_employee_am_data(username)
#         if timesheet_entry:
#             return jsonify({"success": True, "data": timesheet_entry}), 200
#         else:
#             return jsonify({"success": False, "message": "No timesheet found"}), 404

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# Fetch user's AM timesheet by date
@application.route("/api/timesheet/user/<string:username>/<string:date>", methods=["GET"])
def get_user_timesheet(username, date):
    """
    Fetch timesheet data for a specific user and date.
    """
    try:
        # Convert the date string to the expected format
        timesheet_entry = get_latest_employee_am_data(username,date)
        if timesheet_entry:
            return jsonify({"success": True, "data": timesheet_entry}), 200
        else:
            return jsonify({"success": False, "message": "No timesheet found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# Show list of all users
@application.route("/api/timesheet/showUser", methods=["GET"])
def all_user_details():
    data = show_user()
    return jsonify({"message": "Employee list fetched successfully", "data": data})

# Fetch all projects
@application.route('/api/projects', methods=['GET'])
def get_projects():
    projects = retrieve_project()
    return jsonify(projects)

# Add a new project
@application.route('/api/projects', methods=['POST'])
def add_new_project():
    """ Add a new project """
    try:
        project = request.json
        add_project(project)
        return jsonify({"message": "Project added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all project names and numbers   
@application.route('/api/projectslist', methods=['GET'])
def get_projectslist():
    try:
        project_names = get_project_list()
        return jsonify({"success": True, "data": project_names})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Get detailed information about a specific project    
@application.route("/api/projects/<string:project_id>/details", methods=["GET"])
def get_project_details(project_id):
    try:
        # Fetch project details
        project,members_list,total_hours = get_project_hours_pm(project_id)
        return jsonify({
            "success": True,
            "project": project,
            "members": members_list,
            "total_hours": total_hours
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Get AM timesheet data for a user between two dates    
@application.route("/api/timesheet/am/<username>/<start_date>/<end_date>", methods=["GET"])
def get_am_timesheet(username, start_date,end_date):
    # Convert input date format from MM-DD-YYYY to YYYY-MM-DD
    formatted_startDate = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
    formatted_endDate = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
    # Convert string dates to datetime objects
    start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
    end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
    # Check if start_date is after end_date
    if start > end:
        return jsonify({"message": "Start date cannot be after end date."}),500
    data = get_am_timesheet_between_dates(username,start,end)
    if not data:
            return jsonify({"message": "No data found for the given date range."}),404
    return jsonify({"message": "Success", "data": data})

# Get PM timesheet data for a user between two dates
@application.route("/api/timesheet/pm/<username>/<start_date>/<end_date>", methods=["GET"])
def get_pm_timesheet(username,start_date,end_date):
    # Convert input date format from MM-DD-YYYY to YYYY-MM-DD
    formatted_startDate = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
    formatted_endDate = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
    # Convert string dates to datetime objects
    start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
    end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
    # Check if start_date is after end_date
    if start > end:
        return {"message": "Start date cannot be after end date."},500
    data = get_pm_timesheet_between_dates(username,start,end)
    if not data:
            return {"message": "No data found for the given date range."},404
    return jsonify({"message": "Success", "data": data})

# Get performance matrices between two dates
@application.route("/api/matrices/<matrixUsername>/<matrixStartDate>/<matrixEndDate>", methods=["GET"])
def get_performance(matrixUsername,matrixStartDate,matrixEndDate):
    data = get_performance_between_dates(matrixUsername,matrixStartDate,matrixEndDate)
    return jsonify({"message": "Success", "data": data})

# Search project by name and number
@application.route("/api/projects/search", methods=["POST"])
def search_project():
    data = request.json
    project = get_project_detail(data["projectName"],data["projectNumber"])
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    return jsonify(project)

# @application.route("/api/users/email/<email>", methods=["POST"])
# def get_user(email):
#     user = user_details(email)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify(user)

# Delete a project by project name and number
@application.route("/api/projects/delete", methods=["POST"])
def delete_project_from_db():
    try:
        data = request.json
        result = delete_project(data["projectNumber"],data["projectName"])
        if result.deleted_count == 0:
                return jsonify({"message": "Project not found."}), 404
    
        return jsonify({"message": "Project removed successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Fetch user details by email
@application.route("/api/users/email/<email>", methods=["GET"])
def get_user(email):
    user = user_details(email)  # Fetch user from DB

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200

# Update user information
@application.route("/api/users/email/<string:email>", methods=["PUT"])
def edit_user(email):
    data = request.json
    result = update_user(email,data)
    return jsonify(result)

# Update project - incomplete function in your original code
@application.route("/api/projects/update", methods=["POST"])
def edit_project():
    try:
        data = request.json
        search_criteria = data.get("search", {})
        update_data = data.get("update", {})

        if not search_criteria or not update_data:
            return jsonify({"error": "Invalid request, missing search or update fields"}), 400

        result = update_project(search_criteria,update_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get project details between given start and end dates   
@application.route("/api/projects/<string:project_id>/details", defaults={'start_date': None, 'end_date': None}, methods=["GET"])
@application.route("/api/projects/<string:project_id>/details/<string:start_date>/<string:end_date>", methods=["GET"])
def get_project_details_between_dates(project_id, start_date, end_date):
    try:
      formatted_start_date = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
      formatted_end_date = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
      result = project_details_between_dates(project_id,formatted_start_date,formatted_end_date)
      return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Route to get user-specific projects within a date range
@application.route("/api/users/<user_email>/projects/<start_date>/<end_date>", methods=["GET"])
def get_user_projects(user_email, start_date, end_date):
    try:
      formatted_startDate = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
      formatted_endDate = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
      ## Convert string dates to datetime objects
      start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
      end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
      result = resource_management(user_email,start,end)
      return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#endpoint for leave request by naveen 
@application.route("/api/leave-request", methods=["POST"]) 
def leave_request_api():
    try:
        leave_data = request.json
        result = submit_leave_request(leave_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

# @application.route("/api/leave-request", methods=["GET", "POST"])
# def leave_request_api():
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     emp_collection = db["Employee_leavedetails"]

#     if request.method == "POST":
#         try:
#             leave_data = request.json
#             result = submit_leave_request(leave_data)  # your existing logic
#             return jsonify(result)
#         except Exception as e:
#             return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

#     elif request.method == "GET":
#         employee_name = request.args.get("name")
#         if not employee_name:
#             return jsonify({"success": False, "message": "Name is required"}), 400

#         employee = emp_collection.find_one({"name": employee_name})
#         if not employee:
#             return jsonify({"success": False, "message": "Employee not found"}), 404

#         total_leave = employee.get("Total_leave", 0)
#         leave_taken = employee.get("Leave_taken", 0)
#         remaining_leave = total_leave - leave_taken

#         return jsonify({
#             "success": True,
#             "name": employee_name,
#             "totalLeaves": total_leave,
#             "usedLeaves": leave_taken,
#             "remainingLeaves": remaining_leave
#         })
  
@application.route("/api/leave-request/available/<string:name>", methods=["GET"])
def get_leave_status(name):
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    emp_collection = db["Employee_leavedetails"]

    employee = emp_collection.find_one({"name": name})
    if not employee:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    total_leave = employee.get("Total_leave", 0)
    leave_taken = employee.get("Leave_taken", 0)
    remaining_leave = total_leave - leave_taken

    return jsonify({
        "success": True,
        "name": name,
        "Total_leave": total_leave,
        "Leave_taken": leave_taken,
        "Remaining_leave": remaining_leave
    })

@application.route('/api/leave-request', methods=['GET'])
def leave_requests_api():
    leave_requests = get_leave_requests()
    return jsonify(leave_requests)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  
    application.run(host="0.0.0.0", port=port)
    #application.run(host="0.0.0.0", port=port)

