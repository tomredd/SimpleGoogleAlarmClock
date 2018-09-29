#!/usr/bin/env python

    #Note that this is written for python 2.7, not python3.

    #Written by reddit.com/u/neihuffda- https://www.reddit.com/r/raspberry_pi/comments/6ioxc8/button_press_and_long_button_press_question/

import time
import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)

#BCM
btn1 = 26 #Use this variable to set which GPIO your button is connected to. Note that this is BCM, not physical pin positon. Here, '17' refers to GPIO_17, not pin 17.

GPIO.setup(btn1, GPIO.IN) 

def command(cmd):
  #Here you set the "name" of the commands you want to execute from Bash. The syntax should be quite clear.
      commands = {"shutdown":"sudo shutdown -h now",
              "RadioStop"  :"sudo service radiod stop",
              "RadioStart"   :"sudo service radiod start"}

  subprocess.call(commands[cmd], shell=True)

def buttonPress():
  btn1_input = GPIO.input(btn1)
  return btn1_input

def button_callback(channel):
    start = time.time()
    stop = 0
    while buttonPress() == False:
      time.sleep(0.2)
      stop = time.time()
    else:
      pass

    if stop == 0:
      pass
    else:
      duration = (stop - start)
      #Uncomment the 'command()' sections to actually execute. Here you see that the "names" correspond with the dictionary above
      if duration < 1: #all durations can be edited to your liking - just make sure they don't overlap
        print "short press"
        command("RadioStart")
      elif duration > 2 and duration < 4:
        print "medium press with hold"
        command("RadioStop")
      elif duration > 4:
        print "long press with hold"
        command("shutdown")

#Here's the interrupt that does the magic
GPIO.add_event_detect(btn1, GPIO.FALLING, callback=button_callback, bouncetime=100)

try:
    #just to have something to do
    while True:
        time.sleep(60)
        pass
except KeyboardInterrupt:
  GPIO.cleanup()