import json
from pymongo import MongoClient
from mail import review_performance
from werkzeug.security import check_password_hash
from datetime import datetime
from Project import get_designation

# def add_new_user(user_input):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_emp = db["Employee_data"]    
#     result = collection_emp.insert_one(user_input)

# Delete employee from database
def delete_emp(emp_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    collection_credential = db["Employee_credentials"]
    collection_AM =db["Employee_AM"]
    collection_PM =db["Employee_PM"]
    collection.delete_one({"name": emp_name})
    collection_credential.delete_one({"Username": emp_name})
    collection_AM.delete_many({"employee_name": emp_name})
    collection_PM.delete_many({"employee_name": emp_name})

#Get employee data for a given date
#def get_emp_data(emp_name,date):
#    try:
#        formatted_date = datetime.strptime(date, "%m-%d-%Y").strftime("%Y-%m-%d")
#    except ValueError:
#        return {"error": "Invalid date format. Use MM-DD-YYYY."}
#    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#    db = client["Timesheet"]
#    collection = db["Employee_PM"]
#    collection_AM = db["Employee_AM"]
#    emp_data_PM = collection.find_one({"employee_name": emp_name, "date": formatted_date},{"_id":0})
#    emp_data_AM = collection_AM.find_one({"employee_name": emp_name, "date": formatted_date},{"_id":0})
#    emp_data = { "PM": emp_data_PM, "AM": emp_data_AM }
#    return emp_data


# def add_new_user(user_input):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_emp = db["Employee_data"]    
#     collection_credential = db["Employee_credentials"]
#     user_credential = { "Username": user_input["name"], "Password": user_input["password"] }
#     collection_emp.insert_one(user_credential)
#     collection_credential.insert_one(user_input)

# Add new employee to the database
def add_new_user(user_input):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_emp = db["Employee_data"]    
    collection_credential = db["Employee_credentials"]
    user_credential = { "Username": user_input["name"], "Password": user_input["password"] }
    collection_emp.insert_one(user_input)
    collection_credential.insert_one(user_credential)

# Retrieve employee details to display in frontend
def show_user():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]  # Change to your collection name

    # Query to fetch only the required fields (excluding _id)
    query = {}
    projection = {"_id": 0, "name": 1, "email": 1, "manager": 1, "designation": 1}
    
    # Fetch the data
    # results = collection.find(query, projection)
    results = list(collection.find(query, projection))
    # print(results)
    return results

# Convert the date format as per the frontend
def convert_date_format(data):
            for doc in data:
                if "date" in doc:
                    doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d").strftime("%m-%d-%Y")
            return data

# Retrive timesheet data for given date range
def get_timesheet_between_dates(emp_name,startDate,endDate):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_PM = db["Employee_PM"]
    collection_AM = db["Employee_AM"]
    try:
        # Convert input date format from MM-DD-YYYY to YYYY-MM-DD
        formatted_startDate = datetime.strptime(startDate, "%m-%d-%Y").strftime("%Y-%m-%d")
        formatted_endDate = datetime.strptime(endDate, "%m-%d-%Y").strftime("%Y-%m-%d")

        # Convert string dates to datetime objects
        start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
        end = datetime.strptime(formatted_endDate, "%Y-%m-%d")

        # Check if start_date is after end_date
        if start > end:
            return {"error": "Start date cannot be after end date."}

        # MongoDB query (convert stored string dates to datetime)
        query = {
            "$expr": {
                "$and": [
                    {"$gte": [{"$dateFromString": {"dateString": "$date"}}, start]},
                    {"$lte": [{"$dateFromString": {"dateString": "$date"}}, end]}
                ]
            },
            "employee_name": emp_name  # Filter by employee name
        }

        # Fetch PM and AM data
        emp_data_PM = list(collection_PM.find(query, {"_id": 0}))
        emp_data_AM = list(collection_AM.find(query, {"_id": 0}))
        
        emp_data_PM = convert_date_format(emp_data_PM)
        emp_data_AM = convert_date_format(emp_data_AM)


        # If no data found
        if not emp_data_PM and not emp_data_AM:
            return {"message": "No data found for the given date range."}

        # Return the combined result
        return {"PM": emp_data_PM, "AM": emp_data_AM}

    except ValueError:
        return {"error": "Invalid date format. Use MM-DD-YYYY."}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Retrieve PM sheet of an employee for a given date range
