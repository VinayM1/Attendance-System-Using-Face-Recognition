🎓 Face Recognition Attendance System
A real-time, AI-powered student attendance system using face recognition and MongoDB. This project automates the traditional attendance process by recognizing student faces through a webcam, verifying their identity, and logging attendance securely in a cloud database.

🧩 Key Features
✅ Real-Time Face Detection & Recognition
✅ Webcam Feed with Live Bounding Boxes
✅ Student Info Display with Clean UI
✅ Visual Mode Indicators (Searching, Found, Error, etc.)
✅ MongoDB Integration for Data Storage
✅ Highly Customizable and Scalable

📸 How It Works
The webcam captures live video feed.

Detected faces are compared with known encodings.

If matched, student details are fetched from MongoDB.

A status panel shows the student’s Name, Major, Year, and Total Attendance.

A visual mode image below the webcam indicates the system’s current state (e.g., scanning, success, error).

Attendance is confirmed and optionally stored.

💻 Tech Stack
Python 3

OpenCV – for image capture and processing

face_recognition – for facial recognition

MongoDB – for cloud database storage

cvzone – for UI overlays

pickle, gridfs, pymongo, numpy

