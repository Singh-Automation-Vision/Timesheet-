from pymongo import MongoClient

def add_emp_info(emp_data):
    client = MongoClient("mongodb+srv://prashitar:Vision123@cluster0.v7ckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    
    result = collection.insert_one(emp_data)
    print(f"Data inserted with record id: {result.inserted_id}")

#user_data = {
#    "fullName": "Sudharshan",
#    "email": "sudharshan@singhautomation.com",
#    "password": "1234",
#    "role": "Machine vision engineer",
#    "country": "IND",
#    "managerName": "Soorya",
#    "managerEmail": "prashita.r@singhautomation.com"
#}

#add_emp_info(user_data)