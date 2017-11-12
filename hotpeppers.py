import sys
import Adafruit_DHT
import  RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)


print "Welcome to Hot Peppers!"

print "GPIO version:  " + str(GPIO.VERSION)

TempSensorType = 11
TempGPIOPin = 17
MoistureGPIOPin = 25

GPIO.setup(MoistureGPIOPin,GPIO.IN)

print "temperature sensor type: " + str(TempSensorType)
print "temperature GPIO Pin: " + str(TempGPIOPin)
print "Moisture GPIO Pin: " + str(MoistureGPIOPin)

print "*enter main loop*"

while (1==1):
	print "reading temperature sensor"
	#reading and throwing away result.  Sometimes sensor gives bogus results on first read
	humidity, temperature = Adafruit_DHT.read_retry(TempSensorType, TempGPIOPin)
	humidity, temperature = Adafruit_DHT.read_retry(TempSensorType, TempGPIOPin)
	#convert C to F for US-ifying
	temperature = temperature * 9/5.0 + 32

	print datetime.datetime.now()

	print "---------------------------------"
	print "TEMPERATURE"
	print "humidity: " + str(humidity)
	print "temperature: " + str(temperature)
	print "---------------------------------"

	print "reading the moisture sensor"
	print "---------------------------------"
	print "MOISTURE"
	print GPIO.input(MoistureGPIOPin)
	print "---------------------------------"

