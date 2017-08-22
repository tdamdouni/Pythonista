# coding: utf-8

# https://forum.omz-software.com/topic/3964/unipage-as-a-bridge-between-kivy-and-pythonista/28

#-----------------------------------------------------------------------------
# Name:      UniPaGe
# Purpose:   Adaptable Graphic User Interface for Python
#
# Author:    Ti Leyon
#
# Created:   04/04/2017
# Copyright: (c) Ti Leyon 2017
# Licence:   This work is licensed under the
#            Creative Commons Attribution-ShareAlike 4.0 International License.
#            To view a copy of this license, visit:
#            http://creativecommons.org/licenses/by-sa/4.0/
#            or send a letter to:
#            Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#-----------------------------------------------------------------------------

class unipage(object):

	def __init__(self, kivy, screen_size):
		self.kivy = kivy
		self.screen_size = screen_size
		self.unibuttons = []
		self.unitexts = []
		self.unilabels = []
		self.unimages = []
		self.uniframes = []
		self.xratio = self.screen_size[0] / 800.0
		self.yratio = self.screen_size[1] / 600.0
		
	def setscreen(self):
		if self.kivy:
			from kivy.uix.floatlayout import FloatLayout
			from kivy.core.window import Window
			self.root = FloatLayout()
			if (self.xratio == 0) or (self.yratio == 0):
				from kivy.utils import platform as core_platform
				if core_platform == 'android':
					self.screen_size = Window.size
				else:
					self.screen_size = (800, 600)
				self.xratio = self.screen_size[0] / 800.0
				self.yratio = self.screen_size[1] / 600.0
				
			Window.size = self.screen_size
		else:
			import ui
			if (self.xratio == 0) or (self.yratio == 0):
				ss1 = ui.get_screen_size()[0]
				ss3 = ui.get_screen_size()[1]
				notoptimal = True
				while notoptimal:
					if ss1 % 8 == 0:
						notoptimal = False
					else:
						ss1 -= 1
				ss1 = ss1 - 124
				ss2 = (ss1 / 4) * 3
				if ss2 > ss3:
					print('yes')
					ss2 = ss3 - ss2 - ((ss3 - ss2) % 3)
					ss1 = (ss2 / 3) * 4
				self.screen_size = (ss1, ss2)
				self.xratio = self.screen_size[0] / 800
				self.yratio = self.screen_size[1] / 600
				
			self.root = ui.View(frame=(0,0,self.screen_size[0], \
			self.screen_size[1]))
			
	def unibutton(self, params):
		self.unibuttons.append([])
		if len(params) == 6:
			function = params[5]
		else:
			function = nofunction
		if self.kivy:
			from kivy.uix.button import Button
			self.unibuttons[len(self.unibuttons) - 1] = Button(
			text = params[4],
			size_hint_y = None,
			size_hint_x = None,
			height = params[3] * self.yratio,
			width = params[2] * self.xratio,
			pos = (params[0] * self.xratio, params[1] * self.yratio),
			on_press = function )
			self.root.add_widget(self.unibuttons[len(self.unibuttons) - 1])
		else:
			import ui
			self.unibuttons[len(self.unibuttons) - 1] = ui.Button(frame= \
			(params[0] * self.xratio, (600 - params[1] - params[3]) * self.yratio, \
			params[2] * self.xratio, params[3] * self.yratio), title = params[4])
			self.unibuttons[len(self.unibuttons) - 1].background_color \
			= (0.4,0.4,0.4)
			self.unibuttons[len(self.unibuttons) - 1].action = function
			self.unibuttons[len(self.unibuttons) - 1].height = params[3] * self.xratio
			self.unibuttons[len(self.unibuttons) - 1].width = params[2] * self.yratio
			self.unibuttons[len(self.unibuttons) - 1].tint_color = 'white'
			self.root.add_subview(self.unibuttons[len(self.unibuttons) - 1])
			
	def unitext(self, params):
		self.unitexts.append([])
		if self.kivy:
			from kivy.uix.textinput import TextInput
			self.unitexts[len(self.unitexts) - 1] = TextInput (
			id = 'text' + str(len(self.unitexts) - 1),
			size_hint_y = None,
			size_hint_x = None,
			height = params[3] * self.yratio,
			width = params[2] * self.xratio,
			text = params[4],
			multiline = True,
			pos = (params[0] * self.xratio, params[1] * self.yratio))
			self.root.add_widget(self.unitexts[len(self.unitexts) - 1])
		else:
			import ui
			self.unitexts[len(self.unitexts) - 1] = ui.TextField(frame=
			(params[0] * self.xratio, (600 - params[1] - params[3]) * \
			self.yratio, params[2] * self.xratio, params[3] * self.yratio))
			self.unitexts[len(self.unitexts) - 1].bordered = False
			self.unitexts[len(self.unitexts) - 1].background_color = 'white'
			self.unitexts[len(self.unitexts) - 1].font = ('<system>', 23 * self.xratio)
			self.unitexts[len(self.unitexts) - 1].text = params[4]
			self.root.add_subview(self.unitexts[len(self.unitexts) - 1])
			
	def unilabel(self, params):
		self.unilabels.append([])
		if self.kivy:
		
			from kivy.uix.label import Label
			self.unilabels[len(self.unilabels) - 1] = Label(pos = \
			(params[0] * self.xratio, params[1] * self.yratio), \
			size_hint=(1.0,1.0), halign="left", \
			valign="bottom", text = params[4])
			self.unilabels[len(self.unilabels) - 1].bind(size= \
			self.unilabels[len(self.unilabels) - 1].setter('text_size'))
			self.root.add_widget(self.unilabels[len(self.unilabels) - 1])
			
		else:
		
			import ui
			
			self.unilabels[len(self.unilabels) - 1] = ui.Label(frame= \
			(params[0] * self.xratio,  (600 - params[1] - params[3]) * self.yratio, \
			params[2] * self.xratio, params[3] * self.yratio))
			self.unilabels[len(self.unilabels) - 1].text = params[4]
			self.unilabels[len(self.unilabels) - 1].text_color = 'white'
			self.unilabels[len(self.unilabels) - 1].alignment = ALIGN_LEFT = True
			self.unilabels[len(self.unilabels) - 1].font = ('<system>', 18 * self.xratio)
			self.root.add_subview(self.unilabels[len(self.unilabels) - 1])
			
	def unimage(self, params):
		self.unimages.append([])
		if self.kivy:
			from kivy.uix.image import Image
			
			self.unimages[len(self.unimages) - 1] = Image( source= params[4],
			allow_stretch = True, size_hint = (None, None),
			size=(params[2] * self.xratio, params[3] * self.yratio),
			pos=(params[0] * self.xratio, params[1] * self.yratio))
			
			self.root.add_widget(self.unimages[len(self.unitexts) - 1])
			
		else:
			import ui
			
			self.unimages[len(self.unimages) - 1] = (ui.ImageView
			(name = 'Image', frame = (params[0] * self.xratio, \
			(600 - params[1] - params[3]) * self.yratio, \
			params[2] * self.xratio, params[3] * self.yratio)))
			
			self.root.add_subview (self.unimages[len(self.unimages) - 1])
			
			self.unimages[len(self.unitexts) - 1].image = ui.Image.named(params[4])
			
	def uniframe(self, params):
		if self.kivy:
			from kivy.graphics import Color
			from kivy.graphics import Rectangle
			self.root.canvas.add(Color (params[4][0],params[4][1], params[4][2]))
			self.root.canvas.add(Rectangle(pos = (params[0] * self.xratio, \
			params[1] * self.yratio), size = (params[2] * self.xratio, \
			params[3] * self.yratio)))
		else:
			import ui
			self.uniframes.append([])
			self.uniframes[len(self.uniframes) - 1] = \
			ui.View(frame=(params[0] * self.xratio, \
			(600 - params[1] - params[3]) * self.yratio, \
			params[2] * self.xratio, params[3] * self.yratio))
			self.uniframes[len(self.uniframes) - 1].background_color = \
			(params[4][0],params[4][1], params[4][2],1.0)
			self.root.add_subview(self.uniframes[len(self.uniframes) - 1])
			
	def showpage(self):
		if self.kivy:
			from kivy.base import runTouchApp
			runTouchApp(self.root)
		else:
			self.root.present('sheet')
			
