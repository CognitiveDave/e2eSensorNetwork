#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
import json
from dbClass import DBHelper
db = DBHelper()
import logging
import logging.handlers
import os
import time
import redis
r = redis.Redis()
from datetime import date
from datetime import datetime
import time
today = str(date.today())
import pickle
currentTime = datetime.now()
day = currentTime.strftime("%d/%m/%Y")
from datetime import timedelta
existed = False
time.sleep(2)

device_keys = ["CPU Core","CPU Clock","CPU Volts","Core Mem","GPU Mem", "Date", "Time", "Host", "System", "Release", "Version", "Throttling", "Device"]

 
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "/home/pi/Documents/projects/Sensors/sensors.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "WARNING"))
root.addHandler(handler)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def repair(dic):
    repair_dic = {}
    fields = ['CPU Core', 'CPU Clock', 'CPU Volts', 'Core Mem', 'GPU Mem', 'Date', 'Time', 'Host', 'System', 'Release', 'Version', 'Throttling', 'Device', 'Room Temp', 'Room Pressure', 'Room Pressure Unit', 'Room Humidity', 'Humidity unit', 'Light', 'Light unit', 'Oxidising Gas', 'Gas unit', 'Reducing Gas', 'nh3 Gas']
    types = ['float', 'float', 'float', 'float', 'float', 'date', 'time', 'str', 'str', 'str', 'str', 'str', 'str', 'float', 'float', 'str', 'float', 'str', 'float', 'str', 'float', 'str', 'float', 'float']
    for field, form in zip(fields,types):
        try:
            if (form == 'float'):
                repair_dic[field] = round(float(dic[field]),2)
            if (form == 'str'):
                repair_dic[field] = str(dic[field])
            if ( form == 'date'):
                date_time_obj = datetime.strptime(dic[field], '%d/%m/%Y')
                repair_dic[field] = date_time_obj
            if ( form == 'time'):
                date_time_obj = datetime.strptime(dic[field], '%H:%M')
                repair_dic[field] = date_time_obj           
          
        except:
              continue          
            
    return repair_dic


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    data = repair(json.loads(body.decode('utf-8')))
    currentTime = datetime.now()
    day = currentTime.strftime("%d/%m/%Y")
    #print(data, type(data))
    db.add(data)
    print(data)
    key = day
    dev_key = 'devices'
    readings = {}
    
    if (r.exists(dev_key)):
        devices = pickle.loads(r.get(dev_key))
    else:
        devices = {}       
      
    device = data['Device']
    host = data['Host']
    
    dev_record = {}
    for keyed in device_keys:
        dev_record[keyed] = data[keyed]
    
    devices[host] = dev_record
    
    r.set(dev_key, pickle.dumps(devices))
    print(dev_record)
        
    
    if (device == 'Enviro' or device == 'Sense'):
        readings['temp'] = data['Room Temp']
        readings['humidity'] = data['Room Humidity']
        readings['gas'] = str(data['Oxidising Gas']) + '| ' + str(data['Reducing Gas']) + ' | ' + str(data['nh3 Gas'])                                                          
        readings['pressure'] = data['Room Pressure']
        if (r.exists(key)):
            persisted = pickle.loads(r.get(key))
            existed = True
            #print(persisted)
            #print(key)
        else:
            persisted = {}
            existed = False
    
        currentTime = datetime.now()
        day = currentTime.strftime("%d/%m/%Y")
        timeHM = currentTime.strftime("%H:%M:%S")

        #persisted = r.hgetall(key)
        persisted[str(day) +'@' + str(timeHM)] = readings
        r.set(key, pickle.dumps(persisted))
        if (existed == False):
            r.expire(key, timedelta(hours=24))   
        


channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()