#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/57

from __future__ import print_function
import ui
from extend import Extender

class DefaultStyle(Extender):
	background_color = 'teal'
	tint_color = 'white'
	
class BorderedStyle(DefaultStyle):
	border_width = .5
	corner_radius = 3
	
class ButtonAction(Extender):
	def __init__(self, msg = None):
		self.msg = msg
	def action(self, sender):
		print(self.msg)
		
button = BorderedStyle(ButtonAction(ui.Button(title = 'Click me'), 'Clicked'))

button.present()

