#
# Hydrogen is a lightweight GUI framework for Pythonista
#
# Hydrogen        - https://gist.github.com/BashedCrab/5924965
#
# HydrogenLayouts - https://gist.github.com/BashedCrab/6103019
#
# HydrogenDemo    - https://gist.github.com/BashedCrab/5953776
#

from scene import *

# Shape drawing functions used to draw components

def cylinder(x=0, y=0, w=0, h=0, r=0):
	rect(x + h / 2, y, w - h, h)
	ellipse(x, y, h, h)
	ellipse(x + w - h, y, h, h)
	
def rectangle(x=0, y=0, w=0, h=0, r=0):
	rect(x, y, w, h)
	
def round_rect(x=0, y=0, w=0, h=0, r=0):
	if(r <= 0):
		rect(x, y, w, h)
	elif(r >= h):
		cylinder(x, y, w, h)
	else:
		d = r * 2
		rect(x + r, y, w - d, h)
		rect(x, y + r, w, h - d)
		ellipse(x, y, d, d)
		ellipse(x, y + h - d, d, d)
		ellipse(x + w - d, y, d, d)
		ellipse(x + w - d, y + h - d, d, d)
		
def round_bottom_rect(x=0, y=0, w=0, h=0, r= 0):
	if(r <= 0):
		rect(x, y, w, h)
	elif(r >= h):
		cylinder(x, y, w, h)
	else:
		d = r * 2
		rect(x, y + r, w, h - r)
		rect(x + r, y, w - d, r)
		ellipse(x, y, d, d)
		ellipse(x + w - d, y, d, d)
		
def round_top_rect(x=0, y=0, w=0, h=0, r= 0):
	if(r <= 0):
		rect(x, y, w, h)
	elif(r >= h):
		cylinder(x, y, w, h)
	else:
		d = r * 2
		rect(x, y, w, h - r)
		rect(x + r, y + h - r, w - d, r)
		ellipse(x, y + h - d, d, d)
		ellipse(x + w - d, y + h - d, d, d)
		
def round_left_rect(x=0, y=0, w=0, h=0, r=0):
	if(r <= 0):
		rect(x, y, w, h)
	elif(r >= h):
		cylinder(x, y, w, h)
	else:
		d = r * 2
		rect(x, y + r, r, h - d)
		rect(x + r, y, w - r, h)
		ellipse(x, y, d, d)
		ellipse(x, y + h - d, d, d)
		
def round_right_rect(x=0, y=0, w=0, h=0, r=0):
	if(r <= 0):
		rect(x, y, w, h)
	elif(r >= h):
		cylinder(x, y, w, h)
	else:
		d = r * 2
		rect(x + w - r, y + r, r, h - d)
		rect(x, y, w - r, h)
		ellipse(x + w - d, y, d, d)
		ellipse(x + w - d, y + h - d, d, d)
		
# Default Look and Feel used within Hydrogen

HGreyLookAndFeel = {
                "Shape" : round_rect,
                "Foreground" : (0.00, 0.00, 0.00, 1.00),
                "Background" : (0.90, 0.90, 0.90, 1.00),
                "Border" : (0.50, 0.50, 0.50, 1.00),
                "Border Width" : 1,
                "Font" : 'AppleSDGothicNeo-Medium',
                "Font Size" : 16,
                "Edge Radius" : 6,
                "Disabled Foreground" : (0.40, 0.40, 0.40, 1.00),
                "Disabled Background" : (0.70, 0.70, 0.70, 1.00),
                "Disabled Border" : (0.40, 0.40, 0.40, 1.00),
                "Show Background" : True,
                "Show Border" : True,
                "Scene Background" : (0.80, 0.80, 0.80),
                "Button Foreground" : (0.00, 0.00, 0.00, 1.00),
                "Button Background" : (0.85, 0.85, 0.85, 1.00),
                "Button Selected" : (0.60, 0.60, 0.60, 1.00),
                "Image Foreground" : (1.00, 1.00, 1.00, 1.00),
                "Image Show Background" : False,
                "Image Show Border" : False,
                "Text Foreground" : (0.00, 0.00, 0.00, 1.00),
                "Text Show Background" : False,
                "Text Show Border" : False,
                "Progress Bar Shape" : cylinder,
                "Progress Bar Background" : (1.00, 1.00, 1.00, 1.00),
                "Progress Bar Foreground" : (0.00, 0.50, 1.00, 1.00),
                                                                "Slider Shape" : cylinder,
                "Slider Foreground" : (0.00, 0.50, 1.00, 1.00),
                "Slider Show Background" : True,
                "Slider Show Border" : True,
                "Switch Shape" : cylinder,
                "Switch Background On" : (0.00, 0.50, 1.00, 1.00),
                "Switch Background Off" : (1.00, 1.00, 1.00, 1.00),
}

