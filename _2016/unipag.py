# https://forum.omz-software.com/topic/3963/unipage-as-a-bridge-between-kivy-and-pythonista

# The Universal Python Adaptable GUI Extensions (UniPAGe) started as a general interface for researches I was doing in a mathematical form of memory. Multiple platforms graphical user interfaces are now the norm and I did not want to have to continuously rewrite my interface for every single OS that i use. I decided to implement my study in Python with the understanding that the Kivy environment will allow me to use the same code under all five major platforms. I soon realize that although Kivy cover all those environments you have to compile you script to run them in Android and send them to an intermediate script compatible with Xcode in order to test them under IOS. This was unacceptable since my interfaces evolved two to three times a week. Then I discovered Pythonista and the Kivy Launcher came along. Although the Kivy Launcher allowed me to test my scripts on the fly within Android, Pythonista was by no means compatible with Kivy. While experimenting with Pythonista I gradually discerned that it was syntactically more closely related to Kivy than I originally thought. A “view” in Pythonista becomes a “widget” under Kivy. Therefore “add_subview” in the former is equivalent to “add_widget” in the latter. Most of the common ui elements either share the same name or same etymology. “Label” and “Button” are the same while “TextField” and “ImageView” are expressed as “TextInput” and “Image” respectively. I could not post my original modules since they are intertwine with the work mentioned above and could conflict with their “Patent Pending” status. Realizing that this is a popular topic in the Pythonista community (1.6 k views on a 2 year old post that has been revived recently with no proposed solutions) I wrote a new concise but functional and useful version of UniPAGe. As @Phuket2 would say “the below” is the first result of that effort. By the way @Phuket2 I mean no disrespect I admire the way you work and became used to your syntax.

#-----------------------------------------------------------------------------

#Name: UniPAGe

#Purpose: Adaptable Graphic User Interface for Python

#Author: Ti Leyon

#Created: 04/04/2017

#Copyright: (c) Ti Leyon 2017

#Licence: K E

#Github: https://github.com/Tileyon/UniPAGe

#-----------------------------------------------------------------------------

class unipage(object):
	def init(self, kivy, screen_size):
		self.kivy = kivy
		self.screen_size = screen_size
		self.unibuttons = []
		self.unitexts = []
		self.unilabels = []
		self.unimages = []
		self.uniframes = []

def setscreen(self):
	if self.kivy:
		from kivy.uix.floatlayout import FloatLayout
		from kivy.core.window import Window
		self.root = FloatLayout()
		Window.size = self.screen_size
	else:
		import ui
		self.root = ui.View(frame=(0,0,self.screen_size[0], self.screen_size[1]))
		
def unibutton(self, params):
	xratio = self.screen_size[0] / 800.0
	yratio = self.screen_size[1] / 600.0
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
		height = params[3] * yratio,
		width = params[2] * xratio,
		pos = (params[0] * xratio, params[1] * yratio),
		on_press = function )
		self.root.add_widget(self.unibuttons[len(self.unibuttons) - 1])
	else:
		import ui
		self.unibuttons[len(self.unibuttons) - 1] = ui.Button(frame= \
		(params[0] * xratio, (600 - params[1] - params[3]) * yratio, \
		params[2] * xratio, params[3] * yratio), title = params[4])
		self.unibuttons[len(self.unibuttons) - 1].background_color \
		= (0.4,0.4,0.4)
		self.unibuttons[len(self.unibuttons) - 1].action = function
		self.unibuttons[len(self.unibuttons) - 1].height = params[3] * xratio
		self.unibuttons[len(self.unibuttons) - 1].width = params[2] * yratio
		self.unibuttons[len(self.unibuttons) - 1].tint_color = 'white'
		self.root.add_subview(self.unibuttons[len(self.unibuttons) - 1])
		
def unitext(self, params):
	xratio = self.screen_size[0] / 800.0
	yratio = self.screen_size[1] / 600.0
	self.unitexts.append([])
	if self.kivy:
		from kivy.uix.textinput import TextInput
		self.unitexts[len(self.unitexts) - 1] = TextInput (
		id = 'text' + str(len(self.unitexts) - 1),
		size_hint_y = None,
		size_hint_x = None,
		height = params[3] * yratio,
		width = params[2] * xratio,
		text = params[4],
		multiline = True,
		pos = (params[0] * xratio, params[1] * yratio))
		self.root.add_widget(self.unitexts[len(self.unitexts) - 1])
	else:
		import ui
		self.unitexts[len(self.unitexts) - 1] = ui.TextField(frame=
		(params[0] * xratio, (600 - params[1] - params[3]) * \
		yratio, params[2] * xratio, params[3] * yratio))
		self.unitexts[len(self.unitexts) - 1].bordered = False
		self.unitexts[len(self.unitexts) - 1].background_color = 'white'
		self.unitexts[len(self.unitexts) - 1].font = ('<system>', 23 * xratio)
		self.unitexts[len(self.unitexts) - 1].text = params[4]
		self.root.add_subview(self.unitexts[len(self.unitexts) - 1])
		
