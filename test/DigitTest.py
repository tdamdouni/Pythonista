# -*- coding: utf-8 -*-
from scene import *
#from time import *
from datetime import *
from sound import play_effect
from random import choice
import clipboard

import webbrowser
import urllib

class Button (object):
	def __init__(self, number,posx, posy, size):
		self.posx = posx
		self.posy = posy
		self.number = number
		self.size = size
		pass
		
class Result(object):
	def __init__(self, success, reactionTime, number):
		self.success = success
		self.reactionTime = reactionTime
		self.number = number
		pass
		
class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		#print('h: '+ str(self.size.h))
		#print('w: '+ str(self.size.w))
		
		# to configure
		self.maxRoundsToPlay = 3
		self.EndButton = [11,24,4,2]
		self.soundOn = False
		self.touchToRestart = True
		self.Font = 'Courier'
		
		self.endButtonPressed = False
		self.resultCounter = 0
		self.result = []
		self.success = False
		self.resultStored = False
		self.gameHasStarted = False
		self.gameHasEnded = False
		self.countdowninMin= 0
		self.countdownSec= 1
		self.countdown = timedelta(minutes = self.countdowninMin, seconds = self.countdownSec)
		self.countdownrunning = False
		self.Buttons = []
		self.resultsSubmitted = False
		self.lastReactionTime = 'none'
		
		#session id date and time
		dt = datetime.now()
		self.sessionID = str(dt)[0:16]
		
		
		#create Buttons
		offset = self.size.w // 15 -1
		self.offset = offset
		
		#where do the buttons go?
		offsetLines = [11,6,1]
		offsetColumns = [1,6,11]
		buttonsize = 4 #times
		offset
		z= 0       # button numbering starts at z+1
		
		for ol in offsetLines: # go through the lines
			for oc in offsetColumns: # go thorugh the columns
				z = z+1
				new_Button = Button(z,offset*oc,offset*ol,offset*buttonsize             )
				self.Buttons.append(new_Button)
				pass
			pass
		x = self.Buttons
		
	def draw_game(self):
		# This will be called for every frame (typically 60 times per second).
		reactiontime = self.lastReactionTime
		statustext = 'Touch to start'
		
		#draw background + buttons
		background(0.27, 0.47, 0.12) #background color
		
		#draw button
		fill(0.4,0.6,0.7) # button color
		stroke(1,1,1)
		stroke_weight(3)
		for b in self.Buttons:
			img, size = render_text(str(b.number), self.Font, b.size)
			rect(b.posx, b.posy, b.size, b.size)
			image(img, b.posx, b.posy, b.size, b.size)
			
		#draw 'End Button'
		offset = self.offset
		rect(offset*self.EndButton[0],offset*self.EndButton[1],offset*self.EndButton[2],offset*self.EndButton[3])
		text('End', self.Font,offset, offset*(self.EndButton[0]+1), offset*(self.EndButton[1]+0.5),9)
		
		#show number of attepmts
		text(str(self.resultCounter)+' of '+str(self.maxRoundsToPlay), self.Font, offset
		, offset, offset*26, 9)
		
		# Counting down to game begin
		if self.gameHasStarted  == False and self.countdownrunning == True:
			statustext = 'Waiting!'
			self.countdown = self.targetTime - datetime.now()
			if datetime.now() >= self.targetTime:
				#sound
				if self.soundOn == True:
					play_effect('Drums_06')
					
				self.countdownrunning = False
				self.gameHasStarted = True # enables touch and flag to show number
				
				#get random number
				all_numbers = range(1,9)
				self.displaynumber = choice(all_numbers)
				
				self.startTime = datetime.now()
				self.countdown = timedelta(minutes = 0, seconds = 0, microseconds = 0)
				
		if self.gameHasStarted == True and self.gameHasEnded == False:
			text(str(self.displaynumber), self.Font,offset*6, offset*8, offset*20, 5)
			statustext = 'React!'
			
		if self.gameHasEnded == True:
			#Result
			reactiontimefull = self.stopTime - self.startTime
			reactiontime = (reactiontimefull.seconds*10000+reactiontimefull.microseconds)/1000
			self.lastReactionTime = reactiontime
			
			if self.touchToRestart == False:
				self.reset_all()
			else:
				statustext = 'Touch to restart!'
				
			if self.resultStored == False:
				new_result = Result(self.success, reactiontime,self.displaynumber)
				self.result.append(new_result)
				self.resultCounter = self.resultCounter + 1
				
				self.resultStored = True
				
			#print
			
		text(str(self.success), self.Font,offset, offset*15, offset*18,4)
		text(str(reactiontime), self.Font, offset, offset*15, offset*17, 4)
		text(statustext, self.Font,offset, offset, offset * 17, 6)
		pass
		
	def draw_end_stats(self):
		background(0.2,0.2,0.2)
		offset = self.offset
		
		# for debugging print all result to console
		if self.resultsSubmitted == False:
			resultstring = ''
			counter = 1
			for r in self.result:
				resultstring = resultstring+ self.sessionID+';'+str(counter)+';'+str(r.number)+';'+str(r.success)+';'+str(r.reactionTime)+'\n'
				counter = counter +1
			clipboard.set(resultstring)
			self.resultsSubmitted =True
			
		text('Results passed \n to clipboard!\nTouch for Drafts',self.Font,offset//1.5,offset,offset*27,3)
		text(clipboard.get(),self.Font,offset//1.5,offset,offset*24,3)
		
		pass
		
	def end_touches(self, touch):
	
	
		# url encode
		sendstring = 'drafts://x-callback-url/create?action=appClipDropRT&x-success=pythonista://'
		
		# open in Drafts
		webbrowser.open(sendstring)
		
		sys.exit
		pass
		
	def game_touches(self, touch):
	# the thouches used for the game
	
		# first look for the end button
		if touch.location in Rect(self.EndButton[0]*self.offset, self.EndButton[1]*self.offset, self.EndButton[2]*self.offset,self.EndButton[3]*self.offset):
		
			self.endButtonPressed = True
			
		if self.countdownrunning == False and self.gameHasStarted == False:
			#Erster Touch. countdown wird eingeschalten.
			self.countdownrunning = True
			self.targetTime = datetime.now() + self.countdown
			
		elif self.countdownrunning == True and self.gameHasStarted == False:
			#Touch while 'waiting' = no action
			pass
			
		elif self.gameHasStarted == True and self.gameHasEnded == False:
			#Touch, measuring reaction time
			
			#Which button?
			for t in self.Buttons:
				if touch.location in Rect(t.posx,t.posy, t.size, t.size):
					self.ButtonTouched = t.number
					
					if t.number == self.displaynumber:
					# touched the correct button
						self.success = True
						
					else:
						self.success = False
						# touched the wrong button
						pass
						
			#stop the game and register the time
			self.gameHasEnded = True
			self.stopTime = datetime.now()
			
		elif self.gameHasEnded == True:
			# game has ended and the Touch will restart
			#print('Clause 4')
			if self.resultStored == True:
				self.reset_all()
				pass
				
	def draw(self):
	
		#print(self.endButtonPressed)
		if self.endButtonPressed == False and self.resultCounter < self.maxRoundsToPlay:
			self.draw_game()
		else:
			self.draw_end_stats()
		pass
		
	def touch_began(self, touch):
		if self.endButtonPressed == False and self.resultCounter < self.maxRoundsToPlay:
			self.game_touches(touch)
		else:
			self.end_touches(touch)
		pass
		
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
	def reset_all(self):
		#reset everything, but start Countdown (otherwise 2 touches are needed)
		self.countdownrunning = True
		self.gameHasStarted = False
		self.gameHasEnded = False
		self.resultStored = False
		
		#reset coutdown timer
		waiting_interval = 500000*choice(range(2,4))
		
		self.countdown = timedelta(microseconds = waiting_interval)
		self.targetTime = datetime.now() + self.countdown
		
		pass
		
run(MyScene(), PORTRAIT)

