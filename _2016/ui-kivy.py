# https://gist.github.com/balachandrana/4e9accfc894785682f230c54dc5da816#file-ui-py

# https://forum.omz-software.com/topic/3964/unipage-as-a-bridge-between-kivy-and-pythonista/5

from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.utils import platform as core_platform
import sys

from kivy.uix.label import Label as KivyLabel
from kivy.uix.button import Button as KivyButton
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage

from kivy.graphics import Color
from kivy.graphics import Rectangle

#class View(object):
#	screen_size = (800, 600)
#	xratio = screen_size[0] / 800.0
#	yratio = screen_size[1] / 600.0
#	def __init__(self, frame=(0,0,100,100),
#	name=''):
#		self.frame = frame
#		self.name = name
#		self.superview = None
#		self.uniobject = None
#		self.rootdict = {}
		
class View(object):
	screen_size = (800, 600)
	xratio = screen_size[0] / 800.0
	yratio = screen_size[1] / 600.0
	
	def __init__(self, frame=(0, 0, 100, 100), name=''):
		self.frame = frame
		self.name = name
		self.superview = None
		self.uniobject = None
		self.rootdict = {}
		
	@property
	def kivy_pos(self):
		"""Convert a Pythonista ui frame into a Kivy x, y position"""
		x, y, _, _ = self.frame
		return x * self.xratio, y * self.yratio
		
	@property
	def kivy_size(self):
		"""Convert a Pythonista ui frame into a Kivy width, height size"""
		_, _, w, h = self.frame
		return w * self.xratio, h * self.yratio
		
	@property
	def kivy_rect(self):
		"""Convert a Pythonista ui frame into a Kivy Rectangle"""
		return Rectangle(pos=self.kivy_pos, size=self.kivy_size)
		
class MainView(View):
	def __init__(self, frame=(0,0,100,100), name=''):
		super().__init__(frame=frame, name=name)
		self.root = FloatLayout()
		Window.size = View.screen_size
		self.root.canvas.add(
		Color(1.0, 1.0, 1.0))
		self.root.canvas.add(
		Rectangle(pos = (self.frame[0] * View.xratio,
		self.frame[1]*View.yratio),
		size = (frame[2] * View.xratio,
		frame[3] * View.yratio)))
		
	def add_subview(self, v):
		v.superview = self
		if v.name:
			self.rootdict[v.name] = v.kivyobject
		self.root.add_widget(v.kivyobject)
		
	def __getitem__(self, key):
		return self.rootdict[key]
		
	def close(self):
		if core_platform == 'android':
			sys.exit()
		else:
			Window.close()
			
	def present(self, style):
		#todo: screen size, style
		runTouchApp(self.root)
		
class Button(View):
	def __init__(self, frame=(0,0,100,100),
	title='',
	name='',
	font=('Helvetica', 20),
	action=None):
		super().__init__(frame=frame, name=name)
		self.kivyobject = (KivyButton(text=title,
		size_hint_y = None,
		size_hint_x = None,
		width = self.frame[2]* View.xratio,
		height = self.frame[3]* View.yratio,
		pos = (self.frame[0] * View.xratio,
		self.frame[1] * View.yratio),
		on_press = action))
		
class Label(View):
	def __init__(self, frame=(0,0,100,100),
	text='',
	alignment='',
	name='',
	font=('Helvetica', 20),
	text_color='blue'):
		super().__init__(frame=frame, name=name)
		label = KivyLabel(text=text,
		id=name,
		size_hint=(1.0, 1.9),
		halign="left",
		valign="bottom",
		pos = (self.frame[0] * View.xratio,
		self.frame[1] * View.yratio))
		#label.bind(size=label.setter('text_size'))
		self.kivyobject = (label)
		
class TextField(View):
	def __init__(self,
	frame=(0,0,100,100),
	text='',
	name='',
	font=('Helvetica', 20),
	alignment='',
	text_color='blue'):
																																								#action=None):
		super().__init__(frame=frame, name=name)
		self.kivyobject = (TextInput(text=text,
		size_hint_y = None,
		size_hint_x = None,
		height = self.frame[3]* View.yratio,
		width = self.frame[2]* View.xratio,
		multiline = True,
		pos = (self.frame[0] * View.xratio,
		self.frame[1] * View.yratio)))
			#on_press = action))
			
			
class ImageView(View):
	def __init__(self,
	frame=(0,0,100,100),
	name='',
	image=None):
		super().__init__(frame=frame, name=name)
		if image:
			image_source = image.source
		else:
			image_source = None
		self.kivyobject = (
		KivyImage(source=image_source,
		allow_stretch = True,
		size = (self.frame[2]* View.xratio,
		self.frame[3]* View.yratio),
		pos = (self.frame[0] * View.xratio,
		self.frame[1] * View.yratio)))
		
class Image(object):
	def __init__(self, source):
		self.source = source

