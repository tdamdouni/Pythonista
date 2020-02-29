from __future__ import print_function
import os
import sys

sys.path += [os.path.join(
                os.path.dirname(
                   os.path.abspath(__file__)), 'lib')]

# Pythonista Modules
import console
from scene import *
import editor

from glob import glob
from time import time
from itertools import chain

#import Scene_Widgets as

class MyScene (Scene):
	def __init__(self, fs, toolHeight = 40):
		super(MyScene, self).__init__()
		self.fs = fs
		self.toolHeight = toolHeight
		self.tb_height = 30
	def setup(self):
		# This will be called before the first frame is drawn.
		# Set up the root layer and one other layer:
		self.root_layer = Layer(self.bounds)
		tint(0,0,0)
		self.scroller = Scroll_Layer(Rect(0,0,
		self.size.w,
		self.size.h-self.toolHeight-self.tb_height),
		Layer())
		self.opendir('.')
		self.upbutton = Button_Layer(Rect(self.toolHeight,
		self.bounds.top()-self.toolHeight,
		self.toolHeight,self.toolHeight),
		'Typicons48_Up',
		Color(1,1,1,0),
		Color(.5,.5,.5,.5),
		self.updir)
		self.homebutton = Button_Layer(Rect(0,
		self.bounds.top()-self.toolHeight,
		self.toolHeight,self.toolHeight),
		'Typicons48_Home',
		Color(1,1,1,0),
		Color(.5,.5,.5,.5),
		self.home)
#               self.btn_add = Button_Layer(Rect(self.toolHeight*2,
#                                               self.bounds.top()-self.toolHeight,
#                                               self.toolHeight,self.toolHeight),
#                                          'Typicons48_Plus',
#                                          Color(1,1,1,0),
#                                          Color(.5,.5,.5,.5),
#                                          self.adddir)
		self.btn_remove = Button_Layer(Rect(self.bounds.right() -self.toolHeight*3,
		self.bounds.top()-self.toolHeight,
		self.toolHeight,self.toolHeight),
		'Typicons48_Trash',
		Color(1,1,1,0),
		Color(.5,.5,.5,.5),
		self.remove)
		self.toolbar1 = Layer(Rect(0,self.bounds.top()-self.toolHeight,
		self.size.w, self.toolHeight/2))
		self.toolbar2 = Layer(Rect(0,self.bounds.top()-self.toolHeight/2,
		self.size.w, self.toolHeight/2))
		self.textbox = Layer(Rect(0,self.bounds.top() - self.toolHeight - self.tb_height,
		self.size.w, self.tb_height))
		self.textbox.background = Color(1,1,1)
		self.textbox.stroke=Color(0,0,0)
		self.textbox.stroke_weight = 1
		self.toolbar1.background = Color(0.80, 0.80, 0.80)
		self.toolbar2.background = Color(0.90, 0.90, 0.90)
		self.root_layer.add_layer(self.scroller)
		self.root_layer.add_layer(self.toolbar1)
		self.root_layer.add_layer(self.toolbar2)
		self.root_layer.add_layer(self.textbox)
		self.root_layer.add_layer(self.upbutton)
		self.root_layer.add_layer(self.homebutton)
		self.root_layer.add_layer(self.btn_remove)