def get_pm_timesheet_between_dates(emp_name,start,end):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_PM = db["Employee_PM"]
    #try:
    #    # Convert input date format from MM-DD-YYYY to YYYY-MM-DD
    #    formatted_startDate = datetime.strptime(startDate, "%m-%d-%Y").strftime("%Y-%m-%d")
    #    formatted_endDate = datetime.strptime(endDate, "%m-%d-%Y").strftime("%Y-%m-%d")
#
    #    # Convert string dates to datetime objects
    #    start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
    #    end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
#
    #    # Check if start_date is after end_date
    #    if start > end:
    #        return {"error": "Start date cannot be after end date."}

        # MongoDB query (convert stored string dates to datetime)
    query = {
        "$expr": {
            "$and": [
                {"$gte": [{"$dateFromString": {"dateString": "$date"}}, start]},
                {"$lte": [{"$dateFromString": {"dateString": "$date"}}, end]}
            ]
        },
        "employee_name": emp_name  # Filter by employee name
    }
    # Fetch AM data
    emp_data_PM = list(collection_PM.find(query, {"_id": 0,"ratings":0}))
    
    
    emp_data_PM = convert_date_format(emp_data_PM)

    #print(emp_data_PM)

        # If no data found
        #if not emp_data_PM:
        #    return {"message": "No data found for the given date range."}

        # Return the combined result
    return emp_data_PM

    #except ValueError:
    #    return {"error": "Invalid date format. Use MM-DD-YYYY."}
#
    #except Exception as e:
    #    return {"error": f"An unexpected error occurred: {str(e)}"}
    
# Retrieve AM sheet of an employee for a given date range
def get_am_timesheet_between_dates(emp_name,start,end):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_AM = db["Employee_AM"]
    #try:
        # Convert input date format from MM-DD-YYYY to YYYY-MM-DD
        #formatted_startDate = datetime.strptime(startDate, "%m-%d-%Y").strftime("%Y-%m-%d")
        #formatted_endDate = datetime.strptime(endDate, "%m-%d-%Y").strftime("%Y-%m-%d")
#
        ## Convert string dates to datetime objects
        #start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
        #end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
#
        ## Check if start_date is after end_date
        #if start > end:
        #    return {"message": "Start date cannot be after end date."}

        # MongoDB query (convert stored string dates to datetime)
    query = {
        "$expr": {
            "$and": [
                {"$gte": [{"$dateFromString": {"dateString": "$date"}}, start]},
                {"$lte": [{"$dateFromString": {"dateString": "$date"}}, end]}
            ]
        },
        "employee_name": emp_name  # Filter by employee name
    }
    # Fetch AM data
    emp_data_AM = list(collection_AM.find(query, {"_id": 0,"ratings":0}))
    
    
    emp_data_AM = convert_date_format(emp_data_AM)
        

        # If no data found
        #if not emp_data_AM:
        #    return {"message": "No data found for the given date range."}

        # Return the combined result
    return emp_data_AM

    #except ValueError:
    #    return {"error": "Invalid date format. Use MM-DD-YYYY."}
#
    #except Exception as e:
    #    return {"error": f"An unexpected error occurred: {str(e)}"}

