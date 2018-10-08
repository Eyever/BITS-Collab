#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import sys
#import Adafruit_DHT

#GPIO SETUP
pin_SoilSensor = 40 #Soil Moisture sensor

GPIO.setmode(GPIO.BOARD) #GPIO.BCM can be used for channels, BOARD refers to actual physical pin number on pi
GPIO.setup(pin_SoilSensor, GPIO.IN)

def callback(pin_SoilSensor):

    if GPIO.input(pin_SoilSensor):
        print('No water detected')
        print('Turning Water pump ON')
    else:
        print('Water detected - Turning water pump OFF')

GPIO.add_event_detect(pin_SoilSensor, GPIO.BOTH, callback=callback, bouncetime=300)
print('Starting Program')

# Infinte loop to keep our script running
while(True):    
    time.sleep(1)