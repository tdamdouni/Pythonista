#
#############################################################################################################
## PiTFT Social Media Monitor by @AverageManVsPi http://AverageManVsRaspberryPi.com                        ##
##                                                                                                         ##
## --> Original basic PyGame example: http://home.uktechreviews.com                                        ##
## --? Urllib2 tutorial: (Kickstarter tracker: http://raspi.tv/                                            ##
##                                                                                                         ##
## This project uses PyGame on the Adafruit PiTFT (original model) to make a social media monitor          ##
## The monitor checks my Twitter, Facebook, Google+ and Pinterest follower counts every 45 seconds           ##
##                                                                                                         ##
## To find out more on the various blocks of code that make this happen, go to AverageManVsRaspberryPi.com ##
##                                                                                                         ##
## DISCLAIMER: I no expert. Not even close.                                                                ##
## This code is probably poor for many reasons including my commenting style -  but it works!              ##
##                                                                                                         ##
#############################################################################################################

###########
# IMPORTS #
###########

import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
from urllib2 import Request, urlopen, URLError

#######################################################################
# SET UP THE PITFT TO WORK WITH PYGAME                                #
#                                                                     #
# This part is necessary to make PyGame work with the PiTFT (I think) #
#                                                                     #
#######################################################################

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

###########################################################
# INITIALIZE THE PYGAME FONT MODULE                       #
#                                                         #
# Supposedly nothing will work if you don't do this part! #
#                                                         #
###########################################################

pygame.init()

######################################################
# SET THE GLOBAL FONT                                #
#                                                    #
# This can be overridden for individual items/labels #
#                                                    #
######################################################

font=pygame.font.Font(None,24)

###############################################################################################
# DEFINE WHAT HAPPENS WHEN YOU CLICK CERTAIN AREAS OF THE SCREEN                              #
#                                                                                             #
# This will commonly be used for making simple buttons on screen. I've used this to exit.     #
#                                                                                             #
# As an example, look at the code below:                                                      #
#                                                                                             #
# if 15 <= click_pos[0] <= 125 and 15 <= click_pos[1] <=50:                                   #
#                                                                                             #
# This creates a rectangle clicking shape (not visible) by using X (across) and Y (down) axis #
# It's always starting from the top-left corner                                               #
# Consider the "and" as the splitter between X and Y                                          #
# It's making the X axis line from 15 across to 125 across                                    #
# Then making the Y axis line from 15 down to 50 down                                         #
# This gives you two lines making a right-angle, which is our rectangle                       #
# (PyGame makes a rectangle out of this - we don't need to add the other two lines            #
#                                                                                             #
###############################################################################################

def on_click():
	click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])

	# Check to see if screen has been pressed
	if 1 <= click_pos[0] <= 320 and 1 <= click_pos[1] <=240: #This uses the entire screen i.e.e click anywhere to exit
		print "You pressed exit" # Print a message to Terminal for our information
		button(0) # Run the 'button' module (0)

######################################
# DEFINE THE BUTTON PRESSING ACTIONS #
######################################

