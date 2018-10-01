#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import datetime
import sys

#GPIO SETUP
pin_SoilSensor = 40 #Soil Moisture sensor

GPIO.setmode(GPIO.BOARD) #GPIO.BCM can be used for channels, BOARD refers to actual physical pin number on pi
GPIO.setup(pin_SoilSensor, GPIO.IN)

def callback_soil(pin_SoilSensor):
    if GPIO.input(pin_SoilSensor):
        print('No water detected')
    else:
        print('Water detected')

# Tells script to watch gpio pin and let us know when the pin goes both HIGH (Rising) or LOW (falling)
GPIO.add_event_detect(pin_SoilSensor, GPIO.BOTH, callback=callback_soil, bouncetime=1000)

# Infinte loop to keep our script running
while(True):
    try:
       time.sleep(2)
    except:
        GPIO.cleanup()
        print("ERR_RANGE")
        #exit(0)