LAF = HGreyLookAndFeel

# HInset used to for inset spacing in layouts

class HInset(object):
	def __init__(self, left=0, right=0, top=0, bottom=0):
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right
		
	def width(self):
		return self.left + self.right
		
	def height(self):
		return self.top + self.bottom
		
# Base HComponent class
# Parent class for all Hydrogen GUI Classes

class HComponent (object):
	def __init__(self):
		self.bounds = Rect(0, 0, 20, 100)
		self.preferred_size = None
		self.is_enabled = True
		self.is_visible = True
		self.owner = None
		self.id = None
		self.ignores_touches = False
		self.laf_prefix = ""
		self.laf_keys = ["Shape", "Background", "Foreground", "Border", "Border Width", "Show Border",
		"Show Background", "Disabled Foreground", "Disabled Background",
		"Disabled Border", "Edge Radius", "Font", "Font Size"]
		self.laf = {}
		self.laf_loaded = False
		self.touch_listeners = []
		
	# Gets called when the component is added a container (including the base scene)
	# The look and feel should already have been loaded so you can safely change position
	# or calculate sizes based on look and feel font sizes etc
	
	def setup(self):
		pass
		
	def load_lookandfeel(self):
		def get_laf_value(key):
			value = None
			try:
				value = LAF[self.laf_prefix + key]
			except KeyError:
				value = LAF[key]
			return value
			
		for key in self.laf_keys:
			self.laf[key] = get_laf_value(key)
		if(self.laf_loaded == False):
			self.laf_loaded = True
			size = self.get_preferred_size()
			self.bounds.w = size.w
			self.bounds.h = size.h
			
	# Methods enable the Layout system to know preferred sizes of components
	
	def get_preferred_size(self):
		if self.preferred_size is not None:
			return self.preferred_size
		else:
			return self.calculate_preferred_size()
			
	# This is the method to override to provide the layout with the preferred size of your custom component
	
	def calculate_preferred_size(self):
		return self.bounds.size()
		
	def get_screen_origin(self):
		if self.owner == None:
			return self.bounds.origin()
		else:
			x, y = self.bounds.origin().as_tuple()
			x_offset, y_offset = self.owner.get_screen_origin().as_tuple()
			x_screen = x + x_offset
			y_screen = y + y_offset
			return Point(x_screen, y_screen)
			
	def get_scene(self):
		if isinstance(self, HScene):
			return self
		elif self.owner == None:
			return None
		else:
			return self.owner.get_scene()
			
	def hit_test(self, x, y):
		if not self.is_visible:
			return None
		elif self.ignores_touches:
			return None
		elif not self.is_enabled:
			return None
		elif Point(x, y) in self.bounds:
			return self
		else:
			return None
			
	# Component drawing methods
	
	def set_border_fill(self):
		if(self.is_enabled):
			fill(*self.laf["Border"])
		else:
			fill(*self.laf["Disabled Border"])
			
	def set_background_fill(self):
		if(self.is_enabled):
			fill(*self.laf["Background"])
		else:
			fill(*self.laf["Disabled Background"])
			
	def set_foreground_fill(self):
		if(self.is_enabled):
			tint(*self.laf["Foreground"])
			fill(*self.laf["Foreground"])
		else:
			tint(*self.laf["Disabled Foreground"])
			fill(*self.laf["Disabled Foreground"])
			
	# Default draw border method should be fine for most custom components
	# Part of the new Look and Feel system
	
	def draw_border(self, x, y):
		if(self.laf["Show Border"]):
			self.set_border_fill()
			self.laf["Shape"](x, y, self.bounds.w, self.bounds.h, self.laf["Edge Radius"])
			
	# Default draw background method should be fine for most custom components
	# Part of the new Look and Feel system
	
	def draw_background(self, x, y):
		if(self.laf["Show Background"]):
			self.set_background_fill()
			if(self.laf["Show Border"]):
				self.laf["Shape"](x + self.laf["Border Width"], y + self.laf["Border Width"],
				self.bounds.w - self.laf["Border Width"] * 2,
				self.bounds.h - self.laf["Border Width"] * 2,
				self.laf["Edge Radius"] - self.laf["Border Width"])
			else:
				self.laf["Shape"](x, y, self.bounds.w, self.bounds.h, self.laf["Edge Radius"])
				
	# Preferred method to override for drawing your custom component.  Starting here means
	# the Look and Feel will take care of the Border and Background.  The bounds of the
	# component includes the border, so you will need to manually account for border width
	# and edge radius when drawing the contents of your control
	# The x,y parameters passed are the screen coordinates of the bottom left edge
	
	def draw_foreground(self, x, y):
		pass
		
	# Root method called to draw the Component.  Override this if you want your component
	# to be built from scratch, (potentially) outside the look and feel system
	# Component x,y values are relative to their container.  x_offset & y_offset need to be
	# added to the local x,y values to get screen coordinates for drawing the component
	
	def h_draw(self, x_offset, y_offset):
		x = self.bounds.x + x_offset
		y = self.bounds.y + y_offset
		no_stroke()
		self.draw_border(x, y)
		self.draw_background(x, y)
		self.draw_foreground(x, y)
		
	def h_touch_began(self, touch):
		for t in self.touch_listeners:
			t(self, "began", touch)
			
	def h_touch_moved(self, touch):
		for t in self.touch_listeners:
			t(self, "moved", touch)
			
	def h_touch_ended(self, touch):
		for t in self.touch_listeners:
			t(self, "ended", touch)
			
