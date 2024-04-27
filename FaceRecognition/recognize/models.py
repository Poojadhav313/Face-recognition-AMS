from django.db import models

import pymongo

url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)

db = client['faces_encoded']
#DBtable = db['recog']

DBtable = db['faces']