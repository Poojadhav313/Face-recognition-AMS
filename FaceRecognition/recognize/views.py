from ast import Str
from asyncio.windows_events import NULL
import datetime
from urllib import response
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
    if 'LoggedIn' not in request.session:   #checking if session created
        print("no ssessiion")
    else:
        #print(request.session['LoggedIn'])  #getting LoggedIn userid
        pass
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

                request.session['LoggedIn'] = userid    #session created

                return redirect('home_page')
        
            else:
                error = "Invalid Password"
                content = {'error' : error}
                return render(request, 'recognize/login.html', content)
        else:
            error = "Invalid UserID"
            content = {'error' : error}
            return render(request, 'recognize/login.html', content)
        
def loginReq(request):
    return render(request, 'recognize/loginreq.html')
    
def profile(request):
    if request.method == "GET":
        return render(request, 'recognize/profile.html')

    
    if (request.method == "POST"):
        form_type = request.POST.get("form_type")
        if form_type == "adddataBtnForm":
            #print("aaaaaaaaaaaa")
            error = addData(request)
            #print(error)
            context = {"error" : error}
            return render(request, "recognize/profile.html", context)

        if form_type == "logoutBtnForm":
            del request.session['LoggedIn']
            return redirect("home_page")
    
    return render(request, "recognize/aboutus.html")

def addData(request): 
    error = None
    
    savedNames = []
    collection = dataTable
    cursor = collection.find()
    for document in cursor:
        savedNames.append(document["name"])

    face = {}
    faceEncoding = {}
    x = 0

    
    folder = "C:/Users/dell/Desktop/images/"
    imagesFolder = os.listdir(folder)

    try:
        df = pd.read_csv("C:/Users/dell/Desktop/data.csv")
    except:
        error = "data.csv File not found"
        return error
    
    names = df["name"]
    emails = df["email"]
    phones =  df["phone"]
    departments = df["department"]
    roles = df["role"]
        
    count = 0

    if imagesFolder == []:
        error = "No image to add"
        return error

    for name, email, phone, dep, role in  zip(names, emails, phones, departments, roles):
        
        name = name.lower()
        if name in savedNames:
            continue  #skip if already exists
        
        i = f"{name}.jpg"
        #print(i)
        
        if folder + i not in imagesFolder:
            error = f"Image of {name} not found"
            return error
    
        face[f"face{x}"] = face_recognition.load_image_file(folder + i)
        faceEncoding[f"faceEncoding{x}"] = face_recognition.face_encodings(face[f"face{x}"])[0]

        record = {
            "name" : name,
            "email" : email,
            "phone" : phone,
            "department" : dep,
            "role" : role,
            "encoding" : list(faceEncoding[f"faceEncoding{x}"]),
        }
        collection.insert_one(record)
        
        x = x + 1
        count = count + 1
        
        # os.remove(folder + i)

    if count == 0:
        error = "No new records added"
    else:
        error = f"{count} new records added successfully"
    
    return error

def addData1(request): 
    error = None
    
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
        error = "File not found"
        return error
    
    names = df["name"]
    emails = df["email"]
    phones =  df["phone"]
    departments = df["department"]
    roles = df["role"]
        
    count = 0

    if imagesFolder == []:
        error = "No image to add"
        return error

    for name, email, phone, dep, role in  zip(names, emails, phones, departments, roles):
        
        temp = 0
        name = name.lower()
        if name.split(".")[0] in savedNames:
            temp = 1
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
        error = "Record already added"
        return error
    else:
        error = "Record added successfully"
        return error

def capture(request):
    if not 'LoggedIn' in request.session:
            return render(request, 'recognize/loginreq.html')

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

        # only process every other frame 
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # convert the image from BGR -> RGB
            rgb_small_frame = small_frame[:, :, ::-1]

            # find all faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"

                # use the known face 
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    matched_indices.add(known_names[best_match_index])  #making set to store matched faces

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # draw name box
            cv2.rectangle(frame, (left, top - 30), (right, bottom + 30), (0, 0, 255), 2)

            # draw name
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 20), font, 0.6, (255, 255, 255), 1)
       
        cv2.imshow('Press q to exit', frame)
        

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
    return redirect('home_page')

def viewData(request):
    if not 'LoggedIn' in request.session:
        return render(request, 'recognize/loginreq.html')

    collection = attendanceTable
    cursor = list(collection.find())

    names = set()
    emails = set()
    deps = set()
    roles = set()
    days = set()
    months = set()
    years = set()
    

    for document in cursor:
        names.add(document['name'])
        emails.add(document['email'])
        deps.add(document['department'])
        roles.add(document['role'])
        days.add(int(document['day']))
        months.add(int(document['month']))  
        years.add(int(document['year']))

    context = {'data': cursor, "name": names, "email" : emails, "dep": deps, "role": roles, "day" : days, "month" : months, "year" : years}

    if request.method == 'POST':
        selected_name = request.POST.get('name')
        selected_email = request.POST.get('email')
        selected_department = request.POST.get('department')
        selected_role = request.POST.get('role')
        selected_day = request.POST.get('day')
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')


        print(cursor)
        if selected_name:
            cursor = [doc for doc in cursor if doc['name'] == selected_name]
        if selected_email:
            cursor = [doc for doc in cursor if doc['email'] == selected_email]
        if selected_department:
            cursor = [doc for doc in cursor if doc['department'] == selected_department]
        if selected_role:
            cursor = [doc for doc in cursor if doc['role'] == selected_role]
        if selected_day:
            selected_day = int(selected_day)
            cursor = [doc for doc in cursor if doc['day'] == selected_day]
        if selected_month:
            selected_month = int(selected_month)
            cursor = [doc for doc in cursor if int(doc['month']) == selected_month]
        if selected_year:
            selected_year = int(selected_year)
            cursor = [doc for doc in cursor if doc['year'] == selected_year]
        

        context['data'] = cursor

    return render(request, 'recognize/viewdata.html', context)