#               self.root_layer.add_layer(self.btn_add)

		self.touch_start_t = -1
		self.touch_start = Touch(0,0,0,0,0)
		self.hold_timeout = 0
		
		#self.root_layer.add_layer(TextList_Layer(self.bounds, files))
		
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(1, 1, 1)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		tint(0.30, 0.30, 0.30)
		text(self.fs.getcwd(), 'HelveticaNeue-Medium', 16,
		5, self.size.h - self.toolHeight - self.tb_height/2, 6)
		
	def touch_began(self, touch):
		self.touch_start = touch
		self.touch_start_t = self.t
		
	def opendir(self, path):
		self.fs.chdir(path)
		list = List_Layer(300,
		self.fs.getdirs() + self.fs.getfiles(),
		onDblClick = self.openSelected)
		for item in list.sublayers:
			absolute_path = os.path.join(self.fs.getcwd(),item.text)
			ext = os.path.splitext(absolute_path)[1]
			
			if self.fs.isdir(absolute_path):
				try:
					os.listdir(absolute_path) # see if we can open it
					item.setIcon('Pouch')
				except:
					item.setIcon('Lock_2')
			elif ext in ['.png','.jpg']:
				item.setIcon('Camera')
			else:
				item.setIcon('Page_Facing_Up')
		self.scroller.setLayer(list)
		
		
	def home(self):
		self.opendir(self.fs.home)
		
	def updir(self):
		self.opendir('..')
		
	def openSelected(self):
		if self.scroller.sublayer.selected:
			filename = self.scroller.sublayer.selected.text
			absolute_path = os.path.join(self.fs.cwd,filename)
			relative_path = os.path.relpath(absolute_path)
			ext = os.path.splitext(filename)[1]
			
			if self.fs.isdir(absolute_path):
				self.opendir(filename)
			# cant open anything below the documents folder
			elif ext in ['.png','.jpg']:
				console.show_image(absolute_path)
				sys.exit()
			elif relative_path[:2] != '..':
				if ext == '.py':
					editor.open_file(relative_path)
					sys.exit()
				else:
					show_tempfile(absolute_path)
			else:
				show_tempfile(absolute_path)
	def remove(self):
		if self.scroller.sublayer.selected:
			filename = self.scroller.sublayer.selected.text
			absolute_path = os.path.join(self.fs.cwd,filename)
			
			os.remove(absolute_path)
			self.opendir('.')
	def adddir(self):
		pass
		#path = console.input_alert('Folder name', 'Folder name')
		
def show_tempfile(absolute_path):
	infile = open(absolute_path,'r')
	contents = infile.read()
	try:
		# make sure the encoding wont break Pythonista
		contents.decode('ascii')
	except:
		print('Unknown encoding in file:\n\t',absolute_path)
		sys.exit()
	infile.close()
	
	writefile = open('temp.py','w')
	writefile.write(contents)
	writefile.close()
	
	editor.open_file('temp.py')
	
	sys.exit()
	
class Base_Layer (Layer):
	def __init__(self, frame):
		super(Base_Layer, self).__init__(frame)
		
	def touch_began(self, touch):
		if self.superlayer:
			self.superlayer.touch_began(touch)
			
	def touch_ended(self, touch):
		if self.superlayer:
			self.superlayer.touch_ended(touch)
			
	def touch_moved(self, touch):
		if self.superlayer:
			self.superlayer.touch_moved(touch)
			
# makes a scrollable window
class Scroll_Layer (Layer):
	def __init__(self, frame, sublayer):
		super(Scroll_Layer, self).__init__(frame)
		
		self.stroke=Color(0,0,0)
		self.stroke_weight = 1
		self.sublayer = None
		self.setLayer(sublayer)
		
	def scrollTo(self, y):
		if y < 0:
			self.scrollTo(0)
		elif y > self.scroll_range:
			self.scrollTo(self.scroll_range)
		else:
			self.scroll_pos = y
			self.sublayer.frame.y = self.frame.h -self.sublayer.frame.h + y
			
	def scrollBy(self, dy):
		self.scrollTo(self.scroll_pos + dy)
		
	def touch_moved(self, touch):
		self.scrollBy((touch.location.y - touch.prev_location.y))
		
	def setLayer(self, sublayer):
		if self.sublayer:
			self.sublayer.remove_layer()
		self.sublayer = sublayer
		self.add_layer(self.sublayer)
		# zero when upper left corners match
		scroll_range = self.sublayer.frame.h - self.frame.h
		if scroll_range < 0: scroll_range = 0
		self.scroll_range = scroll_range
		self.scroll_pos = scroll_range
		self.scrollTo(0)
		
		
class List_Layer (Layer):
	def __init__(self, width, olist, spacing = 40,
	onDblClick = None, multiSelect = False):
		frame = Rect(0, 0, width, spacing * len(olist))
		super(List_Layer, self).__init__(frame)
		
		self.spacing = spacing
		self.multiSelect = multiSelect
		self.selected = None
		
		for i in range(len(olist)):
			item = ListItem_Layer((len(olist)-i-1)*spacing,
			Size(300,spacing),
			olist[i], onDblClick = onDblClick)
			self.add_layer(item)
			
	def select(self, select_item):
		if not self.multiSelect:
			if self.selected:
				self.selected.deselect()
			self.selected = select_item
		else:
			pass
			
	def touch_moved(self, touch):
		self.superlayer.touch_moved(touch)
		