# Base class for any container component that contains child components
# Has enough functionality to be used as a basic panel as is.

class HContainer(HComponent):
	def __init__(self):
		HComponent.__init__(self)
		self.components = []
		self.layout = HLayout(self)
		self.insets = HInset()
		
	def load_lookandfeel(self):
		HComponent.load_lookandfeel(self)
		for c in self.components:
			c.load_lookandfeel()
		self.pack()
		
	def calculate_preferred_size(self):
		return self.layout.get_preferred_size()
		
	def add_component(self, comp, constraints=None):
		comp.load_lookandfeel()
		comp.setup()
		self.components.append(comp)
		comp.owner = self
		self.layout.add(comp, constraints)
		self.do_layout()
		
	def do_layout(self):
		self.layout.do_layout()
		for c in self.components:
			if isinstance(c, HContainer):
				c.do_layout()
				
	def pack(self):
		pref_size = self.get_preferred_size()
		self.bounds.w = pref_size.w
		self.bounds.h = pref_size.h
		self.do_layout()
		
	def draw_components(self, x_offset, y_offset):
		x = self.bounds.x + x_offset
		y = self.bounds.y + y_offset
		for c in self.components:
			if c.is_visible:
				c.h_draw(x, y)
				if isinstance(c, HContainer):
					c.draw_components(x, y)
					
	def hit_test(self, x, y):
		if(not self.is_visible):
			return None
		comp = None
		p = Point(x - self.bounds.x , y - self.bounds.y)
		for c in reversed(self.components):
			comp = c.hit_test(p.x, p.y)
			if comp <> None:
				break
		if comp == None:
			return HComponent.hit_test(self, x, y)
		else:
			return comp
			
# Base Image component

class HImage(HComponent):
	def __init__(self, img = None, img_size = None):
		HComponent.__init__(self)
		self._img = img
		self._img_size = img_size
		self.laf_prefix = "Image "
		self.stretch = False
		self.ignores_touches = True
		
	def set_image(self, img, img_size):
		self._img = img
		self._img_size = img_size
		
	def calculate_preferred_size(self):
		if(self.laf_loaded == False):
			return self.bounds.size()
		if(self._img_size == None):
			return self.bounds.size()
		pad = self.laf["Edge Radius"] * 2
		if self.laf["Show Border"]:
			pad += self.laf["Border Width"]
		return Size(self._img_size.w + pad, self._img_size.h + pad)
		
	def draw_foreground(self, x, y):
		self.set_foreground_fill()
		if(self._img <> None):
			if(self.stretch):
				image(self._img, x, y, self.bounds.w, self.bounds.h)
			else:
				image(self._img, x + (self.bounds.w - self._img_size.w) / 2,
				y + (self.bounds.h - self._img_size.h) / 2, self._img_size.w, self._img_size.h)
				
# Text component - takes the given text and creates an image for the HImage subclass to display