class uniscreen(unipage):
	screendef = []
	def __init__(self, screendef):
		try:
			from kivy.uix.floatlayout import FloatLayout
			kivy = True
		except:
			import ui
			kivy = False
		unipage.__init__(self, kivy, screendef[0])
		self.setscreen()
		self.screendef = screendef
		
	def setpage(self):
		for k in range(1, len(self.screendef)):
			self.screendef[k][0](self, self.screendef[k][1])
			
def closepage(sender):
	if mypage.kivy:
	
		from kivy.utils import platform as core_platform
		from kivy.core.window import Window
		import sys
		
		if core_platform == 'android':
			sys.exit()
		else:
			Window.close()
			
	else:
	
		mypage.root.close()
		
def function_1(sender):
	mypage.unitexts[0].text = 'Oh! You clicked my button.'
	
def nofunction(sender):
	pass
	
if __name__ == '__main__':
	unilabel = unipage.unilabel
	uniframe = unipage.uniframe
	unitext = unipage.unitext
	unibutton = unipage.unibutton
	unimage = unipage.unimage
	widgets = [(0, 0),
	(uniframe,(0, 0, 600, 450,(.6,.6,.6))),
	(unilabel,(80, 300, 240, 20, 'Hey I am just a simple label.')),
	(unibutton,(40, 40, 100, 40, 'Click me', function_1)),
	(unibutton,(460, 40, 100, 40, 'Close me', closepage)),
	(unitext,(40, 120, 300, 40, 'I am a text field')),
	(unimage,(460, 310, 100, 100,'insidelogo.png'))
	]
	mypage = uniscreen(widgets)
	mypage.setpage()
	mypage.showpage()

