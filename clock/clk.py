# https://gist.github.com/jsbain/6b7dcc13b39440217abfab7a51105d68

# https://forum.omz-software.com/topic/3107/two-instances-of-labels-updated-by-time/13

import ui,time
import bz2
from base64 import b64decode
import threading
import math
from objc_util import on_main_thread
import time
import sound


def run_async(func):
	from threading import Thread
	from functools import wraps
	
	@wraps(func)
	def async_func(*args, **kwargs):
		func_hl = Thread(target = func, args = args, kwargs = kwargs)
		func_hl.start()
		return func_hl
		
	return async_func
	
class clockster(object):

	def __init__(self,timelimit=60*60):
		compressedui = '''\
		QlpoOTFBWSZTWUc9NZEAAyzfgFUQUGd/9T+E3Qq/r976QAL8wYDa1TCSQIZMptTU9U9T1A
		A0xGTQAA9IESJSm9KYyjI0B6gHqfqmmg0ZAbSaBzTEwAJgAmAAEwABMEUo1MU2INIaeoAA
		AABoBpXQDYpCgnMlgf2mycngJQSSASdLEzlBE5ICGEGigpRUClAG9AcCEJCOSCFKfaGiDh
		SsfT89nQ2zcEg7mdbgkZNxVIFjoWDp1dnjaTI1uRycNb7nnbm6zJ2+GcDwENYpsTVsTYQs
		jG7KAq2mEMMSkuwJSUW4hREinC29Pg1yR0haUlpFTbJAfX57Ye3OtskxEvGlTtjiG/o5O1
		y81U2oR68XN1cHU6FvutEzMm/AyR01Pa1mGUPZ0Mw5JEJpFNMKIa138TPQzFWCJsSK2OyA
		4HOW09a8cJT3yMr5jxDYXpkIyiSpoz7PudZRMPhnrQdFRcUkjIzUeFoBjuxhhVt5Pg/HcO
		wNGq04b69+xCsnEVEmieM6Y4ak91LUOZ2kIQ0fqgQPX8ULqlLasbsYz1tKzYU5pRn2rDO9
		Q2rXbPdptKEJ0aD4VxleN50jnWw+ON2hltb5LIXqDxDl707pG9cQj4Bejn50dsursYDwHp
		0VkiHnSQFKlqkhgSNCx9DNMp8OUbMJS729xDWYaYSI/5IXHo/sCVoMEHUkRDjGgCdxUOkS
		5ZDiqmYM6UgmNxH6UvdcWiOU1yRmLRHdtUTOSOR/gJFiQtrri8yVzCTMKFw52QyvaUu/gr
		ZxwNVIH2GoNpoojgqBqtzzagE1RIwSHRFmxqkRBZIwAyJlUvcb+NjMhYZBrcw4W+JEFx7G
		QJyBwFAWjcTJhzD1BUma8ICoTS2pWfKQmhiQCDkpfsTbjcpgP3zM+tE+ZcE/4u5IpwoSCO
		emsiA=
		'''
		pyui = bz2.decompress(b64decode(compressedui))
		v = ui.load_view_str(pyui.decode('utf-8'))
		self.v = v
		self.v.present('sheet')
		self.timelimit=timelimit
		
		self.startTime = time.time()
		self.gameBegun = False
		
		self.playerOne = self.v["playerOne"]
		self.playerTwo = self.v["playerTwo"]
		self.playerOne.tint_color='green'
		self.playerTwo.tint_color='green'
		self.playerOne.sound='casino:ChipsStack3'
		self.playerTwo.sound='casino:ChipsStack6'
		self.playerOne.border_width=1
		self.playerTwo.border_width=1
		self.playerOne.height=44
		self.playerTwo.height=44
		self.playerOne.opponentTimeElapsed = 0
		self.playerTwo.opponentTimeElapsed = 0
		self.playerOne.latestTurnElapsed = 0
		self.playerTwo.latestTurnElapsed = 0
		self.playerOne.currentOppTime=0
		self.playerTwo.currentOppTime=0
		self.lastPlayerToTap = "NOBODY"
		self.lastTimeToggled=self.startTime
		sound.load_effect(self.playerOne.sound)
		sound.load_effect(self.playerTwo.sound)
		self.mainLoop()
		
		
	def togglePlayer(self,sender):
		triggerTime=time.time()
		if self.lastPlayerToTap == sender:
			return
		elif self.game_over():
			return
		elif self.lastPlayerToTap == "NOBODY":
			#start the game
			self.gameBegun = True
			self.startTime = triggerTime
			self.lastTimeToggled = triggerTime
			sound.play_effect(sender.sound)
			self.lastPlayerToTap = sender
			self.lastPlayerToTap.tint_color='red'
			
		else:
			#update elapsed time of current player, flip tint, and update labels
			latestTurnElapsed= (triggerTime-self.lastTimeToggled)
			self.lastPlayerToTap.opponentTimeElapsed += latestTurnElapsed
			self.lastPlayerToTap.latestTurnElapsed=0
			#swap player, update labels
			self.lastPlayerToTap.tint_color='green'
			sender.tint_color='red'
			
			self.lastPlayerToTap = sender
			
			self.lastTimeToggled = triggerTime
			#update labels
			timeError=self.updateLabels()
			sound.play_effect(sender.sound)
			#sanity check that times add up
			if abs(timeError)>0.00001:
				print(timeError)
	def formatTime(self,t):
		'''format as H:MM:SS:hundreths'''
		t=max(t,0)
		hours,remainder=divmod(t,60*60)
		minutes,remainder=divmod(remainder,60)
		sec, hundredths=divmod(remainder*100, 100)
		
		return'{:1.0f}:{:02.0f}:{:02.0f}:{:02.0f}'.format(hours,minutes,sec,round(hundredths,0))
	def updateLabels(self):
		'''update labels. return difference between total time and sum of player times'''
		
		if self.lastPlayerToTap!='NOBODY':
			currentTime=time.time()
			self.lastPlayerToTap.latestTurnElapsed= (currentTime-self.lastTimeToggled)
		else:
			currentTime=0
		#update BOTH players labels ensure we have accurate time shown
		self.playerOne.currentOppTime = self.playerOne.opponentTimeElapsed +self.playerOne.latestTurnElapsed
		self.v["playerTwoTime"].text = self.formatTime(self.timelimit-self.playerOne.currentOppTime)
		
		self.playerTwo.currentOppTime = self.playerTwo.opponentTimeElapsed +self.playerTwo.latestTurnElapsed
		self.v["playerOneTime"].text = self.formatTime(self.timelimit-self.playerTwo.currentOppTime)
		
		#update elapsed time
		totalTimeElapsed=currentTime-self.startTime
		self.v["totalTime"].text = self.formatTime(totalTimeElapsed)
		
		#check for discrepancy
		return totalTimeElapsed-(self.playerTwo.currentOppTime+self.playerOne.currentOppTime)
	def game_over(self):
		if self.timelimit-self.playerOne.currentOppTime<0:
			sound.play_effect('game:Error')
			return True
		if self.timelimit-self.playerTwo.currentOppTime<0:
			sound.play_effect('game:Error')
			return True
	@run_async
	def mainLoop(self):
		self.updateLabels()
		while self.v.on_screen and not self.game_over():
			if self.gameBegun is True:
				self.updateLabels()
			time.sleep(0.01)
			
if __name__ == "__main__":
	a = clockster(9)