class HText(HImage):
	def __init__(self, txt="Text"):
		HImage.__init__(self)
		self._text = txt
		self.laf_prefix = "Text "
		
	def set_text(self, t):
		self._text = t
		self._img = None
		
	def load_lookandfeel(self):
		self._img = None
		HImage.load_lookandfeel(self)
		
	def calculate_preferred_size(self):
		if(self.laf_loaded == False):
			return self.bounds.size()
		elif(self._text == None):
			return self.bounds.size()
		else:
			self._img, self._img_size = render_text(self._text, self.laf["Font"], self.laf["Font Size"])
			return HImage.calculate_preferred_size(self)
			
	def draw_foreground(self, x, y):
		if(self._text <> None and self._img == None):
			self._img, self._img_size = render_text(self._text, self.laf["Font"], self.laf["Font Size"])
		HImage.draw_foreground(self, x, y)
		
		
# Basic button Component
# Take the basic functionality of the HText component and make it click
# Buttons can also take images, since HImage is the super class of both
# HText and HButton

class HButton(HText):
	def __init__(self, txt="Button"):
		HText.__init__(self, txt)
		self.laf_prefix = "Button "
		self.laf_keys.append("Selected")
		self.is_selected = False
		self.click_listeners = []
		self.ignores_touches = False
		
	def draw_background(self, x, y):
		if(self.laf["Show Background"]):
			if(self.is_selected):
				_background = self.laf["Background"]
				self.laf["Background"] = self.laf["Selected"]
				HComponent.draw_background(self, x, y)
				self.laf["Background"] = _background
			else:
				HComponent.draw_background(self, x, y)
				
	def h_touch_began(self, touch):
		if(self.is_enabled):
			self.is_selected = True
			
	def h_touch_ended(self, touch):
		if(self.is_enabled):
			self.is_selected = False
			screen_x, screen_y = self.get_screen_origin().as_tuple()
			screen_bounds = Rect(screen_x, screen_y, self.bounds.w, self.bounds.h)
			if(touch.location in screen_bounds):
				for click in self.click_listeners:
					click(self)
					
# Progress bar to display visual progress on screen

class HProgressBar(HComponent):
	def __init__(self):
		HComponent.__init__(self)
		self.preferred_size = Size(150, 15)
		self.laf_prefix = "Progress Bar "
		self.value = 0.0
		
	# TODO: finish implementing new look and feel system - will draw slightly glitchy if
	# shape is not a cylinder
	
	def draw_foreground(self, x, y):
		# If value 0 then no progress to be drawn
		if(self.value == 0):
			return
		# Setup local coords inside border
		w = self.bounds.w
		h = self.bounds.h
		if(self.laf["Show Border"]):
			w = w - (self.laf["Border Width"] * 2)
			h = h - (self.laf["Border Width"] * 2)
			x = x + self.laf["Border Width"]
			y = y + self.laf["Border Width"]
		pixel_progress = w * self.value
		self.set_foreground_fill()
		if(self.value >= 1.0):
			self.laf["Shape"](x, y, w, h, self.laf["Edge Radius"] - self.laf["Border Width"])
			return
		self.laf["Shape"](x, y, h, h, self.laf["Edge Radius"] - self.laf["Border Width"])
		if(pixel_progress <= (h / 2)):
			self.set_background_fill()
			rect(x + (h / 2), y, h, h)
		elif(pixel_progress <= h):
			rect(x + (h / 2), y, h / 2, h)
			self.set_background_fill()
			blank = h - pixel_progress
			rect(x + h - blank, y, h, h)
		else:
			if(pixel_progress > w - (h / 2)): pixel_progress = w - (h / 2)
			rect(x + (h / 2), y, pixel_progress - (h / 2), h)
			
# Slider component to visually control the output of a value.
# HSlider.value varies from 0.0 at minimum to 1.0 at maximum

