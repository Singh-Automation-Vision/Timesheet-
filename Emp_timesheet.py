import json
from pymongo import MongoClient
from mail import review_performance
from werkzeug.security import check_password_hash
from datetime import datetime



def convert_to_time_range(time_str):
    from datetime import datetime, timedelta
    
    try:
        start_time = datetime.strptime(time_str, "%I:%M %p")
        end_time = start_time + timedelta(hours=1)
        return f"{start_time.strftime('%I:%M')}-{end_time.strftime('%I:%M')}"
    except ValueError:
        return time_str  # Return as-is if format is unexpected


def transform_timesheet(data):
    transformed_data = {
        "employee_name": data["employee_name"],
        "date": data["date"],
        "hours": []
    }

    for hour, details in data["hours"].items():
        if details["description"].strip():  # Ignore empty descriptions
            transformed_data["hours"].append({
                "hour": convert_to_time_range(hour),
                "task": details["description"],
                "progress": details.get("status", "Not Set"),
                "comments": details.get("comment", "")
            })

    return transformed_data


def employee_login(emp_name,emp_password):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_credentials"]
    user = collection.find_one({"Username": emp_name}) 
    
    #for data in user:
    username = user["Username"]
    password = user["Password"]
    if username==emp_name and password==emp_password:
        if username=="admin":
    #if user and check_password_hash(user["Password"], emp_password):  # Verify hashed password
            return {"Username": user["Username"], "message": "Admin login successful"}
        else:
            return {"Username":user["Username"],"message":"Login successful"}
    
    
    else:
        return None

# def get_manager_details(emp_name):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_data"]

#     data = collection.find({"fullName":emp_name})

#     for value in data:
#         manager = value["managerName"]
#         mail = value["managerEmail"]
#     return manager,mail

def get_manager_details(emp_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]

    data = collection.find_one({"name": emp_name})

    if data:
        return data.get("manager"), data.get("manager_email")
    else:
        print(f"No manager found for employee: {emp_name}")
        return None, None  # Handle the case where no manager data is found
    

# def add_AM_data(data):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_AM"]

#     # Extract the first valid hour from "tasks" (not "hours")
#     first_am_hour = next(
#         (hour for hour, details in data.get("tasks", {}).items() if details.get("description")),
#         None
#     )

#     # Determine shift based on first valid hour
#     if first_am_hour:
#         shift = "USD" if first_am_hour.startswith("8") else "IND"
#     else:
#         shift = "UNKNOWN"  # Default shift if no valid hour is found

#     # Format hours list
#     formatted_hours = [
#         {"hour": hour, "task": details["description"]}
#         for hour, details in data.get("tasks", {}).items() if details["description"]
#     ]

#     # Create the final formatted document
#     formatted_data = {
#         "employee_name": data.get("employee_name"),
#         "date": data.get("date"),
#         "hours": formatted_hours,
#         "shift": shift  # Add shift field
#     }

#     # Insert into MongoDB
#     result = collection.insert_one(formatted_data)
#     print(f"AM Data inserted with record id: {result.inserted_id}")


