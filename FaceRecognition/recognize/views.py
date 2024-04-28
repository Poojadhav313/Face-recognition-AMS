from ast import Str
from asyncio.windows_events import NULL
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import dataTable
from .models import attendanceTable
from .models import adminTable
from datetime import datetime

import pandas as pd

import face_recognition
import cv2
import numpy as np
import os

def home(request):
    return render(request, "recognize/home.html")

def login(request):
    if(request.method == 'GET'):
        return render(request, "recognize/login.html")

    if(request.method == 'POST'):
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        
        collection = adminTable
        document = collection.find_one({"userid" : userid})
        
        error = None
        
        if document:
        
            storedPass = document.get('password')
            
            if storedPass == password:


                return redirect('home_page')
        
            else:
                error = "Invalid Password"
                content = {'error' : error}
                return render(request, 'recognize/login.html', content)
        else:
            error = "Invalid UserID"
            content = {'error' : error}
            return render(request, 'recognize/login.html', content)

            

def capture(request):
    collection = dataTable
    cursor = collection.find()
    known_encodings = []
    known_names = []
    for document in cursor:
        known_encodings.append(document["encoding"])
        known_names.append(document["name"])

    # Initialize video capture
    cp = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
    matched_indices = set()

    while True:
        ret, frame1 = cp.read()
        frame = cv2.flip(frame1, 1)

        # Only process every other frame of video to save time
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color to RGB color
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"

                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    matched_indices.add(known_names[best_match_index])  #making set to store matched faces

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top - 30), (right, bottom + 30), (0, 0, 255), 2)

            # Draw label 
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 20), font, 0.6, (255, 255, 255), 1)
       
        cv2.imshow('Video', frame)
        

        if cv2.waitKey(1) == ord('q'):
            break
    
    print(matched_indices)
    
    for x in matched_indices:
        document = collection.find_one({"name" : x})

        shift = ""
        hr = datetime.now().strftime("%H:%M")
        if "15:00" < hr > "7:00":
            shift = "morning shift"
        elif "23:00" < hr > "15:00":
            shift = "evening shift"
        else:
            shift = "night shift"
            
        record = {
            "id" : document.get("_id"),
            "name" : x,
            "email" : document.get("email"),
            "phone" : document.get("phone"),
            "department" : document.get("department"),
            "role" : document.get("role"),
            "day" : datetime.now().day,
            "month" : datetime.now().month,
            "year" : datetime.now().year,
            "time" : datetime.now().strftime("%H:%M:%S"),
            "shift" : shift
            }
        attendanceTable.insert_one(record)

    cp.release()
    cv2.destroyAllWindows()
    return HttpResponse("running")

def addData(request): 
    savedNames = []
    collection = dataTable
    cursor = collection.find()
    for document in cursor:
        savedNames.append(document["name"])

    face = {}
    faceEncoding = {}
    x=0

    
    folder = "C:/Users/dell/Desktop/images/"
    imagesFolder = os.listdir(folder)

    try:
        df = pd.read_csv("C:/Users/dell/Desktop/data.csv")
    except:
        return HttpResponse("File not found")
    
    names = df["name"]
    emails = df["email"]
    phones =  df["phone"]
    departments = df["department"]
    roles = df["role"]
        
    count = 0

    if imagesFolder == []:
        return HttpResponse("no images to add")

    for name, email, phone, dep, role in  zip(names, emails, phones, departments, roles):
        
        
        name = name.lower()
        if name.split(".")[0] in savedNames:
            continue
            #return HttpResponse("data already exists")
       
        count = count + 1
        
        i = f"{name}.jpg"
        print(i)
    
    
        face["face{0}.format(x)"] = face_recognition.load_image_file(folder+i)
        faceEncoding["faceEncoding{0}.format(x)"] = face_recognition.face_encodings(face["face{0}.format(x)"])[0]

        x = x+1
        
        record = {
            "name" : name,
            "email" : email,
            "phone" : phone,
            "department" : dep,
            "role" : role,
            "encoding" : list(faceEncoding["faceEncoding{0}.format(x)"]),
            }
        dataTable.insert_one(record)
        
        #os.remove(folder+i)

    if count == 0:
        return HttpResponse("record already added")
    else:
        return HttpResponse("record added")

    