#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from moviepy.editor import VideoFileClip, concatenate_videoclips
import glob
import os
from datetime import date
import time
today = str(date.today())
import datetime
now = str(datetime.datetime.now())
now = now.replace(' ','_').replace(':','_')
import redis
r = redis.Redis()
import pickle

def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == 'KB':
       return size_in_bytes/1024
   elif unit == 'MB':
       return size_in_bytes/(1024*1024)
   elif unit == 'GB':
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes
  



libs = ["/home/pi/shared/Monitor2/",
        "/home/pi/shared/Monitor/",
        "/home/pi/shared/Monitor3/",
        "/home/pi/shared/Monitor4/",
        "/home/pi/shared/Monitor5/",
        "/home/pi/shared/Monitor6/",
        "/home/pi/shared/archives/"
        ]

files = [ ]

for f in libs:       
    with os.scandir(f) as dir_contents:
        for entry in dir_contents:
            rec = {}
            info = entry.stat()
            modificationTime = time.ctime ( info.st_mtime )
            rec['directory'] = str(f)
            rec['file'] = entry.name
            rec['timestamp'] = modificationTime
            rec['size'] = round(convert_unit(info.st_size,'MB'),2)
            files.append(rec)


r.set('messages', pickle.dumps(files))


