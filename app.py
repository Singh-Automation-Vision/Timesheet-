from flask import Flask, request, jsonify
from pymongo import MongoClient
from Emp_timesheet import add_PM_data, add_AM_data, employee_login,performance_matrices, get_latest_employee_am_data
from Emp_info import add_emp_info
from flask_cors import CORS
import logging
from admin import add_new_user,delete_emp,get_emp_data,show_user
from Project import retrieve_project,add_project, get_project_list
#from pyngrok import ngrok
import os

application = Flask(__name__)

CORS(application) 
#CORS(application, resources={r"/*": {"origins": "*"}}) # Enable CORS for frontend-backend communication
#
## Start ngrok tunnel
#port = 8000  # Set the same port as Flask
#public_url = ngrok.connect(port).public_url
#print(f"Ngrok Tunnel URL: {public_url}")

@application.route("/")
def home():
    return jsonify({"message": "Backend is running successfully!"})

@application.route("/api/routes", methods=["GET"])
def get_routes():
    return jsonify([str(rule) for rule in application.url_map.iter_rules()])

logging.basicConfig(level=logging.DEBUG)

#@application.errorhandler(Exception)  # Capture all unhandled errors
#def handle_exception(e):
#    application.logger.error(f"Error: {e}", exc_info=True)
#    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

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



@application.route("/api/AM", methods=["POST"])
def add_AM_timesheet():
    data = request.json
    add_AM_data(data)
    return jsonify({"message": "Timesheet added successfully"})

@application.route("/api/PM", methods=["POST"])
def add_PM_timesheet():
    data = request.json
    #print(data)
    add_PM_data(data)
    return jsonify({"message": "Timesheet added successfully"})

@application.route("/api/users", methods=["POST"])
def new_users():
    data = request.json
    add_new_user(data)
    return jsonify({"message": "Timesheet added successfully"})

@application.route("/api/users/email/<string:email>", methods=["DELETE"])
def delete_user(email):
    
    delete_emp(email)
    return jsonify({"message": "Employee deleted successfully"})

@application.route("/api/matrices", methods=["POST"])
def matrices():
    data = request.json
    email = data.get("email")
    date = data.get("date")
    ratings = data.get("ratings")
    performance_matrices(email, date, ratings)
    return jsonify({"message": "Performance matrices updated successfully"})

@application.route("/api/add_employee", methods=["POST"])  # Fixed: Added missing route
def add_employee():
    emp_name = request.json
    add_emp_info(emp_name)
    return jsonify({"message": "Employee added successfully"})

@application.route("/api/timesheet/admin/<string:username>/<string:date>", methods=["GET"])
def get_timesheet(username, date):
    data = get_emp_data(username,date)
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

