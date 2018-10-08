#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import sys

#GPIO SETUP
pin_WaterPump = 7

GPIO.setmode(GPIO.BOARD) #GPIO.BCM can be used for channels, BOARD refers to actual physical pin number on pi
GPIO.setup(pin_WaterPump, GPIO.OUT)

# Infinte loop to keep our script running
print('Starting Program')
while(True):
    print('Turn pump on for 5 seconds')
    GPIO.output(pin_WaterPump, GPIO.HIGH)
    time.sleep(5)
    print('Turn pump off for 5 seconds')
    GPIO.output(pin_WaterPump, GPIO.LOW)
    time.sleep(5)