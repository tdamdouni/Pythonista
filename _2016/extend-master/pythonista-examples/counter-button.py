# coding: utf-8

# https://github.com/mikaelho/extend

from extend import Extender
from ui import View, Button

class CounterButton(Extender):

	def __init__(self):
		self.click_count = 0
		self.action = self.increase_count
		
	def increase_count(self, sender):
		self.click_count += 1
		self.title = 'Clicked: ' + str(self.click_count)
		
v = View()
v.background_color = 'white'

button = CounterButton(Button(title = 'Click me'))
button.width = 200
button.center = (v.width * 0.5, v.height * 0.5)
button.flex = 'LRTB'

v.add_subview(button)
v.present('sheet')

