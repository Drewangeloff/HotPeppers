import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime

#set up GPIO into BCM as opposed to BOARD
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#map GPIO pins to relays
PumpRelay = 4
GPIO.setup(PumpRelay,GPIO.OUT)
GPIO.output(PumpRelay,GPIO.LOW)

for i in range(1,100):
	print i
	GPIO.setup(PumpRelay,GPIO.OUT)
	GPIO.output(PumpRelay,GPIO.LOW)
	time.sleep(.2)
	GPIO.output(PumpRelay,GPIO.HIGH)
	time.sleep(.2)

GPIO.cleanup()
