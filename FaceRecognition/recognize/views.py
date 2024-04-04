from ast import Str
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import DBtable

import face_recognition
import cv2
import numpy as np
import os

def home(request):
    return render(request, "recognize/home.html")


def addData(request):  

    face = {}
    faceEncoding = {}
    x=0

    folder = "C:/Users/dell/Desktop/images/"

    imagesFolder = os.listdir(folder)
    for i in imagesFolder:
        li = i.split('.')[0]
        print(li)
    
    
        face["face{0}.format(x)"] = face_recognition.load_image_file(folder+i)
        faceEncoding["faceEncoding{0}.format(x)"] = face_recognition.face_encodings(face["face{0}.format(x)"])[0]

        x = x+1
        
        record = {
            "name" : li,
            "encoding" : list(faceEncoding["faceEncoding{0}.format(x)"]),
            }
        DBtable.insert_one(record)
        
        os.remove(folder+i)

    return HttpResponse("record added")

    