def add_AM_data(data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_AM"]

    # Extract the first valid hour from "tasks"
    first_am_hour = next(
        (hour for hour, details in data.get("tasks", {}).items() if details.get("description")),
        None
    )

    # Determine shift based on first valid hour
    shift = "USD" if first_am_hour and first_am_hour.startswith("8") else "IND"

    # Format hours list
    formatted_hours = [
        {"hour": hour, "task": details["description"]}
        for hour, details in data.get("tasks", {}).items() if details["description"]
    ]

    # Define filter to check if the entry already exists
    filter_condition = {
        "employee_name": data.get("employee_name"),
        "date": data.get("date")
    }

    # Define the update operation
    update_data = {
        "$set": {
            "employee_name": data.get("employee_name"),  # Ensure it doesn't get removed
            "date": data.get("date"),  # Ensure date stays
            "hours": formatted_hours,
            "shift": shift  # Add or update the shift field
        }
    }

    print(f"Filter Condition: {filter_condition}")  # Debugging
    print(f"Update Data: {update_data}")  # Debugging

    # Update existing entry or insert new one
    result = collection.update_one(filter_condition, update_data, upsert=True)

    # Log the action taken
    if result.matched_count > 0:
        print(f"AM Data updated for {data.get('employee_name')} on {data.get('date')}")
    else:
        print(f"AM Data inserted for {data.get('employee_name')} on {data.get('date')}")

    print(f" Matched Count: {result.matched_count}, Modified Count: {result.modified_count}")  # Debugging

# def add_PM_data(data):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_PM"]

#     # Extract the first valid hour
#     first_pm_hour = next(
#         (hour for hour, details in data.get("hours", {}).items() if details.get("description")),
#         None
#     )

#     # Determine shift based on first valid hour
#     shift = "USD" if first_pm_hour and first_pm_hour.startswith("8") else "IND"

#     # Format hours list
#     formatted_hours = [
#         {
#             "hour": hour,
#             "task": details["description"],
#             "progress": details.get("status", "green").lower(),
#             "comments": details.get("comment", "")
#         }
#         for hour, details in data.get("hours", {}).items() if details.get("description")
#     ]

#     # Create the final formatted document
#     formatted_data = {
#         "employee_name": data.get("employee_name"),
#         "date": data.get("date"),
#         "hours": formatted_hours,
#         "shift": shift,  # Add shift field
#         "country": data.get("country")
#     }

#     # Insert into MongoDB (Overwrite if employee & date exist)
#     filter_condition = {
#         "employee_name": formatted_data["employee_name"],
#         "date": formatted_data["date"]
#     }
#     result = collection.update_one(
#         filter_condition, 
#         {"$set": formatted_data}, 
#         upsert=True  # Overwrite if exists, insert if not
#     )

#     if result.matched_count > 0:
#         print(f"Updated existing PM data for {formatted_data['employee_name']} on {formatted_data['date']}")
#     else:
#         print(f"Inserted new PM data for {formatted_data['employee_name']} on {formatted_data['date']}")


# def add_PM_data(data):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_pm = db["Employee_PM"]
#     try:
#         # Fetch latest AM date if PM date is missing or empty
        
#         latest_am_date = get_latest_am_date(data.get("employee_name"))
#         print(latest_am_date)
#         data["date"] = latest_am_date if latest_am_date else "No AM data found"

#         # Determine shift based on first valid hour
#         first_pm_hour = next((entry["hour"] for entry in data["hours"] if entry.get("task")), None)
#         shift = "USD" if first_pm_hour and first_pm_hour.startswith("8") else "IND"

#         # Format hours list correctly
#         formatted_hours = [
#             {
#                 "hour": entry["hour"],
#                 "task": entry["task"],
#                 "progress": entry.get("progress", "green").lower(),
#                 "comments": entry.get("comments", ""),
#                 "projectName": entry.get("projectName", "Unassigned")  # Ensure projectName is included
#             }
#             for entry in data["hours"] if entry.get("task")
#         ]

#         # Create the final formatted document
#         formatted_data = {
#             "employee_name": data.get("employee_name"),
#             "date": data.get("date"),
#             "hours": formatted_hours,
#             "shift": shift,
#             "country": data.get("country")
#         }

#         # Save to MongoDB (update if exists, insert if not)
#         filter_condition = {
#             "employee_name": formatted_data["employee_name"],
#             "date": formatted_data["date"]
#         }
#         result = collection_pm.update_one(filter_condition, {"$set": formatted_data}, upsert=True)

#         message = "Timesheet updated successfully" if result.matched_count > 0 else "Timesheet saved successfully"
#         return message
    
#     except Exception as e:
#         return f"Error: {str(e)}"

######### replcaing for 3 projects adding
def add_PM_data(data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_pm = db["Employee_PM"]
    employee_name = data.get("employee_name")
    try:
        if not employee_name:
            return {"error": "Employee name is required"}

        # Fetch latest AM date if PM date is missing or empty
        latest_am_date = get_latest_am_date(employee_name)
        data["date"] = latest_am_date 

        # Determine shift based on first valid hour
        first_pm_hour = next((entry["hour"] for entry in data["hours"] if entry.get("task")), None)
        shift = "USD" if first_pm_hour and first_pm_hour.startswith("8") else "IND"

        # Format hours list correctly, extracting multiple projects
        formatted_hours = []
        for entry in data["hours"]:
            if entry.get("task"):
                formatted_hours.append({
                    "hour": entry["hour"],
                    "task": entry["task"],
                    "progress": entry.get("progress", "green").lower(),
                    "comments": entry.get("comments", ""),
                    "projects": entry.get("projects", {})  # Keep it as a dictionary
                })

        # Create the final formatted document
        formatted_data = {
            "employee_name": employee_name,
            "date": data["date"],
            "hours": formatted_hours,
            "shift": shift,
            "country": data.get("country", "India")  # Default country if missing
        }

        # Save to MongoDB (update if exists, insert if not)
        filter_condition = {"employee_name": formatted_data["employee_name"], "date": formatted_data["date"]}
        result = collection_pm.update_one(filter_condition, {"$set": formatted_data}, upsert=True)

        message = "Timesheet updated successfully" if result.matched_count > 0 else "Timesheet saved successfully"
        return {"message": message, "data": formatted_data}

    except Exception as e:
        return {"error": str(e)}

# def performance_matrices(email, date, ratings):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_PM"]
#     print(ratings)

#     # Update the document where email and date match
#     result = collection.update_one(
#         {"employee_name": email, "date": date},  # Match condition
#         {"$set": {"ratings": ratings}}  # Update or insert the ratings field
#     )
#     emp_name = email
#     manager, mail = get_manager_details(emp_name)
#     user_input = collection.find_one({"employee_name": email, "date": date})
#     review_performance(user_input,manager,mail)

# def performance_matrices(email, date, ratings):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_PM"]
#     print(ratings)

#     # Update the document where email and date match
#     result = collection.update_one(
#         {"employee_name": email, "date": date},  # Match condition
#         {"$set": {"ratings": ratings}}  # Update or insert the ratings field
#     )

#     if result.matched_count == 0:
#         print(f"Warning: No matching document found for {email} on {date}. Insert operation might be needed.")

#     emp_name = email
#     manager, mail = get_manager_details(emp_name)

#     if manager and mail:  # Ensure manager and email exist before proceeding
#         user_input = collection.find_one({"employee_name": email, "date": date})
#         if user_input:
#             review_performance(user_input, manager, mail)
#         else:
#             print("Error: Could not retrieve updated employee data.")
#     else:
#         print("Error: Manager details missing, cannot proceed with performance review.")

#     return {"message": "Performance data updated successfully"}

"""Fix the performace matrix to get the data properly"""
def performance_matrices(email, date, ratings):

    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_PM"]
    recent_date = get_most_recent_date(email)
    if not recent_date:
        print("No records found for the employee.")
        return

    

    # Update the document where email and most recent date match
    result = collection.update_one(
        {"employee_name": email, "date": recent_date},  # Match condition
        {"$set": {"ratings": ratings}}  # Update the ratings field
    )

    # Fetch the updated document
    emp_name = email
    manager, mail = get_manager_details(emp_name)
    user_input = collection.find_one({"employee_name": email, "date": recent_date})

    # Call the review performance function
    review_performance(user_input, manager, mail)

def format_date_if_needed(date):
    try:
        # Check if the date is already in YYYY-MM-DD format
        datetime.strptime(date, "%Y-%m-%d")
        return date  # Return unchanged if correct format

    except ValueError:
        # Try converting from MM-DD-YYYY to YYYY-MM-DD
        try:
            date_obj = datetime.strptime(date, "%m-%d-%Y")
            return date_obj.strftime("%Y-%m-%d")  # Convert and return

        except ValueError:
            return None  # Invalid format, return None
        
def get_latest_employee_am_data(username, date):
    
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    pm_collection = db["Employee_PM"]
    am_collection = db["Employee_AM"]
    formatted_date = format_date_if_needed(date)
    
    if not formatted_date:
        return {"success": False, "error": "Invalid date format. Expected MM-DD-YYYY or YYYY-MM-DD"}

    # Check if PM data exists for the given date
    if pm_collection.find_one({"employee_name": username, "date": formatted_date}):
        return {"employee_name": None, "date": None, "hours": None, "tasks": None}

    # Get the latest AM data before the given date
    latest_am_data = am_collection.find_one(
        {"employee_name": username, "date": {"$lte": formatted_date}},  # Get AM data before the current date
        sort=[("date", -1)],  # Sort by date descending (most recent first)
        projection={"_id": 0}  # Exclude MongoDB _id field
    )

    # If no AM data exists, return empty response
    if not latest_am_data:
        return {"employee_name": None, "date": None, "hours": None, "tasks": None}

    # Recursive call to check if PM data exists for the found AM date
    return get_latest_employee_am_data(username, latest_am_data["date"]) if pm_collection.find_one({"employee_name": username, "date": latest_am_data["date"]}) else latest_am_data


# def get_latest_employee_am_data(username,date):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     pm_collection = db["Employee_PM"]
#     am_collection = db["Employee_AM"]
#     try:
#         date_obj = datetime.strptime(date, "%m-%d-%Y")  # Convert to datetime object
#         formatted_date = date_obj.strftime("%Y-%m-%d")  # Convert back to string
#     except ValueError:
#         return {"success": False, "error": "Invalid date format. Expected MM-DD-YYYY"}

    
#     pm_data_exists = pm_collection.find_one({"employee_name": username, "date": formatted_date})

#     if pm_data_exists:
#         return {"employee_name": None, "date": None, "hours": None, "tasks": None}

#     # If PM data does not exist, retrieve the latest AM data before the current date
#     latest_am_data = am_collection.find_one(
#         {"employee_name": username, "date": {"$lte": formatted_date}},  
#         sort=[("date", -1)],  # Sort by date descending (most recent first)
#         projection={"_id": 0}  # Exclude MongoDB _id field
#     )

#     return latest_am_data if latest_am_data else {"employee_name": None, "date": None, "hours": None, "tasks": None}
    

def get_most_recent_date(employee_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_PM"]
    latest_entry = collection.find_one(
        {"employee_name": employee_name},  # Filter by employee name
        sort=[("date", -1)]  # Sort by date in descending order
    )
    
    if latest_entry and "date" in latest_entry:
        try:
            # Convert the date to string in "YYYY-MM-DD" format
            recent_date = latest_entry["date"]
            if isinstance(recent_date, datetime):  # If stored as a datetime object
                return recent_date.strftime("%Y-%m-%d")
            elif isinstance(recent_date, str):  # If stored as a string
                return datetime.strptime(recent_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except Exception as e:
            print("Error parsing date:", e)
    
    return None  # Return None 

def get_latest_am_date(employee_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_am = db["Employee_AM"]
    latest_am_entry = collection_am.find_one(
        {"employee_name": employee_name},
        sort=[("date", -1)]  # Sort by date in descending order (latest first)
    )
    return latest_am_entry["date"] if latest_am_entry else None



#email = "Sudharshan"
#date = "2025-04-04"
#ratings = {
#     "Performance of the Day": "Green",
#     "First Time Quality": "Yellow",
#     "On-Time Delivery": "Red",
#     "Engagement and Support": "Red"
# }
#performance_matrices(email,date,ratings)
# get_latest_employee_am_data(email)
# print(get_latest_employee_am_data(email))
#print(get_latest_employee_am_data("Sudharshan","04-05-2025"))