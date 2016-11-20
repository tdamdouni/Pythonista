# coding: utf-8

# https://forum.omz-software.com/topic/3027/saving-pythonista-app-switch-and-button-states/5

import ui
import json
import os

class RememberMe(ui.View):
	def __init__(self):
		self.mysettings = None
		self.loadsettings()
		width, height = ui.get_screen_size()
		self.frame = (0,0,width,height)
		self.background_color = 'white'
		
		self.switch1 = ui.Switch()
		self.switch1.x = 50
		self.switch1.y = 50
		if self.mysettings != None:
			value = self.mysettings.get("switch1")
			self.switch1.value = value
		self.add_subview(self.switch1)
		self.present('full_screen')
		
	def will_close(self):
		if self.switch1.value == True:
			self.mysettings = {'switch1':True}
		else:
			self.mysettings = {'switch1':False}
		self.savesettings()
		
	def loadsettings(self):
		if os.path.exists("mysettings.json"):
			with open("mysettings.json", "r") as f:
				self.mysettings = json.load(f)
				
	def savesettings(self):
		with open("mysettings.json", "w") as f:
			json.dump(self.mysettings, f)
			
RememberMe()

