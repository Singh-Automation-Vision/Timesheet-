from pymongo import MongoClient
from collections import OrderedDict
from datetime import datetime

def add_project(project):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    collection.insert_one(project)
    

def get_project_list():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]  # Change to your collection name

    query = {}
    projection = {"_id": 0, "projectName": 1}
    
    # Fetch the data
    results = list(collection.find(query, projection))
    
    # Extract only project names into a list
    project_names = [proj["projectName"] for proj in results]

    return project_names

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%m-%d-%y")
    except (ValueError, TypeError):
        return date_str  # If the format is incorrect or None, return as is


def retrieve_project():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    project_details = collection.find({}, {"_id": 0, "projectName": 1, "projectNumber": 1, "startDate": 1, "endDate": 1})
    
    
    ordered_projects = [
        OrderedDict([
            ("projectNumber", project["projectNumber"]),
            ("projectName", project["projectName"]),
            ("startDate", format_date(project["startDate"])),
            ("endDate", format_date(project["endDate"]))
        ])
        for project in project_details
    ]
    #print(ordered_projects)

    return ordered_projects

# def get_project_detail(project_name,projectNumber):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Projects"]

#     data = list(collection.find({"projectName":project_name,"projectNumber":projectNumber},{"_id":0}))

#     return data

def get_project_detail(project_name,projectNumber):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]

    data = list(collection.find({"projectName":project_name,"projectNumber":projectNumber},{"_id":0}))
    data[0]["startDate"] = format_date(data[0]["startDate"])
    data[0]["endDate"] = format_date(data[0]["endDate"])

    return data

def get_designation(employee_name):
    # print(employee_name)
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]

    data = collection.find({"name":employee_name})

    for value in data:
        designation = value["designation"]

    return designation


# def get_project_hours_pm(project_name):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_pm = db["Employee_PM"]


#     try:
#         pipeline = [
#             {
#                 "$unwind": "$hours"  # Flatten the hours array
#             },
#             {
#                 "$match": {
#                     "hours.projectName": project_name  # Filter by project
#                 }
#             },
#             {
#                 "$group": {
#                     "_id": "$employee_name",  # Group by employee
#                     "total_hours": {"$sum": 1}  # Count total hours spent
#                 }
#             }
#         ]

#         pm_data = list(collection_pm.aggregate(pipeline))

#         # List of employees and their hours
#         employees_list = [
#             {
#                 "employee_name": emp["_id"],
#                 "designation": get_designation(emp["_id"]),
#                 "hours": emp["total_hours"]
#             }
#             for emp in pm_data
#         ]
        
#         project = get_project_detail(project_name)

#         # Calculate total hours spent on the project
#         total_project_hours = sum(emp["hours"] for emp in employees_list)

#         # print(total_project_hours)
#         # print(employees_list)
#         return project[0],employees_list,total_project_hours

#     except Exception as e:
#         return {"error": str(e)}

# def get_project_hours_pm(project_name):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection_pm = db["Employee_PM"]
#     collection = db["Projects"]
#     try:
#         pipeline = [
#             {
#                 "$unwind": "$hours"  # Flatten the hours array
#             },
#             {
#                 "$match": {
#                     "hours.projectName": project_name  # Filter by project
#                 }
#             },
#             {
#                 "$group": {
#                     "_id": "$employee_name",  # Group by employee
#                     "total_hours": {"$sum": 1}  # Count total hours spent
#                 }
#             }
#         ]

#         pm_data = list(collection_pm.aggregate(pipeline))

#         # List of employees and their hours
#         employees_list = [
#             {
#                 "employee_name": emp["_id"],
#                 "designation": get_designation(emp["_id"]),
#                 "hours": emp["total_hours"]
#             }
#             for emp in pm_data
#         ]
        
#         project = list(collection.find({"projectName":project_name},{"_id":0}))

#         # Calculate total hours spent on the project
#         total_project_hours = sum(emp["hours"] for emp in employees_list)

        
#         return project[0],employees_list,total_project_hours

#     except Exception as e:
#         return {"error": str(e)}



