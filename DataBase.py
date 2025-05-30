from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from urllib.parse import quote_plus


# --- Connection Setup ---
username = "UserName"
raw_password = "Password"  # <-- Update if needed
password = quote_plus(raw_password)

uri = f"mongodb+srv://{username}:{password}@attendancesystemusingfa.7pc7r6j.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(uri, server_api=ServerApi('1'))

# --- Test Connection ---
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
    exit()

# --- Define Database and Collection ---
db = client["attendance_system"]
students_collection = db["students"]

# --- Sample Student Data ---
student_data = [
    {
        "_id": "0000",
        "name": "Elon Musk",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 6,
        "standing": "G",
        "year": 4,
        "last_attendance_time": datetime.strptime("2022-12-11 00:54:34", "%Y-%m-%d %H:%M:%S")
    },
    {
        "_id": "1111",
        "name": "Bill Gates",
        "major": "Computer Science",
        "starting_year": 2016,
        "total_attendance": 9,
        "standing": "A",
        "year": 2,
        "last_attendance_time": datetime.strptime("2022-12-11 00:54:34", "%Y-%m-%d %H:%M:%S")
    },
    {
        "_id": "2222",
        "name": "Alex",
        "major": "Electronics & Communication ",
        "starting_year": 2025,
        "total_attendance": 23,
        "standing": "A",
        "year": 2,
        "last_attendance_time": datetime.strptime("2022-12-11 00:54:34", "%Y-%m-%d %H:%M:%S")
    }
]

# Insert/Update each student
for student in student_data:
    students_collection.replace_one({"_id": student["_id"]}, student, upsert=True)

print("✅ All student data inserted/updated in MongoDB.")
