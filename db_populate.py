import face_recognition
import cv2
import db


vincent = face_recognition.load_image_file("./vincent.jpg")
small = cv2.resize(vincent, (0, 0), fx=0.5, fy=0.5)
vincent_face_encoding = face_recognition.face_encodings(small)[0]
db.insert('Vincent', vincent_face_encoding)