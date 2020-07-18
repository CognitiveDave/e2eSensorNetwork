#!/usr/bin/python3.5
#-*-coding: utf-8 -*-
import pymongo
import os
import json
from bson.json_util import dumps
import datetime

from datetime import date
today = date.today()

_id = ""

class DBHelper:

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client[_id]

    def add(self, record):
        self.db.readings.insert_one(record)
        self.client.close()

    def all(self):
        docs = []
        cursor = self.db.readings.find()
        for doc in cursor:
            del doc['_id']
            docs.append(doc)
        self.client.close()    
        return docs   


    def day_summary(self, present=True, target=[None]):    
        if present:
            dateobject = datetime.date.today()
            d1 = datetime.datetime.combine(dateobject, datetime.time.min)
            match = {"$match" : {"Date" : d1}}  
        else:
            if (len(target) == 1):
                d1 = target[0]
                match = {"$match" : {"Date" : d1}}  
                
            else:
                d1 = target[0]
                d2 = target[1]
                match = {"$match" : {"$and" : [{"Date" : { "$gte":d1, "$lte": d2}}]}}       
                 
        group = {
            "$group" : {'_id': {
                    "Host": "$Host",
                    "Device": "$Device",
                    "Date": "$Date"
                    },               
                    'Avg Temp': {'$avg':'$CPU Core'},
                    'Avg Freq': {'$avg':'$CPU Clock'},
                    'Obs': {'$sum': 1},
                    'Humidity' : {'$avg': '$Room Humidity'},
                    'Pressure' : {'$avg': '$Room Pressure'},
                    'Ox Gas' : {'$avg': '$Oxidising Gas'},
                    'Red Gas'  : {'$avg': '$Reducing Gas'},
                    'nh3 Gas' : {'$avg' : '$nh3 Gas'}
                   }    
        } 
        
        proj = {
           "$project": {
              "Date" : { 
                 "$dateFromString" : 
                  {
                    "dateString": '$Date',
                    "timezone": 'Europe/Dublin'
                  }
                },
               "Host":1,
               "Device":1,
               "CPU Core":1,
               "Room Pressure":1,
               "Room Pressure":1,
               "Oxidising Gas":1,
               "Reducing Gas":1,
               "nh3 Gas":1,
               "CPU Clock":1
           }
        }      
            
        pipeline = [
            match,
            group
        ]
    
        agg_sum = self.db.readings.aggregate(pipeline)   
        docs = []
        for b in agg_sum:
            rec = {}
            rec['Host'] = b['_id']['Host']
            rec['Device'] = b['_id']['Device']
            rec['Date'] = b['_id']['Date']
            
            del b['_id'] 
            for key in b.keys():
                if (type(b[key]) == str):
                    rec[key] = b[key]
                else:
                    try:
                        amt = b[key]
                        rec[key] = round(amt,2)
                    except:
                        continue
                    
                
                
            docs.append(rec)   
        self.client.close()
        return docs