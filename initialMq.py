#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pika
import json
import time 
import logging
import logging.handlers
import os
 
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "/home/pi/Documents/projects/Sensors/sensors.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "WARNING"))
root.addHandler(handler)

import socket
import platform
import config as cf
from datetime import datetime
import numpy as np
from sense_hat import SenseHat
import math

factor = cf.config['Enviro_Factor']

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def read_env(ltr559, bme280, gas, cpu_temps):
    envodata = {}
    proximity = ltr559.get_proximity()
    unit = "C"
    cpu_temp = getCPUtemperature()
    # Smooth out with some averaging to decrease jitter
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    envodata['Room Temp'] = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    unit = "hPa"
    envodata['Room Pressure'] = bme280.get_pressure()
    envodata['Room Pressure Unit'] = unit
    unit = "%"
    data = bme280.get_humidity()
    envodata['Room Humidity'] = data
    envodata['Humidity unit'] = unit
    unit = "Lux"
    if proximity < 10:
        envodata['Light'] = ltr559.get_lux()
        envodata['Light unit'] = unit
    else:
        data = 1
    unit = "kO"
    data = gas.read_all()
    envodata['Oxidising Gas'] = data.oxidising / 1000
    envodata['Gas unit'] = unit
    # variable = "reduced"
    data = gas.read_all()
    envodata['Reducing Gas'] = data.reducing / 1000
    # variable = "nh3"
    data = gas.read_all()
    envodata['nh3 Gas'] = data.nh3 / 1000
    return envodata


def read_sense(sense):
 temp = round(sense.get_temperature_from_humidity(),2)
 temp_pressure = round(sense.get_temperature_from_pressure(),2)
 humidity = round(sense.get_humidity(),2)
 pressure = round(sense.get_pressure(),2)
 return (temp, temp_pressure, humidity, pressure)


def sense_display(temp, sense):
 temp = round(temp,0)   
 temp_color = (255, 255, 255)
 black = (0, 0, 0)

 number = [
    0, 0, 0, 0, # zero
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 0, 1,
    0, 1, 0, 1,
    0, 1, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 0,

    0, 0, 0, 0, # one
    0, 0, 1, 0,
    0, 1, 1, 0,
    0, 0, 1, 0,
    0, 0, 1, 0,
    0, 0, 1, 0,
    0, 1, 1, 1,
    0, 0, 0, 0,

    0, 0, 0, 0, # two
    0, 1, 1, 1,
    0, 0, 0, 1,
    0, 0, 1, 0,
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 1, 1, 1,
    0, 0, 0, 0,


    0, 0, 0, 0, # three
    0, 1, 1, 1,
    0, 0, 0, 1,
    0, 0, 1, 1,
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 0,

    0, 0, 0, 0, # four
    0, 0, 0, 1,
    0, 1, 0, 1,
    0, 1, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 0, 0, 0,

    0, 0, 0, 0, # five
    0, 1, 1, 1,
    0, 1, 0, 0,
    0, 1, 1, 1,
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 0,

    0, 0, 0, 0, # six
    0, 0, 0, 1,
    0, 0, 1, 0,
    0, 1, 0, 0,
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 0,


    0, 0, 0, 0, # seven
    0, 1, 1, 1,
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 0, 1, 0,
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,

    0, 0, 0, 0, # eight
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 0,

    0, 0, 0, 0, # nine
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 1, 1,
    0, 0, 0, 1,
    0, 0, 1, 0,
    0, 1, 0, 0,
    0, 0, 0, 0
    ]

 temp_image = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
    ]

 pixel_offset = 0
 index = 0

 for index_loop in range (0, 8):
    for counter_loop in range(0, 4):
        if (temp >= 10):
            temp_image[index] = number[int(temp/10)*32+pixel_offset]
        temp_image[index+4] = number[int(temp%10)*32+pixel_offset]
        pixel_offset = pixel_offset + 1
        index = index + 1
    index = index + 4

 for index in range(0, 64):
    if(temp_image[index]):
        temp_image[index] = temp_color
    else:
        temp_image[index] = black

 sense.set_pixels(temp_image)
 return 0




def getCPUtemperature() :
    res=os.popen("vcgencmd measure_temp").readline()
    return (round(float(res.replace("temp=","").replace("'","").replace("C\n","")),2))

def throttling():
    res=os.popen("vcgencmd get_throttled").readline()
    res = res.split("=")[1]
    scale = 16 ## equals to hexadecimal
    num_of_bits = 8
    decim = bin(int(res, scale))[2:].zfill(num_of_bits)
    return decim
    
def getCPUclock ( ) :
    res=os.popen("vcgencmd measure_clock arm").readline()
    res = res.replace("frequency(48)=","").replace("\n","")
    return (round((float (res) / 1000000 ) , 2 ) )

def getCPUvolts ( ) :
    res=os.popen("vcgencmd measure_volts core").readline()
    return (res.replace ("volt=","").replace("V\n",""))

def getfree_mem() :
    res=os.popen("vcgencmd get_mem arm").readline()
    return (res.replace("arm=", "" ).replace("M\n",""))

def getfree_memGPU ( ) :
    res=os.popen("vcgencmd get_mem gpu").readline()
    return (res.replace ("gpu=","").replace("M\n",""))



def main():
    cpu_temps = []
    cpu_temps.append(getCPUtemperature())
    credentials = pika.PlainCredentials()
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.1', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    if socket.gethostname().find('.')>=0:
        name=socket.gethostname()
    else:
        name=socket.gethostbyaddr(socket.gethostname())[0]

    if (cf.config['Type'] == 'Sense'):
        print('sense')
        sense = SenseHat()
        sense.clear()

    if (cf.config['Type'] == 'Enviro'):
        try:
            # Transitional fix for breaking change in LTR559
            from ltr559 import LTR559
            ltr559 = LTR559()
        except ImportError:
            import ltr559

        from bme280 import BME280
        from enviroplus import gas
        from subprocess import PIPE, Popen

        # BME280 temperature/pressure/humidity sensor
        bme280 = BME280()

    while True:

        data= {
        "CPU Core": getCPUtemperature(),
        "CPU Clock": getCPUclock(),
        "CPU Volts": getCPUvolts(),
        "Core Mem": getfree_mem(),
        "GPU Mem": getfree_memGPU(),
        "Date":  time.strftime("%d/%m/%Y"),
        "Time":  time.strftime("%H:%M"),
        "Host": name,
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Throttling": throttling(),
        "Device": cf.config['Type']
        }

        if (cf.config['Type'] == 'Sense'):
            senseHat = read_sense(sense)
            sense_display(senseHat[0], sense)
            data['Room Temp'] = senseHat[0]
            data['Room Temp Pressure'] = senseHat[1]
            data['Room Humidity'] = senseHat[2]
            data['Room Pressure'] =senseHat[3]


        elif (cf.config['Type']) == 'Enviro':
            print('enviro')
            enviro = read_env(ltr559, bme280, gas,cpu_temps)
            data = merge_two_dicts(data, enviro)

        else:
            print('controller')
                


        message = json.dumps(data)

        channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

        print(f" [x] Sent { message }")
        time.sleep(1200)
    
    connection.close()
    return 0



if __name__ == "__main__":
    time.sleep(120)
    main()  


