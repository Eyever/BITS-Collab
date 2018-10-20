#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import sys
import Adafruit_DHT

def main():
    # GPIO SETUP
    pin_SoilSensor = 40  # Soil Moisture sensor (physcial pin 40)
    pin_HumiditySensor = 25  # Temperature/Humidity sensor (channel 17, physical pin 11)
    humidity_sensor_type = 11  # DHT11 sensor model type
    pin_WaterPump = 11  #Water pump

    GPIO.setmode(GPIO.BOARD)  # GPIO.BCM can be used for channels, BOARD refers to actual physical pin number on pi
    GPIO.setup(pin_SoilSensor, GPIO.IN)
	
    GPIO.setup(pin_WaterPump, GPIO.OUT)
 

    def callback(pin_SoilSensor):
        water_volume = get_temperature_humidity()

        if GPIO.input(pin_SoilSensor):
            print('No water detected')
            activate_pump(water_volume)
        else:
            print('Water detected')
            deactivate_pump()
	
    #function polls and gets the readings from the DHT11 temperature/humidity sensor and calculates a heat stress index
    #value using the combination of both data. It will then calculate and return a water volume variable which
    #will be used to tell the pump how long to push water for to the plant at any one time.
    #The higher the index, the higher the water volume to send to the plant at any one time.
    #This will promote the water reaching the plant roots before absorbed from top of the soil in high heat conditions

    def get_temperature_humidity():
        humidity, temperature = Adafruit_DHT.read_retry(humidity_sensor_type, pin_HumiditySensor)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	        
            #print('calculating Heat Index from Temperature/Humidity readings')
	
            temperature = (1.8 * temperature) + 32 #convert to Fahrenheit for the purpsoe of calculating Heat Stress Index
	    #print('Temp in Fahrenheit: {}'.format(temperature))
	
	    #heat stress index formula: calculate heat stress index from temperature and humidity readings
            heat_index = (
            -42.379 + (2.04901523 * temperature) + (10.14333127 * humidity) - (0.22475541 * temperature * humidity) - \
            (6.83783e-3 * (temperature * temperature)) - (5.481717e-2 * (humidity * humidity)) + \
            (1.22874e-3 * (temperature * temperature) * humidity) + (8.5282e-4 * temperature * (humidity * humidity)) - \
            (1.99e-6 * (temperature * temperature) * (humidity * humidity)))
	
	    #heat_index = (heat_index-32) * 5 / 9 #convert from fahrenheit to degrees celcius
            heat_index = round(heat_index)
	
            print('Heat Index is: {}'.format(heat_index))
            if heat_index in range(0, 80): #rating: NORMAL
                water_volume = 1  #mild/normal absorption rate
            elif heat_index in range(80, 91):  # rating: CAUTION
                water_volume = 2  # normal absorption rate
            elif heat_index in range(91, 104):  # rating: EXTREME_CAUTION
                water_volume = 3  # high than normal absorption rate
            elif heat_index in range(104, 125):  # rating: DANGER
                water_volume = 4  # very high absorption rate
            elif heat_index in range(125, 138):  # rating: EXTREME_DANGER
                water_volume = 5  # extremly high absorption rate
            else:
                water_volume = 6  # rating: OFF_THE_CHARTS radically high absorption rate
	    
            return(water_volume)
        else:
            print('Failed to get temperature/humidity reading. Try again!')
            return(0)

    def activate_pump(water_volume):
        print('Turning Water Pump ON for {} seconds (keep watering until moisture detected)'.format(5*water_volume))
        time.sleep(1)
        GPIO.output(pin_WaterPump, GPIO.LOW)
        time.sleep(5 * water_volume)
        deactivate_pump()
        callback(pin_SoilSensor)
	
    def deactivate_pump():
        print('Turning water pump OFF (if not already)')
        GPIO.output(pin_WaterPump, GPIO.HIGH)
        time.sleep(1)
        callback(pin_SoilSensor)

    print('Starting Program')
    # Assigns a function to the GPIO pin so when a change on the state of the pin then run callback function
    #GPIO.add_event_detect(pin_SoilSensor, GPIO.BOTH, callback=callback, bouncetime=100)
    #below code is needed on startup to detect soil moisture or not as add_event_detect will not trigger until a state has changed
    #this is important if the plant is already saturated or dry to begin with
    try:
        current_state = GPIO.input(pin_SoilSensor)
        if current_state == 0 or current_state == 1:
            callback(pin_SoilSensor)
    
        # Assigns a function to the GPIO pin so when a change on the state of the pin then run callback function
        GPIO.add_event_detect(pin_SoilSensor, GPIO.BOTH, callback=callback, bouncetime=500)
    	
        # Infinte loop to keep our script running
        while(True):
            time.sleep(2)

    except:
        print('An error occurred. Check all sensor connections and restart program.')
        exit()
    finally:
        GPIO.cleanup()
	
main()