class ListItem_Layer(Layer):
	def __init__(self, y, # vertical position relative to superlayer
	size,
	text,
	value = 0,
	padding = 3, # just applied to horizontal atm
	alignment = 4, #TODO: support
	icon = None,
	onClick = None,
	onDblClick = None):
		super(ListItem_Layer, self).__init__(Rect(0,y,size.w,size.h))
		
		# store initialization info
		self.value = value
		self.padding = padding
		self.alignment = alignment
		self.onClick = onClick
		self.onDblClick = onDblClick
		
		self.text_layer = None
		self.setText(text)
		
		self.setIcon(icon)
		
		# set click flags
		self.last_touch = 0
		self.last_click = 0
		
		# selection status
		self.selected = False
		
	def setText(self, text):
		if self.text_layer: # remove old text if we've set it
			self.text_layer.remove_layer()
		self.text = text
		# render and add text
		text_image = render_text(text)
		size = text_image[1]
		self.text_layer = Layer(Rect(x = self.padding,
		y = self.frame.h/2 - size.h/2,
		w = size.w,
		h = size.h))
		self.text_layer.tint = Color(0,0,0)
		self.text_layer.image = text_image[0]
		self.text_layer.ignores_touches = True
		
		self.add_layer(self.text_layer)
		
	def setIcon(self, icon):
		if icon:
			if self.icon_layer:
				self.icon_layer.remove_layer()
			icon_size = self.frame.h - self.padding/2
			# make room for the icon
			if self.text_layer.frame.x < icon_size:
				self.text_layer.frame.x += icon_size + self.padding
			self.icon_layer = Layer(Rect(x = self.padding,
			y = self.padding,
			w = icon_size,
			h = icon_size))
			self.icon_layer.image = icon
			self.icon_layer.ignores_touches = True
			
			self.add_layer(self.icon_layer)
		else:
			self.icon_layer = None
			
			
	def touch_began(self, touch):
		self.last_touch = time()
		self.background = Color(0.90, 0.90, 0.90)
		
	def touch_moved(self, touch):
		self.last_touch = 0 # cancel click
		self.superlayer.touch_moved(touch) # pass it up the line
		
	def touch_ended(self, touch):
		if time() - self.last_touch < 0.2:
			# click
			if time() - self.last_click < 0.5 and self.onDblClick:
				# double click
				self.onDblClick()
			elif self.onClick:
				self.onClick()
			self.last_click = time()
			if not self.selected:
				self.superlayer.select(self)
			self.select()
		else:
			self.deselect()
			
	def select(self):
		self.selected = True
		self.background = Color(0.40, 0.80, 1.00)
		
		
	def deselect(self):
		self.selected = False
		self.background = Color(1,1,1)
		self.last_touch = 0
		self.last_click = 0
		
class Button_Layer (Layer):
	def __init__(self, frame, image, color_up, color_down, onClick = None):
		super(Button_Layer, self).__init__(frame)
#               self.stroke=Color(0,0,0)
#               self.stroke_weight = 1
		self.onClick = onClick
		self.image = image
		self.color_up = color_up
		self.color_down = color_down
		self.tint = Color(0,0,0)
		self.background = self.color_up
		self.depressed = False
		
		self.last_touch = 0
		
	def touch_began(self, touch):
		self.background = self.color_down
		self.depressed = True
		self.last_touch = time()
		
	def touch_moved(self, touch):
		self.depressed = False # cancel click
		
	def touch_ended(self, touch):
		if self.depressed and self.onClick:
			self.onClick()
		self.background = self.color_up
		self.depressed = False
		
class filesystem:
	def __init__(self, cwd ='.'):
		self.cwd = cwd
		self.chdir(cwd)
		self.home = self.cwd
		
	def chdir(self,path):
		# see if its an absolute path
		if path.startswith('/'):
			self.cwd = path
		# it's probably a relative path,
		# let's append cwd and let os.path do its magic
		else:
			self.cwd = os.path.abspath(os.path.join(self.cwd,path))
			
		entries = os.listdir(self.cwd)
		self.dirs = []
		self.files = []
		for entry in entries:
			if os.path.isdir(entry):
				self.dirs.append(entry)
			else:
				self.files.append(entry)
				
	def getcwd(self):
		return self.cwd
		
	def getdirs(self):
		return self.dirs
		
	def getfiles(self):
		return self.files
		
	def listfile(self):
		return
		
	def isdir(self, path):
		return os.path.isdir(path)
		
	def isfile(self, path):
		return os.path.isfile(path)
		
run(MyScene(filesystem()))

