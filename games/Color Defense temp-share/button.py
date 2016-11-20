# coding: utf-8

import ui
import scene
import math
import random


class Button(object):
	
	def __init__(self, parent, x, y, w, h, border = True, rounded = True, text = "foo", color = 'white', bordercolor = 'black', textcolor = 'black',
																													altcolor = 'black', altbordercolor = 'white', alttextcolor = 'white'):
		#Basic button colors
		self.color = color
		self.textcolor = textcolor
		self.bordercolor = bordercolor
		
		#Colors for when button is pressed
		self.altcolor = altcolor
		self.altbordercolor = altbordercolor
		self.alttextcolor = alttextcolor
		
		#create button label and apply arguments
		self.label = scene.LabelNode(text)
		self.label.color = textcolor
		
		#create button path and shape
		#rounded variable determines rounded rect or not
		if rounded == True:
			self.path = ui.Path.rounded_rect(0, 0, w, h, 10)
		else:
			self.path = ui.Path.rect(0, 0, w, h)
		
		#Create button node
		self.node = scene.ShapeNode(self.path, stroke_color = self.bordercolor, position = (x, y))
		
		#Extra stuff
		self.node.line_width = 1.5
		self.node.fill_color = self.color
		
		#Add label to button, add button to parent scene
		self.node.add_child(self.label)
		parent.add_child(self.node)
    
	def was_pressed(self, loc):
		self.node.fill_color = self.altcolor
		self.node.stroke_color = self.altbordercolor
		self.label.color = self.alttextcolor
		
	def press_done(self):
		self.node.fill_color = self.color
		self.node.stroke_color = self.bordercolor
		self.label.color = self.textcolor
