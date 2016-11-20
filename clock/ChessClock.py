# https://gist.github.com/Tkizzy/b8e6f213d19e9d4668a7f28bbd1efe9f

# https://forum.omz-software.com/topic/3107/two-instances-of-labels-updated-by-time/9

import ui,time
import bz2
from base64 import b64decode


#https://gist.github.com/c61951cc318e7beaf378f6c292f94883
#v = ui.load_view()
#v.present('sheet')

class clockster(object):

	def __init__(self):
		#self.v = ui.load_view()
		
		
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
		
		print(self.v["playerOne"])
		
		self.startTime = time.time()
		self.gameBegun = False
		
		
		self.playerOne = self.v["playerOne"]
		self.playerTwo = self.v["playerTwo"]
		self.playerOne.totalTimeElapsed = 0
		self.playerTwo.totalTimeElapsed = 0
		self.playerOne.latestTurnElapsed = 0
		self.playerTwo.latestTurnElapsed = 0
		self.currentActivePlayer = "NOBODY"
		
		
		self.mainLoop()
		
	def togglePlayer(self,sender):
		print(sender)
		print(self.currentActivePlayer)
		if self.currentActivePlayer == sender:
			print("no change....")
			pass
			
		elif self.currentActivePlayer == "NOBODY":
			print("this meNS THE GME HAS BEGUN")
			self.gameBegun = True
			self.startTime = time.time()
			self.currentActivePlayer = sender
			self.lastTimeToggled = time.time()
			print('game has begun with',sender.name)
			
		else:
			print('player changed')
			#cleaning up old active plyayer
			self.currentActivePlayer.totalTimeElapsed = self.currentActivePlayer.totalTimeElapsed+self.currentActivePlayer.latestTurnElapsed
			
			
			#new active player
			self.currentActivePlayer = sender
			self.lastTimeToggled = time.time()
			
			print("player toggled to",sender.name)
			
			
			
			
	def switchClockOnForSelectedPlayer(self):
	
		if self.currentActivePlayer == self.playerOne:
			self.playerOne.latestTurnElapsed= (time.time()-self.lastTimeToggled)
			self.playerOne.timeToDisplay = self.playerOne.totalTimeElapsed +self.playerOne.latestTurnElapsed
			self.v["playerOneTime"].text = str(round(self.playerOne.timeToDisplay))
			
		elif self.currentActivePlayer == self.playerTwo:
			self.playerTwo.latestTurnElapsed= (time.time()-self.lastTimeToggled)
			self.playerTwo.timeToDisplay = self.playerTwo.totalTimeElapsed +self.playerTwo.latestTurnElapsed
			self.v["playerTwoTime"].text = str(round(self.playerTwo.timeToDisplay))
			
			
	@ui.in_background
	def mainLoop(self):
	
	
	
		while True:
		
		
		
			self.switchClockOnForSelectedPlayer()
			if self.gameBegun is True:
			
				timeElapsed = round(time.time()-self.startTime,0)
				print(round(time.time()-self.startTime))
				self.v["totalTime"].text = str(timeElapsed)
			#print(time.time())
			time.sleep(1)
			
			
		mainLoop()
		
		
		
if __name__ == "__main__":
	a = clockster()

