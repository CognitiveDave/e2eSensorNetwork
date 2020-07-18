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
  

vids = (glob.glob("/home/pi/shared/Monitor2/*.mkv"))
vids2 = (glob.glob("/home/pi/shared/Monitor/*.mkv"))
vids3 = (glob.glob("/home/pi/shared/Monitor3/*.mkv"))
vids4 = (glob.glob("/home/pi/shared/Monitor4/*.mkv"))
vids5 = (glob.glob("/home/pi/shared/Monitor5/*.mkv"))
vids6 = (glob.glob("/home/pi/shared/Monitor6/*.mkv"))

vids  = sorted(vids,  reverse=False)
vids2 = sorted(vids2, reverse=False)
vids3 = sorted(vids3, reverse=False)
vids4 = sorted(vids4, reverse=False)
vids5 = sorted(vids5, reverse=False)
vids6 = sorted(vids6, reverse=False)

if ((len(vids) + len(vids2) + len(vids3) + len(vids4)) > 5):
    time.sleep(30)

    vid_list = []
    
    if (len(vids) > 3):
        for vid in vids[:-1]:
           try: 
            clip = VideoFileClip(vid)
            vid_list.append(clip)
           except:
            continue
        
    if (len(vids5) > 3):
        for vid in vids5[:-1]:
           try: 
            clip = VideoFileClip(vid)
            vid_list.append(clip)
           except:
            continue        
        
    if (len(vids6) > 3):
        for vid in vids6[:-1]:
           try: 
            clip = VideoFileClip(vid)
            vid_list.append(clip)
           except:
            continue
 
 
    if (len(vids2) > 3):
        for vid in vids2[:-1]:
           try: 
            clip = VideoFileClip(vid)
            vid_list.append(clip)
           except:
            continue  

    if (len(vids3) > 3):
        for vid in vids3[:-1]:
           try: 
            clip = VideoFileClip(vid)
            vid_list.append(clip)
           except:
            continue   

    if (len(vids4) > 3):
        for vid in vids4[:-1]:
           try: 
            clip = VideoFileClip(vid)
            vid_list.append(clip)
           except:
            continue         
   
    if (len(vid_list) > 0):
        full_vid = concatenate_videoclips(vid_list)
        out_file = f"/home/pi/shared/archives/{now}_con.mp4"
        full_vid.write_videofile(out_file)

        for vid in vids[:-1]:
            os.remove(vid)
    
        for vid in vids2[:-1]:
            os.remove(vid)
        
        for vid in vids3[:-1]:
            os.remove(vid)      
     
        for vid in vids4[:-1]:
            os.remove(vid)
            
        for vid in vids5[:-1]:
            os.remove(vid)

        for vid in vids6[:-1]:
            os.remove(vid)


else:
    print('nothing')        
   


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


