import sys
import Adafruit_DHT
import  RPi.GPIO as GPIO
import time
import datetime

#set up GPIO into BCM as opposed to BOARD
GPIO.setmode(GPIO.BCM)

#set variables for GPIO pins on the Raspberry Pi to talk to the correct sensors
TempSensorType = 11
TempGPIOPin = 17
MoistureGPIOPin = 25
PumpRelay = -1
HeatingPadRelay = -1

#setup the GPIO pins
GPIO.setup(MoistureGPIOPin,GPIO.IN)

#Greeting
print "------------------------------------"
print "Welcome to Hot Peppers!"
print "GPIO version:  " + str(GPIO.VERSION)
print "temperature sensor type: DHT" + str(TempSensorType)
print "temperature GPIO Pin: " + str(TempGPIOPin)
print "Moisture GPIO Pin: " + str(MoistureGPIOPin)
print "Heating Pad Relay: " + "Not implemented!"
print "Pump Relay" + "Not implemented!"
print "------------------------------------"

def getTemperatureAndHumidity():
    #reading and throwing away result.  Sometimes sensor gives bogus results on first read
	#this is apparently a known issue with the sensor according to interwebs.
	hum, temp= Adafruit_DHT.read_retry(TempSensorType, TempGPIOPin)
	hum, temp = Adafruit_DHT.read_retry(TempSensorType, TempGPIOPin)
	#convert C to F
	temp = temp * 9/5.0 + 32
	return hum, temp

def getMoisture():
	return GPIO.input(MoistureGPIOPin)

def printTemperatureAndHumidity(hum, temp):
	print "---------------------------------"
	print "TEMPERATURE"
	print "humidity: " + str(humidity)
	print "temperature: " + str(temperature)
	print "---------------------------------"
    	
def printMoisture(moist):
    print "---------------------------------"
	print "MOISTURE"
	print moist
	print "---------------------------------"

print "entering main loop..."

#just do this forever
while (1==1):
	#read the sensors
	print "reading temperature sensor"
	humidity, temperature = getTemperatureAndHumidity()

	print "reading the moisture sensor"
	moisture = getMoisture()

	#print out time and sensor data.
	#TODO this is where we stick the sensor data into a local mySQL or CSV so we can make a nice chart over time
	print datetime.datetime.now()
	printTemperatureAndHumidity()
	printMoisture()

	#take action
	#if temperature is too low, activate HeatingPadRelay
	#if moisture is too low, activate PumpRelay

	