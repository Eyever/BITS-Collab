#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import datetime
import sys

#GPIO SETUP
channel = 21 #Soil Moisture sensor - equivalent to PIN 40

GPIO.setmode(GPIO.BCM) #GPIO.BCM can be used for channels, BOARD refers to actual physical pin number on pi
GPIO.setup(channel, GPIO.IN)

def callback_soil(channel):
    if GPIO.input(channel):
        print('No water detected')
    else:
        print('Water detected')

# Tells script to watch gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, callback=callback_soil, bouncetime=1000)

# Infinte loop to keep our script running
while(True):
    try:
        time.sleep(5)
    except:
        print("ERR_RANGE")
        #exit(0)