import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime

#set up GPIO into BCM as opposed to BOARD
GPIO.setmode(GPIO.BCM)

#set variables for GPIO pins on the Raspberry Pi to talk to the correct sensors
TempSensorType = 11
TempGPIOPin = 17
MoistureGPIOPin = 25
PumpRelayGPIOPin = 4
HeatingPad = 26

#setup the GPIO pins
GPIO.setup(MoistureGPIOPin,GPIO.IN)
GPIO.setup(PumpRelayGPIOPin,GPIO.OUT)
GPIO.setup(HeatingPad,GPIO.OUT)

#setup variables for temperature
#(note, we don't have to set a moisture threshhold, as the sensor is binary - the sensor returns 1 if it's too dry) 
minimumTemp = 75

#Greeting and settings readout
print "------------------------------------"
print "Welcome to Hot Peppers!"
print "GPIO version:  " + str(GPIO.VERSION)
print "temperature sensor type: DHT" + str(TempSensorType)
print "temperature GPIO Pin: " + str(TempGPIOPin)
print "Moisture GPIO Pin: " + str(MoistureGPIOPin)
print "Heating Pad Relay: " + str(HeatingPad)
print "Pump Relay" + str(PumpRelayGPIOPin)
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

def relayTest(pin):
	sleeptime =  0.1
	for i in range(1,20):
		print i
#		GPIO.cleanup()
#		GPIO.setmode(GPIO.BCM)

#total hack.  If I don't put this in here, for some reason the relays get 
#stuck / GPIO turns off
		GPIO.setup(PumpRelayGPIOPin,GPIO.OUT)
		GPIO.setup(HeatingPad,GPIO.OUT)

		GPIO.output(pin, GPIO.LOW)
		time.sleep(sleeptime)
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(sleeptime)

while (1==1):
	relayTest(PumpRelayGPIOPin)
	time.sleep(1)
	relayTest(HeatingPad)
	time.sleep(1)

print "entering main loop..."

#just do this forever
while (1==1):
	#read from the sensors
	print "reading temperature sensor"
	humidity, temperature = getTemperatureAndHumidity()
	print "reading the moisture sensor"
	moisture = getMoisture()

	#print out time and sensor data. TODO this is where we stick the sensor data into a local mySQL or CSV so we can make a nice chart over time
	print datetime.datetime.now()
	printTemperatureAndHumidity(humidity,temperature)
	printMoisture(moisture)

	#take action
	if temperature < minimumTemp:
    		print "activating heating pad"
		#activate HeatingPad
		GPIO.output(HeatingPad,LOW)
		time.sleep(60)
		GPIO.output(HeatingPad,HIGH)
	
	if moisture == 1:
		print "activating pump"
		#activate PumpRelay
		GPIO.output(PumpRelayGPIOPin,LOW)
		time.sleep(1)
		GPIO.output(PumpRelayGPIOPim,HIGH)

GPIO.cleanup()
