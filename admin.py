import json
from pymongo import MongoClient
from mail import review_performance
from werkzeug.security import check_password_hash
from datetime import datetime

# def add_new_user(user_input):
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client["Timesheet"]
#     collection_emp = db["Employee_data"]    
#     result = collection_emp.insert_one(user_input)

def delete_emp(emp_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    collection_AM =db["Employee_AM"]
    collection_PM =db["Employee_PM"]
    collection.delete_one({"email": emp_name})
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
#     client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
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