def unilabel(self, params):
	xratio = self.screen_size[0] / 800.0
	yratio = self.screen_size[1] / 600.0
	self.unilabels.append([])
	if self.kivy:
	
		from kivy.uix.label import Label
		self.unilabels[len(self.unilabels) - 1] = Label(pos = \
		(params[0] * xratio, params[1] * yratio), \
		size_hint=(1.0,1.0), halign="left", \
		valign="bottom", text = params[4])
		self.unilabels[len(self.unilabels) - 1].bind(size= \
		self.unilabels[len(self.unilabels) - 1].setter('text_size'))
		self.root.add_widget(self.unilabels[len(self.unilabels) - 1])
		
	else:
	
		import ui
		
		self.unilabels[len(self.unilabels) - 1] = ui.Label(frame= \
		(params[0] * xratio,  (600 - params[1] - params[3]) * yratio, \
		params[2] * xratio, params[3] * yratio))
		self.unilabels[len(self.unilabels) - 1].text = params[4]
		self.unilabels[len(self.unilabels) - 1].text_color = 'white'
		self.unilabels[len(self.unilabels) - 1].alignment = ALIGN_LEFT = True
		self.unilabels[len(self.unilabels) - 1].font = ('<system>', 18 * xratio)
		self.root.add_subview(self.unilabels[len(self.unilabels) - 1])
		
def unimage(self, params):
	xratio = self.screen_size[0] / 800.0
	yratio = self.screen_size[1] / 600.0
	self.unimages.append([])
	if self.kivy:
		from kivy.uix.image import Image
		
		self.unimages[len(self.unimages) - 1] = Image( source= params[4],
		allow_stretch = True, size_hint = (None, None),
		size=(params[2] * xratio, params[3] * yratio),
		pos=(params[0] * xratio, params[1] * yratio))
		
		self.root.add_widget(self.unimages[len(self.unitexts) - 1])
		
	else:
		import ui
		
		self.unimages[len(self.unimages) - 1] = (ui.ImageView
		(name = 'Image', frame = (params[0] * xratio, \
		(600 - params[1] - params[3]) * yratio, \
		params[2] * xratio, params[3] * yratio)))
		
		self.root.add_subview (self.unimages[len(self.unimages) - 1])
		
		self.unimages[len(self.unitexts) - 1].image = ui.Image.named(params[4])
		
def uniframe(self, params):
	xratio = self.screen_size[0] / 800.0
	yratio = self.screen_size[1] / 600.0
	if self.kivy:
		from kivy.graphics import Color
		from kivy.graphics import Rectangle
		self.root.canvas.add(Color (params[4][0],params[4][1], params[4][2]))
		self.root.canvas.add(Rectangle(pos = (params[0] * xratio, \
		params[1] * yratio), size = (params[2] * xratio, \
		params[3] * yratio)))
	else:
		import ui
		xratio = self.screen_size[0] / 800.0
		yratio = self.screen_size[1] / 600.0
		self.uniframes.append([])
		self.uniframes[len(self.uniframes) - 1] = ui.View(frame=(params[0] * xratio, \
		(600 - params[1] - params[3]) * yratio, \
		params[2] * xratio, params[3] * yratio))
		self.uniframes[len(self.uniframes) - 1].background_color = (params[4][0],params[4][1], params[4][2],1.0)
		self.root.add_subview(self.uniframes[len(self.uniframes) - 1])
		
def showpage(self):
	if self.kivy:
		from kivy.base import runTouchApp
		runTouchApp(self.root)
	else:
		self.root.present('sheet')
class uniscreen(unipage):
	screendef = []
def init(self, screendef):
	try:
		from kivy.uix.floatlayout import FloatLayout
		kivy = True
	except:
		import ui
kivy = False
unipage.init(self, kivy, screendef[0])
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

if name == 'main':
unilabel = unipage.unilabel
uniframe = unipage.uniframe
unitext = unipage.unitext
unibutton = unipage.unibutton
unimage = unipage.unimage
widgets = [(600, 450),
(uniframe,(0, 0, 600, 450,(.6,.6,.6))),
(unilabel,(80, 10, 240, 20, 'Hey I am just a simple label.')),
(unibutton,(40, 40, 100, 40, 'Click me', function_1)),
(unibutton,(460, 40, 100, 40, 'Close me', closepage)),
(unitext,(40, 120, 300, 40, 'I am a text field')),
(unimage,(460, 310, 100, 100,'insidelogo.png'))
]
mypage = uniscreen(widgets)
mypage.setpage()
mypage.showpage()

