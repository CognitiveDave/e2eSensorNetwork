import redis
r = redis.Redis()
from datetime import date
today = str(date.today())
import datetime
import pickle
existed = False

stand = [460, 1.3, .7]

def gas_lvl(gas):
    status = 'normal'
    gas = gas.replace(' ','')
    gases = gas.split('|')
    ox = float(gases[0])
    red = float(gases[1])
    nh = float(gases[2])
    
    ox_diff = (abs(ox-stand[0]) / stand[0] ) * 100
    red_diff = (abs(red-stand[1]) / stand[1] ) * 100
    nh_diff = (abs(nh-stand[2]) / stand[2] ) * 100
    
    if (ox_diff > 30 or red_diff > 30 or nh_diff > 30):
        status = 'abnormal'   
    
    return status
     
    


class RedisHelper:

    def __init__(self):
        self.r = redis.Redis()
        self.existed = False
        self.dev_key = 'devices'
    
    def read(self, span=1800):
        
        current = {
          "temp": -1,
          "humidity" : -1,
          "gas" : "abs",
          "alerts" : -2,
          "messages" : -3
        }
        
        msg, msgC = self.messages()
        
        currentTime = datetime.datetime.now()
        day = currentTime.strftime("%d/%m/%Y")
        
        key = day
        #print(key)

        if (self.r.exists(key)):
            persisted = pickle.loads(self.r.get(key))
            self.existed = True
            self.dev_key = 'devices'
            #print(persisted)
            
        else:
            persisted = {}


        timeHM = datetime.datetime.now()
        temp = 0
        humidity = 0
        pressure = 0
        count = 0

        for keys in persisted:
            date_time_obj = datetime.datetime.strptime(keys, '%d/%m/%Y@%H:%M:%S')
            diff = timeHM - date_time_obj
        
            #print(diff.seconds, span)
            if (diff.seconds <= span) :
                count = count + 1
                temp = temp + persisted[keys]['temp']
                humidity = humidity + persisted[keys]['humidity']
                pressure = pressure + persisted[keys]['pressure']
                #print(keys, persisted[keys], diff)
    
        if (count > 0):
            #print(f"averages are {temp/count} {humidity/count} {pressure/count} {count} ")
            last = list(persisted.keys())
            last_one = len(last) - 1
            gases = persisted[last[last_one]]['gas']
            if (gas_lvl(gases) != 'normal'):
                alert_message = 'Alert!'
            else:
                alert_message = 'Normal'
            
            current = {
              "temp": round(temp/count,2),
              "humidity" : round(humidity/count,2),
              "pressure" : round(pressure/count,2),
              "gas" : gas_lvl(gases),
              "alerts" : alert_message,
              "messages" : msgC,
              "count" : count
          }           
            
 
        return current
    
    
    def devices_read(self):  
        if (r.exists(self.dev_key)):
            devices = pickle.loads(self.r.get(self.dev_key))
        else:
            devices = {}
       
        docs = []
        for dev in devices:
            docs.append(devices[dev])       

        return docs       
                
                
    def devices_update(self, dev):          
        devices = self.devices_read()
        devices.pop(dev, None)
        r.set(self.dev_key, pickle.dumps(devices))            
        return devices
            
    def messages(self):
        if (r.exists('messages')):
            messages = pickle.loads(self.r.get('messages'))
        else:
            messages = {}    

        return messages, len(messages)       
       
    


            