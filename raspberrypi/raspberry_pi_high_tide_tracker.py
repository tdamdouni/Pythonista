from __future__ import print_function
#
# Southend-on-Sea high tide display project by @AverageManVsPi
# Blog of this project at http://www.averagemanvsraspberrypi.com/2015/12/raspberry-pi-high-tide-tracker.html
# Code used from RasPi.TV 7-Seg tutorial and Kickstarter tracker tutorial (and kind of merged together and changed)
# 

import RPi.GPIO as GPIO
import time
import subprocess
import os
from urllib2 import Request, urlopen, URLError

# SET GPIO MODE
GPIO.setmode(GPIO.BCM)
 
# GPIO PORTS FOR THE 7SEG PINS (I think the order is important, in case you change these)
segments =  (17,9,13,5,11,27,19,6) # ALL HAVE RESISTORS
 
# SET THE SEGMNENT DISPLAY GPIO PORTS TO OUTPUTS
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0) # SET ALL SEGMENTS TO LOW
 
# GPIO PORTS FOR THE DIGIT 0-3 PINS 
digits = (3,22,10,26) # NO RESISTORS

# SET THE DIGIT PINS TO OUTPUTS 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1) # SET ALL SEGMENTS TO HIGH
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
    
try:

    #======================================================================
    # MAIN
    
    def mainprog():
  
        timelastchecked = 0

        errsquare() # Show a square on the display so that we know it has started the program properly
        time.sleep(2) # Wait 2 seconds
        
        while True:
            if time.time() >= timelastchecked: #If the current time is greater than or equal to the 'timelastchecked' string
                
                print("-------- UPDATING TIDE TIME --------")
                someurl= 'https://www.tidetimes.org.uk/southend-on-sea-tide-times' # Set the URL for the Pi to look in to
                req = Request(someurl) # Request the URL
				
                try:
                    response = urlopen(req) # Open the URL
                    print("Trying URL...")
                    
                except URLError as e: # This section is for error handling if WiFi is down etc
                
                    if hasattr(e, 'reason'): # One reason (unsure what!)
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                        
                        errsquare() # Show a square on the display to indicate an issue
                        time.sleep(900) # Wait 15 minutes before trying again so as not to over do the url requests
                        
                    elif hasattr(e, 'code'): # Another reason (unsure what!)
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                        
                        errsquare() # Show a square on the display to indicate an issue
                        time.sleep(900) # Wait 15 minutes before trying again so as not to over do the url requests
                        
                else:
                    print("URL open success!")
                    nexthightide = response.readlines() #read the lines of the URL (web page source) and turn that into 'nexthightide'
                    time.sleep(1) # Wait a second
                    
                    for line in nexthightide: # For statement
                    
                        if 'nxhi' in line: # If the Pi finds 'nxhi' in the line...
                            line = line[0:37] # Chop 37 characters from the back of the line
                            print("Starting line string is: ", line)
                            nhtpt1 = line[31:-4] # Take that line and cut away 31 characters from the front and 4 from the rear
                            nhtpt2 = line[34:-1] # Take that line and cut away 34 characters from the front and 1 from the rear
                            nexthightide = nhtpt1 + nhtpt2 # add those two cut strings together to make a 4-digit string
                            print("First segment of time: ",nhtpt1)
                            print("Second segment of time: ",nhtpt2)
                            print("Time string: ", nexthightide)
                            timelastchecked = time.time()+3600 # wait 1 hour until next url check

            else:
                for digit in range(4):
                    for loop in range(0,7):
                        GPIO.output(segments[loop], num[nexthightide[digit]][loop])
                    GPIO.output(digits[digit], 0)
                    time.sleep(0.001)
                    GPIO.output(digits[digit], 1)
                
    def errsquare():
        # Set digits to low to activate digit
        GPIO.output(3, 0)
        GPIO.output(22, 0)
        GPIO.output(10, 0)
        GPIO.output(26, 0)
        
        # Set segment high to activate segment
        GPIO.output(17, 1)
        GPIO.output(5, 1)
        
    #Run main program:
    mainprog()
    
#======================================================================
# EXCEPT BLOCK
# This will run if there is an error or we choose to exit the program

except KeyboardInterrupt: # USE THIS OPTION FOR DEBUGGING

    print("EXIT SCRIPT")
    time.sleep(0.5)
    
    # Clean up GPIOs
    print("PERFORMING GPIO CLEANUP")
    time.sleep(0.5)
    GPIO.cleanup() # Clean up the gpio pins ready for the next project.
    
    # Exit program
    print("--- EXIT NOW ---")
    time.sleep(0.5)
    quit()