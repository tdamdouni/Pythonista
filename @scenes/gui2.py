# coding: utf-8

# https://gist.github.com/LandyQuack/5183934

# https://forum.omz-software.com/topic/136/are-there-code-samples-on-how-to-create-forms-and-lists/5

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
		
	# Skeleton functions to be overriden		
	def touch_began(self,touch): pass
	def touch_moved(self,touch): pass
	def touch_ended(self,touch): pass

#-------------------------------------------------
class Button (Window):
	def __init__(self,p,b):
		Window.__init__(self,p,b)
		
		# Default to a red border of thickness 1.0
		self.stroke = Color(1,0,0)
		self.stroke_weight=1
		self.image = 'Snake'
	
	def touch_began(self,touch):
		new_color = Color(random(), random(), random())
		self.animate('background', new_color, 1.0)
		sound.play_effect('Crashing')
#-------------------------------------------------

# A window (a Layer) containing buttons
class ButtonBar (Window):
	def __init__(self,p,b,n):
		Window.__init__(self,p,b)
		
		# Parent window
		b = self.frame
		x = b.x
		
		for i in range(n):
			Button(self,Rect(x,b.y,b.w,b.h))
			x=x+128
		
#-------------------------------------------------

# A window (a Layer) containing Text
class Text (Window):
	def __init__(self,p,o,t,f,s):
		Window.__init__(self,p,Rect(o.x,o.y,0,0))
		self.tint = Color(0,0,0)
		self.text_img, ims = render_text(t,font_name=f, font_size=s)
		self.frame=Rect(o.x,o.y,ims.w,ims.h)

		self.image = self.text_img

	def touch_began(self,touch):
		sound.play_effect('Beep')
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
		
		# Now try a button bar
		ButtonBar (p,Rect(10,10,128,128),5)
		
		# And a label
		Text (p,Rect(10,200,100,100),'Woof', 'Futura', 100)
		      
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