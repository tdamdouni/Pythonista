# coding: utf-8

# https://forum.omz-software.com/topic/3115/ui-and-device-rotation-monitoring/4

from __future__ import print_function
import ui

class myView(ui.View):
	def __init__(self):
		self.scr_orientation = None
		self.present('full_screen')
		
	def draw(self):
		print('orientation = ' + self.scr_orientation)
		
	def layout(self):
		if self.width > self.height:
			self.scr_orientation = 'landscape'
		else:
			self.scr_orientation = 'portrait'
			
myView()
#orientation = landscape
#or
#orientation = portrait
#there's no orientation = None
#and everytime I tilt my device it changes

