# yet another attempt at implementing game states/multiple scenes

from scene import *

class GameMain(Scene):
	def __init__(self,initState):
		self.currentState = initState
	def setup(self):
		w, h = self.size.w, self.size.h
		splashState.initState()
		playState.initState()
	def changeState(self, newState):
		self.currentState.exit()
		self.currentState = newState
		self.currentState.entry()
	def draw(self):
		self.update()
		self.currentState.draw()
	def update(self):
		self.currentState.update()
	def touch_began(self,touch):
		self.currentState.touch_began(touch)
		
class SplashState(Scene):
	startTime = 0
	def initState(self):
		self.size=GameContext.size
	# Normally states should be able to define entry and exit actions
	# Not all being used in this simple demo
	def entry(self):
		self.startTime = GameContext.t
	def exit(self):
		None
	def update(self):
		if (GameContext.t - self.startTime >= 1.0):
			GameContext.changeState(playState)
	def draw(self):
#               self.update()
		background(1,1,1)
		tint(1,0,0)
		text('splash!', 'Helvetica',60,self.size.w/2, self.size.h / 2)
	def touch_began(self, touch):
		GameContext.changeState(playState)
		
class PlayState(Scene):
	def initState(self):
		self.size=GameContext.size
		self.image = 'PC_Character_Horn_Girl'
	# Normally states should be able to define entry and exit actions
	# Not all being used in this simple demo
	def entry(self):
		None
	def exit(self):
		None
	def update(self):
		# do nothing yet, this is a big to-do...
		None
	def draw(self):
		background(1,0,1)
		tint(1.0, 1.0, 1.0)
		image(self.image,200,200, 300, 400)
	def touch_began(self, touch):
		GameContext.changeState(splashState)
		
# some global declarations and entry point
splashState = SplashState()
playState = PlayState()
GameContext = GameMain(splashState)
run(GameContext,PORTRAIT)