@application.route("/api/timesheet/user/<string:username>/<string:date>", methods=["GET"])
def get_user_timesheet(username, date):
    """
    Fetch timesheet data for a specific user and date.
    """
    try:
        # Convert the date string to the expected format
        timesheet_entry = get_latest_employee_am_data(username)
        if timesheet_entry:
            return jsonify({"success": True, "data": timesheet_entry}), 200
        else:
            return jsonify({"success": False, "message": "No timesheet found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
    
@application.route("/api/timesheet/showUser", methods=["GET"])
def user_details():
    data = show_user()
    return jsonify({"message": "Employee list fetched successfully", "data": data})

@application.route('/api/projects', methods=['GET'])
def get_projects():
    projects = retrieve_project()
    return jsonify(projects)

@application.route('/api/projects', methods=['POST'])
def add_new_project():
    """ Add a new project """
    try:
        project = request.json
        add_project(project)
        return jsonify({"message": "Project added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@application.route('/api/projectslist', methods=['GET'])
def get_projectslist():
    try:
        project_names = get_project_list()
        return jsonify({"success": True, "data": project_names})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  
    application.run(host="0.0.0.0", port=port)
    #application.run(host="0.0.0.0", port=port)




######## UPDATED APP.py


# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from Emp_timesheet import add_PM_data, add_AM_data, employee_login, performance_matrices, get_latest_employee_am_data
# from Emp_info import add_emp_info
# from flask_cors import CORS
# import logging
# from admin import add_new_user, delete_emp, get_emp_data, show_user
# from Project import retrieve_project, add_project, get_project_list
# import os
# from datetime import datetime  # Import datetime for date conversion

# application = Flask(__name__)

# CORS(application)  # Enable CORS for all origins
# # CORS(application, origins=["https://yourfrontend.com"])  # Restrict to specific frontend

# @application.route("/")
# def home():
#     return jsonify({"message": "Backend is running successfully!"})

# @application.route("/api/routes", methods=["GET"])
# def get_routes():
#     return jsonify([str(rule) for rule in application.url_map.iter_rules()])

# logging.basicConfig(level=logging.DEBUG)

# @application.route("/api/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data.get("email")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Username and password are required"}), 400

#     user_data = employee_login(username, password)

#     if user_data:
#         message = "Admin login successful" if username == "admin" else "Login successful"
#         return jsonify({"user": user_data, "message": message}), 200
#     else:
#         return jsonify({"error": "Invalid username or password"}), 401

# @application.route("/api/AM", methods=["POST"])
# def add_AM_timesheet():
#     data = request.json
#     add_AM_data(data)
#     return jsonify({"message": "Timesheet added successfully"})

# @application.route("/api/PM", methods=["POST"])
# def add_PM_timesheet():
#     data = request.json
#     add_PM_data(data)
#     return jsonify({"message": "Timesheet added successfully"})

# @application.route("/api/users", methods=["POST"])
# def new_users():
#     data = request.json
#     add_new_user(data)
#     return jsonify({"message": "User added successfully"})

# @application.route("/api/users/email/<string:email>", methods=["DELETE"])
# def delete_user(email):
#     delete_emp(email)
#     return jsonify({"message": "Employee deleted successfully"})

# @application.route("/api/matrices", methods=["POST"])
# def matrices():
#     data = request.json
#     email = data.get("email")
#     date = data.get("date")
#     ratings = data.get("ratings")
#     performance_matrices(email, date, ratings)
#     return jsonify({"message": "Performance matrices updated successfully"})

# @application.route("/api/add_employee", methods=["POST"])
# def add_employee():
#     emp_name = request.json
#     add_emp_info(emp_name)
#     return jsonify({"message": "Employee added successfully"})

# @application.route("/api/timesheet/admin/<string:username>/<string:date>", methods=["GET"])
# def get_timesheet(username, date):
#     data = get_emp_data(username, date)
#     return jsonify({"message": "Employee data fetched successfully", "data": data})

# @application.route("/api/timesheet/user/<string:username>/<string:date>", methods=["GET"])
# def get_user_timesheet(username, date):
#     """
#     Fetch timesheet data for a specific user and date with correct date format.
#     """
#     try:
#         # Convert date format from MM-DD-YYYY to YYYY-MM-DD
#         formatted_date = datetime.strptime(date, "%m-%d-%Y").strftime("%Y-%m-%d")

#         timesheet_entry = get_latest_employee_am_data(username, formatted_date)
#         if timesheet_entry:
#             return jsonify({"success": True, "data": timesheet_entry}), 200
#         else:
#             return jsonify({"success": False, "message": "No timesheet found"}), 404
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @application.route("/api/timesheet/showUser", methods=["GET"])
# def user_details():
#     data = show_user()
#     return jsonify({"message": "Employee list fetched successfully", "data": data})

# @application.route('/api/projects', methods=['GET'])
# def get_projects():
#     projects = retrieve_project()
#     return jsonify(projects)

# @application.route('/api/projects', methods=['POST'])
# def add_new_project():
#     try:
#         project = request.json
#         add_project(project)
#         return jsonify({"message": "Project added successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @application.route('/api/projectslist', methods=['GET'])
# def get_projectslist():
#     try:
#         project_names = get_project_list()
#         return jsonify({"success": True, "data": project_names})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# if __name__ == "__main__":  # Fixed incorrect _main typo
#     port = int(os.getenv("PORT", 8000))  
#     application.run(host="0.0.0.0", port=port)