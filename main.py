import cv2
import face_recognition
import os
import pickle
from EncodeGenerator import studentIds
import numpy as np
import cvzone
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import gridfs

# MongoDB connection
username = "username"
raw_password = "password"
password = quote_plus(raw_password)
uri = f"mongodb+srv://{username}:{password}@attendancesystemusingfa.7pc7r6j.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ Connection Error:", e)
    exit()

db = client["attendance_system"]
students_collection = db["students"]

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

imgBackground = cv2.imread("D:\\Attendance System\\Resources\\Modes\\Background.png")

# Load mode images
modeImages = [
    cv2.imread("D:\\Attendance System\\Resources\\Modes\\A.png"),
    cv2.imread("D:\\Attendance System\\Resources\\Modes\\B.avif"),
    cv2.imread("D:\\Attendance System\\Resources\\Modes\\C.jpg"),
    cv2.imread("D:\\Attendance System\\Resources\\Modes\\D.png"),
    cv2.imread("D:\\Attendance System\\Resources\\Modes\\E.png")
]

# Load encodings
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

modeType = 0
counter = 0
id = -1

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Resize background canvas
    imgBackground = cv2.resize(imgBackground, (1100, 600))

    # Place webcam image
    imgResized = cv2.resize(img, (345, 240))
    imgBackground[30:270, 50:395] = imgResized

    # Place mode image below webcam
    mode_img_height = 220
    imgModeDisplay = cv2.resize(modeImages[modeType], (345, mode_img_height))
    imgBackground[280:280 + mode_img_height, 50:395] = imgModeDisplay

    # Draw info panel
    cv2.rectangle(imgBackground, (450, 30), (1080, 470), (255, 255, 255), cv2.FILLED)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        print("MatchIndex", matchIndex)

        if matches[matchIndex]:
            print(studentIds[matchIndex])
            id = studentIds[matchIndex]
            counter = 1
            modeType = 1

            y1, x2, y2, x1 = faceLoc
            scale_x = 345 / 160
            scale_y = 240 / 120

            x1_resized = int(x1 * scale_x)
            x2_resized = int(x2 * scale_x)
            y1_resized = int(y1 * scale_y)
            y2_resized = int(y2 * scale_y)

            offset_x = 50
            offset_y = 30

            bbox = (offset_x + x1_resized, offset_y + y1_resized,
                    x2_resized - x1_resized, y2_resized - y1_resized)

            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            if counter == 0:
                counter = 1
                modeType = 1
        else:
            print("Not Known Face Detected")
            modeType = 4

    if counter != 0:
        if counter == 1:
            print(f"🔍 Searching for student ID in MongoDB: {str(id)}")
            studentinfo = students_collection.find_one({"_id": str(id)})

            if studentinfo:
                print("✅ Student Info:")
                for key, value in studentinfo.items():
                    print(f"{key}: {value}")

                # Text Colors
                light_gray = (200, 200, 200)
                dark_gray = (50, 50, 50)

                # Display Info
                text_start_x = 470
                text_start_y = 80
                line_spacing = 50

                def draw_info(label, value, y_offset):
                    label_pos = (text_start_x, text_start_y + y_offset)
                    value_pos = (text_start_x + 250, text_start_y + y_offset)

                    # Clear background behind value
                    (_, label_height), _ = cv2.getTextSize("Text", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(imgBackground, (value_pos[0] - 5, value_pos[1] - label_height),
                                  (value_pos[0] + 200, value_pos[1] + 10), (255, 255, 255), cv2.FILLED)

                    # Draw label and value
                    cv2.putText(imgBackground, f"{label}", label_pos,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, light_gray, 2)
                    cv2.putText(imgBackground, f"{value}", value_pos,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, dark_gray, 2)

                draw_info("Name:", studentinfo.get('name', 'Unknown'), 0)
                draw_info("Major:", studentinfo.get('major', 'Unknown'), line_spacing)
                draw_info("Year:", str(studentinfo.get('year', 'Unknown')), 2 * line_spacing)
                draw_info("Total Attendance:", str(studentinfo.get('total_attendance', 'Unknown')), 3 * line_spacing)

                modeType = 2
            else:
                print(f"❌ No info found in MongoDB for ID: {id}")
                modeType = 4
            counter += 1

        if counter > 20:
            modeType = 0
            counter = 0

    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(1)
