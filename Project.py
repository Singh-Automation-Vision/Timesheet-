from pymongo import MongoClient
from collections import OrderedDict

def add_project(project):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    collection.insert_one(project)
    

# def retrieve_project():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Projects"]
#     project_details = collection.find({}, {"projectNumber": 1, "projectName": 1, "startDate": 1, "endDate": 1, "_id": 0})
#     project_details_list = list(project_details)

#     return project_details_list

def retrieve_project():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    project_details = collection.find({}, {"_id": 0, "projectName": 1, "projectNumber": 1, "startDate": 1, "endDate": 1})
    
    ordered_projects = [
        OrderedDict([
            ("projectNumber", project["projectNumber"]),
            ("projectName", project["projectName"]),
            ("startDate", project["startDate"]),
            ("endDate", project["endDate"])
        ])
        for project in project_details
    ]

    return ordered_projects

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

# print(retrieve_project())