##### replacing for 3 projects 
def get_project_hours_pm(project_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_pm = db["Employee_PM"]
    
    collection = db["Projects"]
    try:
        if not project_name:
            return {"error": "Project name is required"}
    
        # Aggregation pipeline to distribute time correctly
        pipeline = [
            {"$unwind": "$hours"},  # Flatten the hours array
            {"$project": {  
                "employee_name": 1,
                "hour": "$hours.hour",
                "projects": {"$objectToArray": "$hours.projects"}  # Convert project dict to an array of key-value pairs
            }},
            {"$unwind": "$projects"},  # Flatten project dictionary
            {"$group": {
                "_id": {"employee": "$employee_name", "hour": "$hour"},
                "projects_list": {"$addToSet": "$projects.v"}  # Collect unique project names for the hour
            }},
            {"$project": {
                "_id": 1,
                "total_projects": {"$size": "$projects_list"},  # Count the number of projects per hour
                "employee": "$_id.employee",
                "hour": "$_id.hour",
                "projects_list": 1
            }},
            {"$match": {"projects_list": project_name}},  # Ensure project_name is in the project list
            {"$group": {
                "_id": "$employee",
                "total_minutes": {"$sum": {"$divide": [60, "$total_projects"]}}  # Distribute 60 min per project
            }}
        ]
    
        pm_data = list(collection_pm.aggregate(pipeline))
    
        # Prepare the employee list with adjusted hours
        employees_list = [
            {
                "employee_name": emp["_id"],
                "designation": get_designation(emp["_id"]),
                "hours": round(emp["total_minutes"] / 60, 2)  # Convert minutes to hours
            }
            for emp in pm_data if emp["_id"]
        ]
    
        # Retrieve project details
        project = collection.find_one({"projectName": project_name}, {"_id": 0})
    
        if not project:
            return {"error": f"Project '{project_name}' not found"}
    
        # Format project start and end dates if they exist
        project["startDate"] = format_date(project["startDate"]) if "startDate" in project else "N/A"
        project["endDate"] = format_date(project["endDate"]) if "endDate" in project else "N/A"
    
        # Calculate total hours spent on the project
        total_project_hours = sum(emp["hours"] for emp in employees_list)
    
        return project, employees_list, total_project_hours

    except Exception as e:
        return {"error": str(e)}

def delete_project(project_number,project_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    result = collection.delete_one({"projectName":project_name})
    return result

def update_project(query,updated_data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    projects_collection = db["Projects"]
    project = projects_collection.find_one(query)
    print(query)
    if not project:
        return {"error": "Project not found"}
    # Update project data
    result = projects_collection.update_one(query, {"$set": updated_data})
    if result.modified_count == 0:
        return {"error": "No updates applied"}
    return {"message": "Project updated successfully"}

def project_details_between_dates(project_name,start_date,end_date):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection_pm = db["Employee_PM"]
    collection = db["Projects"]

    #try:
    #    if not project_name:
    #        return {"error": "Project name is required"}
    #    
    #    formatted_start_date = datetime.strptime(start_date, "%m-%d-%Y").strftime("%Y-%m-%d")
    #    formatted_end_date = datetime.strptime(end_date, "%m-%d-%Y").strftime("%Y-%m-%d")
    #    
    #    
#
    #    if not formatted_start_date or not formatted_end_date:
    #        return {"error": "Invalid date format. Expected YYYY-MM-DD or MM-DD-YYYY"}

    pipeline = [
    # Step 1: Filter by date range
    {"$match": {
        "date": {"$gte": start_date, "$lte": end_date}  # Filter based on date as a string
    }},

    # Step 2: Unwind the hours array to process each hour individually
    {"$unwind": "$hours"},

    # Step 3: Convert project dictionary to an array of key-value pairs
    {"$project": {
        "employee_name": 1,
        "hour": "$hours.hour",
        "projects": {"$objectToArray": "$hours.projects"}  # Convert project dict to key-value array
    }},

    # Step 4: Unwind the projects array
    {"$unwind": "$projects"},

    # Step 5: Group by employee and hour, collecting a unique list of projects per hour
    {"$group": {
        "_id": {"employee": "$employee_name", "hour": "$hour"},
        "projects_list": {"$addToSet": "$projects.v"}  # Store unique project names per hour
    }},

    # Step 6: Count the total number of projects per hour
    {"$project": {
        "_id": 1,
        "total_projects": {"$size": "$projects_list"},  # Get project count per hour
        "employee": "$_id.employee",
        "hour": "$_id.hour",
        "projects_list": 1
    }},

    # Step 7: Ensure the required project is in the list of projects for that hour
    {"$match": {"projects_list": project_name}},

    # Step 8: Distribute the 60 minutes across the number of projects in that hour
    {"$group": {
        "_id": "$employee",
        "total_hours": {"$sum": {"$divide": [60, "$total_projects"]}}  # Allocate time equally
    }}
    ]

    pm_data = list(collection_pm.aggregate(pipeline))
        

        # Prepare the list of employees working on the project
    employees_list = [
        {
            "employee_name": emp["_id"],
            "designation": get_designation(emp["_id"]),
            "hours": round(emp["total_hours"] / 60, 2)  # Convert minutes to hours
        }
        for emp in pm_data if emp["_id"]
    ]

        # Retrieve project details
    project = collection.find_one({"projectName": project_name}, {"_id": 0})

        #if not project:
        #    return {"error": f"Project '{project_name}' not found"}

        # Format project start and end dates if they exist
    project["startDate"] = format_date(project["startDate"]) if "startDate" in project else "N/A"
    project["endDate"] = format_date(project["endDate"]) if "endDate" in project else "N/A"
    # Calculate total hours spent on the project
    total_project_hours = sum(emp["hours"] for emp in employees_list)

    return {
        "project_details": project,
        "employees": employees_list,
        "total_project_hours": total_project_hours
    }

    #except Exception as e:
    #    return {"error": str(e)}
    
#print(get_project_hours_pm("Nash green house "))
#print(project_details_between_dates("Nash green house ","03-01-2025","03-25-2025"))
