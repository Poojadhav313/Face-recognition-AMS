from django.db import models

import pymongo

url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)

db = client['faces_encoded']
#DBtable = db['recog']

dataTable = db['faces'] #stored data table

attendanceTable = db['attendance'] #to store attendance in

adminTable = db['admin'] #admin table