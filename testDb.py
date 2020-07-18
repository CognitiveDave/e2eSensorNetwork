import pymongo
import os
import json
from bson.json_util import dumps
import datetime

from datetime import date
today = date.today()
client = pymongo.MongoClient()
db = client.test



docs = []
cursor = db.readings.find()
for doc in cursor:
    del doc['_id']
    docs.append(doc)
        