#!/usr/bin/env python3

#imports

import sys

sys.path.append('./SDL_Pi_HDC1080_Python3')

import time
import SDL_Pi_HDC1080

import requests
import json


BLYNK_URL = 'http://blynk-cloud.com/
BLYNK_AUTH = '5ItGnhpRa_-AisxHvLABeHntgCItRKL9

# Main Program
print
print("")

print ("Read Temperature and Humidity from HDC1080 using 12C bus and send
   to Blynk")
print ("")
       
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

def blynkUpdate(temperature, humidity):
    print ("Updating Blynk")
    
    try:
      
        put_header=["Content-Type": "application/json"}
        val = temperature
        put_body = json. dumps(["(0:0.1f)". format(val)])
        r = requests.put(BLYNK_URL+BLYNK_AUTH+'/update/V0', data=put_body,
   headers-put_header)
                    
                    
                    
        put_header=["Content-Type": "application/json"}
        val = humidity
        put_body = json dumps(["{0:0.1f}".format(val)])
        r = requests.put(BLYNK_URL +BLYNK_AUTH+'/update/V1', data=put_body,
   headers=put_header)
                    
                    
                    
        put_header=["Content-Type": "application/json"}
        val = time.strftime("%Y-%m-%d %H:%M:%S")
        put_body = json dumps( [val])
        r = requests.put(BLYNK_URL #BLYNK_AUTH+'/update/V2', data=put_body,
   headers-put_header)
                    
        return 1
                    
    except Exception as e:
                print ("exception in updateBlynk")
                print (e)
                return 0
                    
while True:
                    
       temperature = hdc1080.readTemperature()
       humidity = hdc1080.readHumidity
                    
       print ("---------------------")
       print ("Temperature = %3.15 C" % hd 1080 readTemperature())
