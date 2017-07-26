# coding: utf-8

# https://github.com/mikaelho/extend

from extend import Extender
from ui import View, Button

class BaseFormatting(Extender):

	def __init__(self):
		self.background_color = 'teal'
		self.font = ('Arial Rounded MT Bold', 24)
		
class ButtonFormatting(BaseFormatting):

	def __init__(self):
		BaseFormatting.__init__(self)
		self.tint_color = 'white'
		self.border_width = 2
		self.border_color = 'darkgrey'
		
class SelectedButtonFormatting(ButtonFormatting):

	def __init__(self):
		ButtonFormatting.__init__(self)
		self.background_color = 'maroon'
		
class ToggleButton(Extender):

	def __init__(self):
		self.toggle = False
		self.action = self.toggle_button
		
	def toggle_button(self, sender):
		if self.toggle: ButtonFormatting(self)
		else: SelectedButtonFormatting(self)
		self.toggle = self.toggle == False
		
		
v = View()
v.background_color = 'white'

button = ToggleButton(ButtonFormatting(Button(title = 'Click me')))
button.width = 200
button.height = 50
button.center = (v.width * 0.5, v.height * 0.5)
button.flex = 'LRTB'

v.add_subview(button)
v.present('sheet')

