import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime

#set up GPIO into BCM as opposed to BOARD
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#used to inform the Adafruit lib of sensor type
TempSensorType = 11

#map GPIO pins to  sensors
TempSensor = 17
MoistureSensor = 25

#map GPIO pins to relays
PumpRelay = 4
HeatRelay = 26
FanRelay = 23

#setup the GPIO pins
GPIO.setup(TempSensor, GPIO.IN)
GPIO.setup(MoistureSensor,GPIO.IN)
GPIO.setup(PumpRelay,GPIO.OUT)
GPIO.setup(HeatRelay,GPIO.OUT)
GPIO.setup(FanRelay,GPIO.OUT)

#set relays to off
GPIO.output(HeatRelay,GPIO.HIGH)
GPIO.output(FanRelay,GPIO.HIGH)
GPIO.output(PumpRelay,GPIO.HIGH)

#setup variables for temperature
#(note, we don't have to set a moisture threshhold, as the sensor is binary - the sensor returns 1 if it's too dry) 
minTemp = 85
maxTemp = 95

#Greeting and settings readout
print "------------------------------------"
print "Welcome to Hot Peppers!"
print "GPIO version:  " + str(GPIO.VERSION)
print "GPIO setmode" + str(GPIO.setmode(GPIO.BCM))
print "GPIO RPI_INFO: " + str(GPIO.RPI_INFO)
print "temperature sensor type: DHT" + str(TempSensorType)
print "temperature GPIO Pin: " + str(TempSensor)
print "Moisture GPIO Pin: " + str(MoistureSensor)
print "Heating Pad Relay: " + str(HeatRelay)
print "Pump Relay" + str(PumpRelay)
print "Fan " + str(FanRelay)
print "------------------------------------"

def getTemperatureAndHumidity():
    	#reading and throwing away result.  Sometimes sensor gives bogus results on first read
	#this is apparently a known issue with the sensor according to interwebs.
	hum, temp= Adafruit_DHT.read_retry(TempSensorType, TempSensor)
	hum, temp = Adafruit_DHT.read_retry(TempSensorType, TempSensor)
	#convert C to F
	temp = temp * 9/5.0 + 32
	return hum, temp

def getMoisture():
	return GPIO.input(MoistureSensor)

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

def relayHack(pin, state):
# ABSOLUTE HACK. There is some sort of race condition in the GPIO that is a
# giant PITA.  Basically, if we are going to use this library, we have to make
# a workaround where we are making damn sure the relay is off - where off
# is set to HIGH.  As there is no error thrown by the library, we have to try
# a bunch of times to make sure.  It feels like a library or HW race condition.

	for n in range (1,10):
		GPIO.setup(pin,GPIO.OUT)
	for n in range (1,10):
		GPIO.output(pin,state)

#used for debugging GPIO problems
def testRelay(pin):
	sleeptime =  1
	for i in range(1,20):
		print i
		relayHack(pin,GPIO.LOW)
		time.sleep(sleeptime)
		relayHack(pin,GPIO.HIGH)
		time.sleep(sleeptime)

print "entering main loop..."
#just do this forever
while (1==1):
	#read from the sensors
	time.sleep(1)
	print "reading temperature sensor"
	humidity, temperature = getTemperatureAndHumidity()
	time.sleep(1)
	print "reading the moisture sensor"
	moisture = getMoisture()

	#print out time and sensor data. TODO this is where we stick the sensor data into a local mySQL or CSV so we can make a nice chart over time
	print datetime.datetime.now()
	printTemperatureAndHumidity(humidity,temperature)
	printMoisture(moisture)
	time.sleep(1)

	#take action
	if temperature < minTemp:
    		print "activating heating pad"
		#activate HeatingPad
		relayHack(HeatRelay,GPIO.LOW)
		time.sleep(10)
		relayHack(HeatRelay,GPIO.HIGH)

	if temperature > maxTemp:
    		print "activating fan"
		#activate Fan
		relayHack(FanRelay, GPIO.LOW)
		time.sleep(10)
		relayHack(FanRelay,GPIO.HIGH)

	if moisture == 1:
		print "activating pump"
		#activate PumpRelay
		relayHack(PumpRelay, GPIO.LOW)
		time.sleep(.3)
		relayHack(PumpRelay, GPIO.HIGH)
GPIO.cleanup()
