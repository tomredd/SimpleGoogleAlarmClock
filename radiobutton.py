#!/bin/python 
# Simple script for shutting down the raspberry Pi at the press of a button. 
# by Inderpreet Singh 
import RPi.GPIO as GPIO  
import time  
import os  
# Use the Broadcom SOC Pin numbers 
# Setup the Pin with Internal pullups enabled and PIN in reading mode. 
GPIO.setmode(GPIO.BCM)  
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# Our function on what to do when the button is pressed 
def RadioOn(channel):  
   os.system("sudo service radiod start")  
def RadioOff(channel):
   os.system("sudo service radiod stop")
# Add our function to execute when the button pressed event happens 
GPIO.add_event_detect(12, GPIO.FALLING, callback = RadioOn, bouncetime = 2000)  
GPIO.add_event_detect(16, GPIO.FALLING, callback = RadioOff, bouncetime = 2000) 
# Now wait! 
while 1:  
   time.sleep(1) 
