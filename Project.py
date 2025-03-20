from pymongo import MongoClient


def add_project(project):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    collection.insert_one(project)
    

def retrieve_project():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Projects"]
    project_details = collection.find({}, {"project_number": 1, "project_name": 1, "start_date": 1, "end_date": 1, "_id": 0})
    project_details_list = list(project_details)

    return project_details_list