def button(number):
	print "User requested to close GUI" # Prints a message to the screen telling us we selected to exit
	if number == 0: # button(0) - see 'def on_click()' above

	    # There are 3 Parts to this on-screen message, simply to emulate moving dots on the exit message

		# Part 1
		screen.fill(black) #Fill the screen with my pre-defined colour
		font=pygame.font.Font(None,40) # Font size
        	label=font.render("Closing system.", 1, (white)) # define exit message and colour
        	screen.blit(label,(55,110)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
		time.sleep(0.3) # Wait less than a second then continue

	    # Part 2
		screen.fill(black)
		font=pygame.font.Font(None,40)
        	label=font.render("Closing system..", 1, (white))
        	screen.blit(label,(55,110))
		time.sleep(0.3)

	    # Part 3
		screen.fill(black)
		font=pygame.font.Font(None,40)
        	label=font.render("Closing system...", 1, (white))
        	screen.blit(label,(55,110))
		
		# Exit the script (back to terminal)
		sys.exit() 

#############################################################
# DEFINE RGB COLOURS TO BE USED IN THIS SCRIPT              #
#                                                           #
# I have added some colours for you                         #
# For more, go to http://www.color-hex.com/color-names.html #
#                                                           #
#############################################################

white = 255, 255, 255
black = 0, 0, 0
grey = 238, 238, 238
gold = 255, 215, 0
red = 255, 0, 0

#######################
# SET THE SCREEN SIZE #
#######################

size = width, height = 320, 240 # Set the PiTFT screen size (320x240)

##################################################
# CREATE THE DISPLAY SURFACE AT THE SIZE DEFINED #
##################################################

screen = pygame.display.set_mode(size) # Size is defined separately (above)

#########################################################################################################
# INITIAL 'SPLASH' SCREEN TO SHOW THE DISPLAY IS LOADING                                                #
#                                                                                                       #
# There are 3 parts to this, and the only difference is that each part adds another '.' after 'Loading' #
# This gives the impression that something is happening (but nothing is - just a bit of fun             #
# The time.sleep after each part is how long before the next '.' shows                                  #
# After 3 '.' show, the main GUI starts within the While loop                                           #
#                                                                                                       #
#########################################################################################################

# Part 1
screen.fill(black) #Fill the screen with my pre-defined colour
fontloading=pygame.font.Font(None,40) # Font size
label=fontloading.render("Loading.", 1, (white)) # Define the message and colour
screen.blit(label,(100,110)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
pygame.display.flip() # I think this pushes my screen layout defined above - to the screen?
time.sleep(0.3) #Wait

# Part 2
screen.fill(black)
fontloading=pygame.font.Font(None,40)
label=fontloading.render("Loading..", 1, (white))
screen.blit(label,(100,110))
pygame.display.flip()
time.sleep(0.3)

# Part 3
screen.fill(black)
fontloading=pygame.font.Font(None,40)
label=fontloading.render("Loading...", 1, (white))
screen.blit(label,(100,110))
pygame.display.flip()
time.sleep(0.3)

#########################################################################
# Set an initial value for our time checking function in the While loop #
#########################################################################

timelastchecked = 0

############################################################################################################################
# WHILE LOOP TO MANAGE TOUCH SCREEN INPUTS                                                                                 #
#                                                                                                                          #
# You could say this is the main program - this runs the social media monitor screen and data                              #
# The while loop uses 'while 1' - which means this will loop forever until I stop it                                       #
# An important part is 'if time.time() >= timelastchecked:'                                                                #
# This says "if the current time is greater than equal to the 'timelastchecked' then run                                   # 
# Every time our while loop cycles, it adds 45 seconds to 'timelastchecked' - by running 'timelastchecked = time.time()+45 #
# This means time.time won't be greater or equal to 'timelastchecked' until 45 seconds has passed                          #
#                                                                                                                          #
############################################################################################################################

while 1:
	if time.time() >= timelastchecked: # Explained above...
	
		# Add 45 seconds to 'timelastchecked' - makes the while loop only run every 45 seconds. We don't need more frequent updates than that.
		timelastchecked = time.time()+45
		
		#######################################################################
		# SET UP THE STATIC SCREEN ELEMENTS - BACKGROUND, HEADINGS AND IMAGES #
		#######################################################################	
		
		# Set the background colour and border colour
		screen.fill(black)
		pygame.draw.rect(screen, black, (0,0,320,240),1) # Draw a rectangle (Surface, color, Rect, width)

		# load the social icon box image and place into position required
		logo=pygame.image.load("socialmediabox.png") # Logo image to load (must be in same directory as this script)
		screen.blit(logo,(210,40)) # Position of the logo on the screen - numbers are distance from left then top (left,top)		

		# Set the Twitter heading text
		label=font.render("Twitter", 1, (gold)) # define exit message and colour
		screen.blit(label,(5,40)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
		
		# Set the Facebook heading text
		label=font.render("Facebook", 1, (gold))
		screen.blit(label,(5,105))
		
		# Set the Google+ heading text
		label=font.render("Google+", 1, (gold)) # define exit message and colour
		screen.blit(label,(5,150)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
		
		# Set the Pinterest heading text
		label=font.render("Pinterest", 1, (gold)) # define exit message and colour
		screen.blit(label,(5,195)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
		
		###########################################################################
		# RUN A COMMAND TO GRAB THE PI TEMPERATURE                                #
		#                                                                         #
		# os.popen runs a command like you would in terminal                      #
		# Try '/opt/vc/bin/vcgencmd measure_temp' in terminal to see for yourself #
		# 'f' is a new line with the output of that command, which we will use    #
		#                                                                         #
		###########################################################################
		
		f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
		
		#######################################################################
		# READ OUR NEW LINE AND MANIPULATE INTO A LABEL FOR OUT GUI           #
		#                                                                     #
		# We make a new empty string called 'mytemp'                          #
		# We add the temperature line to this string                          #
		# We then chop off characters from the front and back                 #
		# We then set a font and colour for our PyGame label                  #
		# After this, we make our 'mytemp' string the label text              #
		# Finally, we 'blit' this to the screen (blit - to paste, add, paint) #
		#                                                                     #
		#######################################################################
		
		for i in f.readlines(): # Read the lines of 'f' - our temperature command output
			mytemp = "" # Create an empty string called 'mytemp'
			mytemp += i  # Add the temperature command line to our empty string
			mytemp = mytemp[5:-1] # Cut 5 characters from the front of our string, and 1 from the rear
			font2=pygame.font.Font(None,18) # Setting a custom font for the temp (font2)
			label=font2.render(mytemp, 1, (grey)) # Make our 'mytemp' string the label text for PyGame 
			screen.blit(label,(280,5)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
			
			#########################################################################
			# RUN A COMMAND TO GRAB THE TIME                                        #
			#                                                                       #
			# os.popen runs a command like you would in terminal                    #
			# Try 'date' in termianl to see for yourself                            #
			# 'f' is a new line with the output of that command, which we will use  #
			#                                                                       #
			#########################################################################
			
			f=os.popen("date") 
			
			#############################################################################################
			# SAME AS WITH THE TEMPERATURE COMMAND                                                      #
			#                                                                                           #
			# Read it, make it a string, chop it down, set the font, make the label then blit the label #
			#                                                                                           #
			#############################################################################################
			
			for i in f.readlines():  
				mytime = ""
				mytime += i  
				mytime = mytime[4:-13]  
				font3=pygame.font.Font(None,36)
				label=font3.render(mytime, 1, (white)) 
				screen.blit(label,(5,1))

				######################################################################################################################
				# GRAB TWITTER DATA USING URLLIB2                                                                                    #
				#                                                                                                                    #
				# Here we go to a URL and get our Pi to look for a line in the source code containing a certain string               #
				# This string has to be unique to this line or it will pull back multiple lines                                      #
				# The line we want is the line containing the data required, such as Twitter follower count                          #
				# Go to your public Twitter profile (logged out) and view the source                                                 #
				# Search for your number of Twitter followers using ctrl+f                                                           #
				# When you fine that number in the lines of code, find a unique string of text in that line that contains the data   #
				# Use that unique string below                                                                                       #
				# You will need to cut away the rest of that line in the code below, leaving you with just the data you want to see  #
				# Paste your unwanted characters into http://www.lettercount.com/ to count them for you                              #
				# ****NOTE If the site changes its layout or source code, things can move, and you will have to find this again****  #
				#                                                                                                                    #
				######################################################################################################################
			
				someurl= 'https://twitter.com/AverageManvsPi' # Set the URL for the Pi to look in to
				req = Request(someurl) # Request the URL
				try:
					response = urlopen(req)
				except URLError as e: #This section (307-317) is for error handling, showing "No connection" where a connection could not be made
					if hasattr(e, 'reason'):
						print 'We failed to reach a server.'
						print 'Reason: ', e.reason
						label=font.render("No Connection (1)", 1, (red))
						screen.blit(label,(5,60))
					elif hasattr(e, 'code'):
						print 'The server couldn\'t fulfill the request.'
						print 'Error code: ', e.code
						label=font.render("No Connection (2)", 1, (red))
						screen.blit(label,(5,60))
				else: # "If there are no errors and the connection is good"
					followcount = response.readlines() # read the lines of the URL and set these as a new string 'followcount'
					for line in followcount: # For statement
						if ' Followers"' in line: # If the Pi finds this string in the line...
							followcount = line[158:-32] # Take that line and cut away 158 characters from the front and 32 from the rear
							followcount = "Followers: " + followcount # Add text to the front of our data
							label=font.render(followcount, 1, (white)) # Make our 'followcount' string the label text for PyGame
							screen.blit(label,(5,60)) # Blits this new label onto the screen - numbers are distance from left then top (left,top)
							
						#########################################################################################################
						# RUNS ANOTHER QUERY ON THE SAME TWITTER URL IN THE SAME WAY - MAKES A SECOND LABEL WITH DIFFERENT DATA #
						#                                                                                                       #
						# This grabs my Twitter count of people that I follow                                                   #
						#                                                                                                       #
						#########################################################################################################
						
						if ' Following"' in line:
							tweetfollowing = line[158:-32]
							tweetfollowing = "Following: " + tweetfollowing
							label=font.render(tweetfollowing, 1, (white))
							screen.blit(label,(5,80))
					
							###########################################################
							# NOW FACEBOOK DATA IN THE SAME WAY AS WE DID FOR TWITTER #
							###########################################################
					
							someurl2= 'http://www.likealyzer.com/facebook/averagemanvspi'  
							req = Request(someurl2)  
							try:
								response = urlopen(req)
							except URLError as e:
								if hasattr(e, 'reason'):
									print 'We failed to reach a server.'
									print 'Reason: ', e.reason
									label=font.render("No Connection (3)", 1, (red))
									screen.blit(label,(5,125))
								elif hasattr(e, 'code'):
									print 'The server couldn\'t fulfill the request.'
									print 'Error code: ', e.code
									label=font.render("No Connection (4)", 1, (red))
									screen.blit(label,(5,125))
							else:							
								fblikes = response.readlines()
								for line in fblikes:
									if 'Likes:' in line:
										fblikes = line[75:-8]
										fblikes = "Facebook Likes: " + fblikes
										label=font.render(fblikes, 1, (white))
										screen.blit(label,(5,125))
								
										##########################################
										# NOW GOOGLE+ DATA IN THE SAME WAY AGAIN #
										##########################################
								
										someurl3= 'https://plus.google.com/+AverageManvsPi/posts'  
										req = Request(someurl3)  
										try:
											response = urlopen(req)
										except URLError as e:
											if hasattr(e, 'reason'):
												print 'We failed to reach a server.'
												print 'Reason: ', e.reason
												label=font.render("No Connection (5)", 1, (red))
												screen.blit(label,(5,170))
											elif hasattr(e, 'code'):
												print 'The server couldn\'t fulfill the request.'
												print 'Error code: ', e.code
												label=font.render("No Connection (6)", 1, (red))
												screen.blit(label,(5,170))
										else:			
											gpluslikes = response.readlines()
											for line in gpluslikes:
												if '</span> followers<span class' in line:
													gpluslikes = line[6802:-4444]
													gpluslikes = "Google+ Followers: " + gpluslikes
													label=font.render(gpluslikes, 1, (white))
													screen.blit(label,(5,170))
										
													#########################################################################
													# FINALLY, GRAB PINTEREST DATA AND CREATE A LABEL IN THE SAME WAY AGAIN #
													#########################################################################
										
													someurl4= 'https://uk.pinterest.com/averagemanvspi/'  
													req = Request(someurl4)  
													try:
														response = urlopen(req)
													except URLError as e:
														if hasattr(e, 'reason'):
															print 'We failed to reach a server.'
															print 'Reason: ', e.reason
															label=font.render("No Connection (7)", 1, (red))
															screen.blit(label,(5,215))
														elif hasattr(e, 'code'):
															print 'The server couldn\'t fulfill the request.'
															print 'Error code: ', e.code
															label=font.render("No Connection (8)", 1, (red))
															screen.blit(label,(5,215))
													else:	
														ytsubs = response.readlines()
														for line in ytsubs:
															if 'name="pinterestapp:followers"' in line:
																ytsubs = line[91:-12]
																ytsubs = "Pinterest Followers: " + ytsubs
																label=font.render(ytsubs, 1, (white))
																screen.blit(label,(5,215))
								
	#########################################################################################
	# SOME HANDY DEBUGGING CODE THAT WILL PRINT INFO TO TERMINAL WHEN THE SCREEN IS TOUCHED #
	#########################################################################################
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN: 
			print "screen pressed" # Tells us when the screen detects a press
			pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
			print pos # Prints the position of the press
			pygame.draw.circle(screen, white, pos, 2, 0) # Adds a small dot where the screen is pressed
			on_click()

		######################################################
		# A WAY TO EXIT THE PROGRAM IF THE TOUCHSCREEN FAILS #
		######################################################
		
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit()
				
	#########################################################################################################################
	# UPDATE THE DISPLAY - A VITAL PIECE OF THE CODE INCLUDED IN THE WHILE STATEMENT - WITHOUT, THE SCREEN WOULD NOT CHANGE #
	#########################################################################################################################
	
	pygame.display.update()