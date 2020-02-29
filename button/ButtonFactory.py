#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/46

from __future__ import print_function
import ui
from extend import Extender

def MyMother(sender):
	print('I love my Mums cooking')
	
class DefaultStyle(Extender):
	border_width = .5
	corner_radius = 3
	background_color = 'teal'
	tint_color = 'white'
	
class ButtonFactory(Extender):
	def __init__(self, parent = None, position = (0,0), **kwargs):
		if parent: parent.add_subview(self)
		self.size_to_fit()
		(self.x, self.y) = position
		self.width += 10
		self.action = MyMother
		for key, value in kwargs.iteritems():
			setattr(self, key, value)
			
			
view = ui.View(frame = (0,0,500,500))

button = ButtonFactory(
    DefaultStyle(
        ui.Button(title = 'What do I like?')),
    parent = view, tint_color = 'yellow')

view.present('sheet')

