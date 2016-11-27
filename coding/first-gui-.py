# A very simple first experiment in GUI creation using Pythonista
# on an iPad2. Creates two square buttons which change colour and
# make a noise when touched. It's modelled on what I vaguely remember
# of the innards of MS Windows

from scene import *
from random import random
import sound

# Base class for controls
class Window (Layer):
	# Create a default window
	def __init__(self,p,bounds):
		Layer.__init__(self, bounds)
		
		# Add ourself to parent layer list
		if p: p.add_layer(self)
		
		self.background=Color(1,1,1)
	#                       self.image = 'Snake'
	
		# Default to a red border of thickness 1.0
		self.stroke = Color(1,0,0)
		self.stroke_weight=1
		
	# Skeleton functions to be overriden
	def touch_began(self,touch): pass
	def touch_moved(self,touch): pass
	def touch_ended(self,touch): pass
	
#-------------------------------------------------
class Button (Window):
	def touch_began(self,touch):
		new_color = Color(random(), random(), random())
		self.animate('background', new_color, 1.0)
		sound.play_effect('Crashing')
#-------------------------------------------------

class MyApp (Scene):

	# This runs before any frames or layers are drawn
	def setup(self):
	
		# This is our background canvas (whole display)
		p = self.root_layer = Layer(self.bounds)
		
		center = self.bounds.center()
		
		# Create 2 primitive buttons as children of root layer
		Button(p,Rect(center.x + 80, center.y + 80, 128, 128))
		Button(p,Rect(center.x - 80, center.y - 80, 128, 128))
		
	def draw(self):
		# White background - basically display.clear() before redraw
		background(1, 1, 1)
		
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
	def touch_began(self, touch):
		l=touch.layer
		if l is Window: l.touch_began(touch)
		
	def touch_moved(self, touch):
		l=touch.layer
		if l is Window: l.touch_moved(touch)
		
	def touch_ended(self, touch):
		l=touch.layer
		if l is Window: l.touch_ended(touch)
		
run(MyApp())

