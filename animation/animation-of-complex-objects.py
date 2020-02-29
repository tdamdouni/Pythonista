# coding: utf-8

# https://forum.omz-software.com/topic/2531/animation-of-complex-objects

from __future__ import print_function
from scene import *
import ui

class MyScene(Scene):

	def draw(self):
	
	
		startx = 20
		starty = 20
		length = 100
		width = 200
		
		#simple shape
		# begin location
		fill(.5,.5,.5)
		rect(startx, starty, width, length )
		fill(0,1,0)
		rect(startx*2, starty, width/2, length/2)
		fill(1,0,0)
		ellipse(startx*2, starty*2, 10,10)
		ellipse(startx*8, starty*2, 10,10)
		
		
		
	def touch_began(self, touch):
		#end location
		print(touch.location.x, touch.location.y)
		push_matrix()
		scale(1.5, 1.5)
		translate(touch.location.x, touch.location.y)
		rotate(180)
		pop_matrix()
		
		
class SceneViewer(ui.View):
	def __init__(self, in_scene):
	
		self.present('fullscreen')
		self.scene_view = SceneView(frame=self.bounds)
		self.scene_view.scene = in_scene
		self.add_subview(self.scene_view)
		
		
SceneViewer(MyScene())

#==============================

# coding: utf-8
from scene import *
import ui

class MyScene(Scene):
	def setup(self):
		startx = 20
		starty = 20
		length = 100
		width = 200
		
		self.rect1 = Rect(startx, starty, width, length)
		self.rect2 = Rect(startx*2, starty, width/2, length/2)
		self.elli1 = Rect(startx*2, starty*2, 10, 10)
		self.elli2 = Rect(startx*8, starty*2, 10, 10)
		self.rect1_layer = Layer(self.rect1)
		self.rect1_layer.background = Color(.5,.5,.5)  #grey
		self.add_layer(self.rect1_layer)
		self.rect2_layer = Layer(self.rect2)
		self.rect2_layer.background = Color(0,1,0)  #green
		self.add_layer(self.rect2_layer)
		
	def draw(self):
		background(0,0,1)
		fill(0,1,1)        #cyan
		rect(*self.rect1)
		self.rect2_layer.update(self.dt)
		self.rect2_layer.draw()
		fill(1,0,0)        #red
		ellipse(*self.elli1)
		ellipse(*self.elli2)
		self.rect1_layer.update(self.dt)
		self.rect1_layer.draw()
		
	def touch_began(self, touch):
		self.rect1_layer.animate('alpha', 0.0, duration=1.0, autoreverse=False) # grey => cyan
		self.rect2_layer.animate('rotation', 180.0, duration=2.0, autoreverse=False)
		# Pythonista docu: Animatable attributes are frame, scale_x, scale_y, rotation, background, stroke, stroke_weight, tint and alpha.
		
class SceneViewer(ui.View):
	def __init__(self, in_scene):
		self.present('fullscreen')
		self.scene_view = SceneView(frame=self.bounds)
		self.scene_view.scene = in_scene
		self.add_subview(self.scene_view)
		
SceneViewer(MyScene())

