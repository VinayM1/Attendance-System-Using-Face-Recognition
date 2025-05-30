import cv2
import face_recognition
import pickle
import os
from pymongo import MongoClient #MongoClient connects to MongoDB
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus#quote_plus handles special characters in passwords.
import gridfs#gridfs is used to store large files (like images) in MongoDB
#connecting MongoDB
username = "Vinay"
raw_password = "vinay3112"
password = quote_plus(raw_password)
uri = f"mongodb+srv://{username}:{password}@attendancesystemusingfa.7pc7r6j.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ Connection Error:", e)
    exit()

db = client["AttendanceSystemUsingFaceRecognition"]
fs = gridfs.GridFS(db)


#Importing Students Images
folderPath = "D:\Attendance System\Images"
modePathList = os.listdir(folderPath)
imgList = []
studentIds = []
# print(modePathList) To check if chosed correct path
for path in modePathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
   # print(path)
   # print(os.path.splitext(path)[0]) IT will seperate 'NUMBER' AND '.JPG' AND DICTIONARY [O] WILL ONLY GIVE ID
   # print(len(imgList)) To Test if List is Working
print(studentIds)
#Making A Function For Recognizing The Face Of The ID Holder
# --- Upload student images to MongoDB ---
for path in modePathList:
    student_id = os.path.splitext(path)[0]
    full_path = os.path.join(folderPath, path)

    # Remove old version if it exists
    for old in fs.find({"filename": student_id}):
        fs.delete(old._id)

    # Upload the new image
    with open(full_path, "rb") as f:
        fs.put(f, filename=student_id)

    print(f"✅ Uploaded {student_id}'s image to MongoDB")

def findEncoding(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
#print("Encoding Started....")
encodeListKnown = findEncoding(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]
#print("Encoding Completed....")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
#print("File Saved....")