import json
from pymongo import MongoClient
from mail import review_performance
from werkzeug.security import check_password_hash
from datetime import datetime

# def add_new_user(user_input):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_emp = db["Employee_data"]    
#     result = collection_emp.insert_one(user_input)

def delete_emp(emp_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    collection_AM =db["Employee_AM"]
    collection_PM =db["Employee_PM"]
    collection.delete_one({"name": emp_name})
    collection_AM.delete_many({"employee_name": emp_name})
    collection_PM.delete_many({"employee_name": emp_name})

def get_emp_data(emp_name,date):
    try:
        formatted_date = datetime.strptime(date, "%m-%d-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use MM-DD-YYYY."}
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_PM"]
    collection_AM = db["Employee_AM"]
    emp_data_PM = collection.find_one({"employee_name": emp_name, "date": formatted_date},{"_id":0})
    emp_data_AM = collection_AM.find_one({"employee_name": emp_name, "date": formatted_date},{"_id":0})
    emp_data = { "PM": emp_data_PM, "AM": emp_data_AM }
    return emp_data


# def add_new_user(user_input):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_emp = db["Employee_data"]    
#     collection_credential = db["Employee_credentials"]
#     user_credential = { "Username": user_input["name"], "Password": user_input["password"] }
#     collection_emp.insert_one(user_credential)
#     collection_credential.insert_one(user_input)


def add_new_user(user_input):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_emp = db["Employee_data"]    
    collection_credential = db["Employee_credentials"]
    user_credential = { "Username": user_input["name"], "Password": user_input["password"] }
    collection_emp.insert_one(user_input)
    collection_credential.insert_one(user_credential)


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

def convert_date_format(data):
            for doc in data:
                if "date" in doc:
                    doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d").strftime("%m-%d-%Y")
            return data

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
        print(start,end)
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

def user_details(name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    result = list(collection.find({"name":name},{"_id":0}))
    print(result)
    return result

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
#start_date = "03-14-2025"
#end_date = "04-01-2025"
#formatted_startDate = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
#formatted_endDate = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
## Convert string dates to datetime objects
#start = datetime.strptime(formatted_startDate, "%Y-%m-%d")
#end = datetime.strptime(formatted_endDate, "%Y-%m-%d")
#print(get_pm_timesheet_between_dates("Sudharshan",start,end))