class HSlider(HContainer):
	def __init__(self):
		HContainer.__init__(self)
		self.preferred_size = Size(150, 25)
		self.laf_prefix = "Slider "
		self.progress_bar = HProgressBar()
		self.progress_bar.ignores_touches = True
		self.button = HComponent()
		self.button.laf_prefix = "Slider "
		self.button.ignores_touches = True
		self.add_component(self.progress_bar)
		self.add_component(self.button)
		self.value = 0.0
		self.change_listeners = []
		
	def draw_foreground(self, x, y):
		# This is just a convenient entry point to (re)locate the child components relative to ourselves
		r = self.bounds.h / 4
		self.progress_bar.value = self.value
		self.progress_bar.bounds.w = self.bounds.w - (2 * r)
		self.progress_bar.bounds.h = self.bounds.h / 2
		self.progress_bar.bounds.x = r
		self.progress_bar.bounds.y = r
		self.button.bounds.h = self.bounds.h
		self.button.bounds.w = self.bounds.h
		self.button.bounds.x = ((self.bounds.w - self.bounds.h) * self.value)
		self.button.bounds.y = 0
		
	def value_changed(self):
		for change in self.change_listeners:
			change(self)
			
	def h_touch_moved(self, touch):
		self.value  = self.value  + ((touch.location.x - touch.prev_location.x) / (self.bounds.w * 1.0))
		if(self.value > 1.0): self.value = 1.0
		elif(self.value < 0.0): self.value = 0.0
		self.value_changed()
		
# Switch component for a binary on/off selection
# HSwitch.value will be 0.0 for off and 1.0 on

class HSwitch(HContainer):
	def __init__(self):
		HContainer.__init__(self)
		self.preferred_size = Size(60, 25)
		self.laf_prefix = "Switch "
		self.laf_keys.append("Background On")
		self.laf_keys.append("Background Off")
		self.button = HComponent()
		self.button.ignores_touches = True
		self.button.laf_prefix = "Switch "
		self.add_component(self.button)
		self.is_selected = False
		self.value = 0.0
		self.change_listeners = []
		
	def set_background_fill(self):
		if(self.is_enabled == False):
			fill(*self.laf["Disabled Background"])
		elif(self.is_selected):
			fill(*self.laf["Background On"])
		else:
			fill(*self.laf["Background Off"])
			
	def draw_foreground(self, x, y):
		self.button.bounds.h = self.bounds.h
		self.button.bounds.w = self.bounds.h
		self.button.bounds.y = 0
		x_add = 0
		if(self.is_selected):
			x_add = (self.bounds.w - self.bounds.h)
		self.button.bounds.x = x_add
		
	def change_selected(self):
		self.is_selected = not self.is_selected
		for change in self.change_listeners:
			change(self)
			
	def h_touch_moved(self, touch):
		self.value  = self.value  + ((touch.location.x - touch.prev_location.x) / (self.bounds.w * 1.0))
		if(self.value > 0.5 and self.is_selected == False):
			self.value = 1.0
			self.change_selected()
		elif(self.value < 0.5 and self.is_selected == True):
			self.value = 0.0
			self.change_selected()
			
# Base layout class for developing custom Layout Managers

class HLayout(object):
	def __init__(self, container):
		self.container = container
		self.pad = HInset()
		
	# Only need to override this if your layout does something with constraints
	def add(self, comp, constraint):
		pass
		
	def do_layout(self):
		pass
		
	def get_preferred_size(self):
		return self.container.bounds.size()
		
# Base Scene class.
# Your Hydrogen application will need to subclass this and add your top level components to it.
# The preferred method is to let the scene provide the background only and use the components
# for everything else.  If you do choose to override more than just the HScene.setup() method
# be cautious, as the HScene is the entry point for all touch events, and calls to redraw the
# the scene.

class HScene (Scene, HContainer):
	def __init__(self):
		Scene.__init__(self)
		HContainer.__init__(self)
		self.laf_prefix = "Scene "
		self.touch_map = {}
		self.load_lookandfeel()
		
	def draw(self):
		self.h_draw(0, 0)
		self.draw_components(0, 0)
		
	def draw_border(self, x, y):
		# Overriden to prevent a border around the entire scene
		pass
		
	def draw_background(self, x, y):
		background(*self.laf["Background"])
		
	# Unless your app is completely component based, draw_foreground is where you will put all the drawing
	# routines you would otherwise have put in your Scene.draw() method
	def draw_foreground(self, x, y):
		pass
		
	def touch_began(self, touch):
		comp = None
		for c in reversed(self.components):
			comp = c.hit_test(touch.location.x, touch.location.y)
			if comp <> None:
				break
		if comp == None:
			comp = self
		self.touch_map[touch.touch_id] = comp
		comp.h_touch_began(touch)
		
	def touch_moved(self, touch):
		comp = self.touch_map[touch.touch_id]
		comp.h_touch_moved(touch)
		
	def touch_ended(self, touch):
		comp = self.touch_map[touch.touch_id]
		comp.h_touch_ended(touch)
		del self.touch_map[touch.touch_id]

