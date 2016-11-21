#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/60

import ui
from extend import Extender

class ChainingExtender(Extender):
	def e(self, cls, *args, **kwargs):
		return cls(self, *args, **kwargs)
		
class DefaultStyle(ChainingExtender):
	background_color = 'teal'
	tint_color = 'white'
	
class BorderedStyle(DefaultStyle):
	def __init__(self, border_width):
		self.border_width = border_width
		self.border_color = 'white'
		
class ButtonAction(ChainingExtender):
	def __init__(self, new_title = 'Not defined'):
		self.msg = new_title
	def action(self, sender):
		self.title = self.msg
		
button = ButtonAction(ui.Button(title = 'Click me'), 'Clicked').e(BorderedStyle, 10)

button.present()

