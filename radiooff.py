import RPi.GPIO as GPIO  ##  library that lets you control the Pi's GPIO pins
import os  ##  allows us to talk to the system like in the terminal
from sys import exit  ##  allows us to use "exit"
from time import sleep  ##  allows us to use "sleep"
import psutil ##  allows us to look at processes on the Pi
 
##  allows us to use the Initial State streamer
from ISStreamer.Streamer import Streamer  
 
##  designate bucket name and individual access_key
##  if the bucket name already exists in association with the bucket_key (optional), 
##    then the data will append to that bucket
##  if the bucket name does not already exist, then a new bucket will be created
##  the access_key tells Initial State which account to send the data to
streamer = Streamer(bucket_name="Shutdown", access_key="[Your Access Key Here]")  
 
GPIO.setwarnings(False)  ##  disables messages about GPIO pins already being in use
GPIO.setmode(GPIO.BOARD)  ##  indicates which pin numbering configuration to use
 
GPIO.setup(20, GPIO.IN)  ##  tells it that pin 16 (button) will be giving input
# GPIO.setup(7, GPIO.OUT)  ##  tells it that pin 7 (LED) will be outputting
# GPIO.output(7, GPIO.HIGH)  ##  sets pin 7 (LED) to "HIGH" or off
 
##  set counter's initial value to 0
counter = 0
 
## set found_ntpd's initial value to False
found_ntpd = False
 
##  set i's initial value to 0
i=0
 
##  set prev_input's initial value to 0
prev_input=0
 
##  this while loop looks to see if NTPD has been executed yet
while found_ntpd == False:
    ##  use psutil to iterate through a list of current processes
    for proc in psutil.process_iter():
        ##  only execute if "ntpd" is found
        if proc.name() == "ntpd":
            streamer.log("msg","Found NTPD") ##  stream alert that ntpd was found
            streamer.log("psutil_msg",proc.status()) ##  stream process status of ntpd; "stream name", value
            found_ntpd=True ##  change variable to True to exit this loop
        ##  assume that ntpd has already run if not found in 60 seconds
        elif counter>=60:
            streamer.log"msg","Search for NTPD timeout") ##  stream alert that 60 seconds passed before ntpd was found
            found_ntpd=True ##  change variable to True to exit this loop
        else:
            counter = counter + 1 ##  add to the counter to track time passed
            #streamer.log("counter",counter) ##  stream current counter value
    sleep(1) ##  wait for 1 second
 
##  this while loop constantly looks for button input (presses) once NTPD has run or 60 seconds have passed
while found_ntpd == True:
    streamer.log("msg","Ready for button input") ##  stream message
    ##  if no button press
    if (GPIO.input(16) == False and prev_input!=1):
            i=i+1  ##  iteration count increases by 1
            streamer.log("iteration",(i)) ##  stream current iteration
            GPIO.output(7,True) ##  switch on pin 7 (LED)
            sleep(0.5) ##  wait for 0.5 second
            GPIO.output(7,False) ##  switch off pin 7 (LED)
            sleep(1) ##  wait for 1 second
 
    ##  when button is pressed
    else:
            GPIO.output(7,GPIO.HIGH)  ##  turn pin 7 (LED) off
            ##  script to be called
            os.system("sudo shutdown -h now")  ##  shuts down Pi
            streamer.log("msg","Script has been called")
            ##  keeps script from executing the "if" section while button is unpressed 
            ##  after it has been pressed
            prev_input=1       
            streamer.close() ##  send any messages left in the streamer
            exit()  ##  terminates this script
