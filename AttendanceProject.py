from cv2 import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time

""" This Script is for registering the employees in any organization Sep 10 2021 """ 

#path to get the employees pic and name 
path = 'AttendanceImages'
images = []
classNames = []
myList = os.listdir(path)

"""Reading the image file and creating the list of employees """
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    
print(classNames)

""" Encoding the faces """
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

""" Marking the attendance of employees """
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        NowTime = datetime.now().strftime('%H:%M:%S')
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            dateString = now.strftime('%Y-%d-%B')
            now = datetime.now()
            f.writelines(f'\n{name},{dtString},{dateString}')
            time.sleep(5)
        elif name in nameList and  str(NowTime) > "07:30:00":
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S.%f')
            dateString = now.strftime('%Y-%d-%B')
            now = datetime.now()
            f.writelines(f'\n{name},{dtString},{dateString},{"Exit"}')
            time.sleep(5)
            
            

# Getting the encodeListKnown
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

#strting the program and webcam
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

        # print(faceDis)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(10)