# Retrieve performance matrices of an employee for a given date range
def get_performance_between_dates(emp_name,startDate,endDate):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_PM = db["Employee_PM"]
    try:
        # Convert input date format from MM-DD-YYYY to YYYY-MM-DD
        formatted_startDate = datetime.strptime(startDate, "%m-%d-%Y").strftime("%Y-%m-%d")
        formatted_endDate = datetime.strptime(endDate, "%m-%d-%Y").strftime("%Y-%m-%d")

        # Convert string dates to datetime objects
        start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
        end = datetime.strptime(formatted_endDate, "%Y-%m-%d")

        # Check if start_date is after end_date
        if start > end:
            return {"error": "Start date cannot be after end date."}
        
        # MongoDB query (convert stored string dates to datetime)
        query = {
            "$expr": {
                "$and": [
                    {"$gte": [{"$dateFromString": {"dateString": "$date"}}, start]},
                    {"$lte": [{"$dateFromString": {"dateString": "$date"}}, end]}
                ]
            },
            "employee_name": emp_name  # Filter by employee name
        }

        # Fetch AM data
        emp_data_PM = list(collection_PM.find(query, {"_id": 0,"hours":0}))
        
        
        emp_data_PM = convert_date_format(emp_data_PM)

        #for emp in emp_data_PM:
        #    print(emp)

        # If no data found
        if not emp_data_PM:
            return {"message": "No data found for the given date range."}

        # Return the combined result
        return emp_data_PM

    except ValueError:
        return {"error": "Invalid date format. Use MM-DD-YYYY."}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Retrieve list of employees from database
def user_details(name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    result = list(collection.find({"name":name},{"_id":0}))
    
    return result

# Update Employee information in database
def update_user(name,updated_data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    user = collection.find_one({"name": name})
    if not user:
            return {"error": "User not found"}
    
    result = collection.update_one({"name": name}, {"$set": updated_data})

    if result.modified_count == 0:
        return {"error": "No updates applied"}
    else:
        return {"message": "User updated successfully"}

# Retrive employee data from the database for a given date range    
def resource_management(employee_name,start_date,end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_PM"]
    
    
    #print(type(start_date),type(end_date))

    #Mongodb query pipeline
    pipeline = [
    {"$match": {
        "employee_name": employee_name,
        "date": {"$gte": start_date_str, "$lte": end_date_str}
    }},
    {"$unwind": "$hours"},
    {"$project": {
        "hour": "$hours.hour",
        "projects_array": {"$objectToArray": "$hours.projects"}
    }},
    {"$addFields": {
        "project_count": {"$size": "$projects_array"}
    }},
    {"$unwind": "$projects_array"},
    {"$project": {
        "project_name": "$projects_array.v",
        "partial_hour": {"$divide": [1, "$project_count"]}  # 1 hour divided among all projects
    }},
    {"$group": {
        "_id": "$project_name",
        "hours": {"$sum": "$partial_hour"}
    }},
    {"$project": {
        "_id": 0,
        "project_name": "$_id",
        "hours": {"$round": ["$hours", 2]}
    }}
]

    print(f"Querying for employee: {employee_name}, Start Date: {start_date}, End Date: {end_date}")
    
    designation = get_designation(employee_name)
    
    project_data = list(collection.aggregate(pipeline))
    total_hours = sum(item["hours"] for item in project_data)
    response_data = {    #Employee data contains employee name, designation, list of projects and total hours spent 
            "data": {
                "user_details": {
                    "name": employee_name,
                    "designation": designation
                },
                "projects": project_data,
                "total_hours": round(total_hours,2)
            }
        }

    return response_data
    

# data = {
#   "name": "Sudharshan",
#   "email": "sudharshan.ng@singhautomation.com",
#   "role": "user",
#   "country": "India",
#   "manager": "Soorya",
#   "manager_email": "soorya@singhus.com",
#   "designation": "Machine Vision Engineer"
# }
# update_user("Sudharshan",data)

# user_details("Sudharshan")
#start_date = "03-28-2025"
#end_date = "04-10-2025"
##
#formatted_startDate = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
#formatted_endDate = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
#### Convert string dates to datetime objects
#start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
#end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
#data = get_am_timesheet_between_dates("Bhargav",start_date,end_date)
#
#if not data:
#    print("no data")
#print(data)
#start_date = datetime.strptime(start_date, "%Y-%m-%d")
#end_date = datetime.strptime(end_date, "%Y-%m-%d")

#print(resource_management("Kanakasri",start,end))