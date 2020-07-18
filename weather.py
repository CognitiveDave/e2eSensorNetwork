#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 17:29:43 2020

@author: david
"""

from pyowm import OWM

class Weather:

    def __init__(self):
        self.owm = OWM() 
        self.mgr = self.owm.weather_manager()
        self.coords = ()


    def get_weather(self):

      observation_list = self.mgr.weather_around_coords(self.coords[0], self.coords[1])

      weath = []
        
      try:

        for obs in observation_list:
            rec = {}
            w = obs
            temps = w.weather.temperature('celsius')
            d = obs.to_dict()
            place = d['location']['name']
            wind = w.weather.wind()
            det_status = w.weather.detailed_status
            rain = w.weather.rain
            pressure = w.weather.pressure['press']
            snow = w.weather.snow
            srise = w.weather.srise_time
            sset = w.weather.sset_time
            humidity = w.weather.humidity
            as_of = w.reception_time('iso')
            ref_t = w.weather.reference_time('iso')
            
            rec['temps'] = temps
            rec['place'] = place
            rec['wind'] = wind
            rec['det_status'] = det_status
            rec['rain'] = rain
            rec['pressure'] = pressure
            rec['snow'] = snow
            rec['sun up'] = srise
            rec['Sun down'] = sset
            rec['humidity'] = humidity
            rec['received'] = as_of
            rec['Ref Time'] = ref_t
            weath.append(rec)
      except:
          weath = []  
    
    
        
      return weath
    