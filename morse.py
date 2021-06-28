#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from code import *
pinNum = 26
GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board and pin layout
GPIO.setup(pinNum,GPIO.OUT) #replace pinNum with whatever pin you used, this sets up that pin as an output
#set LED to flash forever
#while True:
#  GPIO.output(pinNum,GPIO.HIGH)
#  time.sleep(0.5)
#  GPIO.output(pinNum,GPIO.LOW)
#  time.sleep(0.5)


antwoord=raw_input('Wat wil je in morse seinen?')
for letter in antwoord:
	morse=(CODE[letter.upper()])
	for teken in morse:
		if teken=='.':
			GPIO.output(pinNum,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(pinNum,GPIO.LOW)
			time.sleep(0.2)
		elif  teken=="-":
			GPIO.output(pinNum,GPIO.HIGH)
			time.sleep(0.6)
			GPIO.output(pinNum,GPIO.LOW)
			time.sleep(0.2)

	time.sleep(1)
			


GPIO.cleanup()

