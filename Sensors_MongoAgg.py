#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymongo import MongoClient
import os
import json
from bson.json_util import dumps
import datetime


dbuser = ""
_id = ""
dbpassword = ""

uri = f"mongodb://{dbuser}:{dbpassword}@ds043972.mlab.com:43972/{_id}"
    
stable = {
    'Oxidising Gas': 400,
    'Reducing Gas': 3.0,
    'nh3 Gas': 3.0
}
     


# In[2]:


client = MongoClient(uri, retryWrites=False)
db = client[_id]


# In[3]:


cursor = db.readings.find({})
docs = []
for document in cursor:
    docs.append(document)


# In[ ]:


import pandas as pd
df = pd.DataFrame(docs)
df['Volts'] = df['CPU Volts'].astype(float)
format = '%d/%m/%Y %H:%M'
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format=format)
df = df.set_index(pd.DatetimeIndex(df['Datetime']))


# In[ ]:


x = df['2020-06-29 18:00:00' : '2020-06-30 23:59:59' ] 


# In[ ]:


x[x['Device']=='Enviro']['Reducing Gas'].plot()


# In[71]:


from datetime import date
today = date.today()


def day_summary(present=True, target=[None]):    
    if present:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y") 
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

    agg_sum = db.readings.aggregate(pipeline)   
    docs = []
    for b in agg_sum:
        rec = {}
        rec['Host'] = b['_id']['Host']
        rec['Device'] = b['_id']['Device']
        rec['Date'] = b['_id']['Date']
        del b['_id'] 
        for key in b.keys():
            rec[key] = b[key]        
        docs.append(rec)   
    
    return docs
    
    


# In[72]:


d = day_summary(False, ['26/06/2020', '30/06/2020'])


# In[73]:


d


# In[75]:


import pandas as pd
ff = pd.DataFrame(d)


# In[76]:


ff


# In[77]:


ff['Date'].unique()


# In[ ]:




