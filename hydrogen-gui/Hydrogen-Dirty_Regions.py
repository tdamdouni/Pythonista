from __future__ import print_function
#
# Hydrogen experiment to use "dirty region rendering" and improve rendering large GUIs
#
# Will not work with Pythonista in it's current form as scene drawing clears the frame buffer
#
# Lightweight GUI framework for Pythonista
#
# Get the the Demo scene here:
#
# https://gist.github.com/BashedCrab/5953776
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
                "HScene Background" : (0.80, 0.80, 0.80),
                "HButton Foreground" : (0.00, 0.00, 0.00, 1.00),
                "HButton Background" : (0.85, 0.85, 0.85, 1.00),
                "HButton Selected" : (0.60, 0.60, 0.60, 1.00),
                "HImage Foreground" : (1.00, 1.00, 1.00, 1.00),
                "HImage Show Background" : False,
                "HImage Show Border" : False,
                "HText Foreground" : (0.00, 0.00, 0.00, 1.00),
                "HText Show Background" : False,
                "HText Show Border" : False,
                "HProgressBar Shape" : cylinder,
                "HProgressBar Background" : (1.00, 1.00, 1.00, 1.00),
                "HProgressBar Foreground" : (0.00, 0.50, 1.00, 1.00),
                                                                "HSlider Shape" : cylinder,
                "HSlider Foreground" : (0.00, 0.50, 1.00, 1.00),
                "HSlider Show Background" : True,
                "HSlider Show Border" : True,
                "HSwitch Shape" : cylinder,
                "HSwitch Background On" : (0.00, 0.50, 1.00, 1.00),
                "HSwitch Background Off" : (1.00, 1.00, 1.00, 1.00),
}

LAF = HGreyLookAndFeel
LAF_SEPARATOR = ' '
NOT_DRAWN = Rect()

# Base HComponent class
# Parent class for all Hydrogen GUI Classes

class HComponent (object):
	def __init__(self):
		self.bounds = Rect(0, 0, 36, 36)
		self.preferred_size = None
		self.is_enabled = True
		self.is_visible = True
		self.owner = None
		self.id = None
		self.ignores_touches = False
		self.touch_listeners = []
		self.last_drawn_bounds = NOT_DRAWN
		self.is_dirty = False
		self.needs_redraw = True
		self.laf = {}
		self.laf_loaded = False
		self.laf_prefix = ""
		self.laf_keys = ["Shape", "Background", "Foreground", "Border", "Border Width",
		"Show Border", "Show Background", "Disabled Foreground",
		"Disabled Background", "Disabled Border", "Edge Radius",
		"Font", "Font Size"]
		
	def set_origin(self, x, y):
		self.bounds = Rect(x, y, self.bounds.w, self.bounds.h)
		self.is_dirty = True
		self.needs_redraw = True
		
	def set_size(self, w, h):
		self.bounds = Rect(self.bounds.x, self.bounds.y, w, h)
		self.is_dirty = True
		self.needs_redraw = True
		
	def set_bounds(self, x, y, w, h):
		self.bounds = Rect(x, y, w, h)
		self.is_dirty = True
		self.needs_redraw = True
		
	def set_preferred_size(self, preferred_size):
		self.preferred_size = preferred_size
		
	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled
		self.needs_redraw = True
		
	def set_visible(self, is_visible):
		self.is_visible = is_visible
		if(self.is_visible):
			self.needs_redraw = True
		else:
			self.is_dirty = True
			
	def set_laf_property(self, key, value):
		self.laf[key] = value
		self.needs_redraw = True
		
	def prefill_dirty_regions(self, dirty_regions):
		if self.is_dirty:
			dirty_regions.append(self.last_drawn_bounds)
			
	# Gets called when the component is added a container (including the base scene)
	# The look and feel should already have been loaded so you can safely change position
	# or calculate sizes based on look and feel font sizes etc
	
	def setup(self):
		pass
		
	def load_lookandfeel(self):
		def get_laf_value(key):
			value = None
			class_name = self.__class__.__name__
			try:
				value = LAF[self.laf_prefix + LAF_SEPARATOR + key]
			except KeyError:
				pass
			if value is None:
				try:
					value = LAF[class_name + LAF_SEPARATOR + key]
				except KeyError:
					pass
			if value is None:
				try:
					value = LAF[key]
				except KeyError:
					print(self.__class__.__name__ + " cannot find value for laf[" + key + "]")
					pass
			return value
			
		for key in self.laf_keys:
			self.set_laf_property(key, get_laf_value(key))
		if(self.laf_loaded == False):
			self.laf_loaded = True
			size = self.get_preferred_size()
			self.set_size(size.w, size.h)
			
	# Methods to enable the Layout system to know preferred sizes of components
	
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
	
	def h_draw(self, x, y, dirty_regions):
		no_stroke()
		self.draw_border(x, y)
		self.draw_background(x, y)
		self.draw_foreground(x, y)
		
	def in_dirty_regions(self, dirty_regions):
		is_in = False
		for region in dirty_regions:
			if self.bounds in region:
				is_in = True
				break
		return is_in
		
	def intersects_dirty_regions(self, dirty_regions):
		intersects = False
		for region in dirty_regions:
			if self.bounds.intersects(region):
				intersects = True
				break
		return intersects
		
	def redraw_check(self, x_offset, y_offset, dirty_regions):
		if not self.is_visible:
			if self.is_dirty:
				self.last_drawn_bounds = NOT_DRAWN
				self.is_dirty = False
		elif self.needs_redraw:
			print(self.__class__.__name__ + " needs_redraw, frame: " + str(self.get_scene().frame_no))
			self.h_draw(x_offset + self.bounds.x, y_offset + self.bounds.y, dirty_regions)
			self.last_drawn_bounds = self.bounds
			self.needs_redraw = False
			self.is_dirty = False
			dirty_regions.append(self.bounds)
		elif self.in_dirty_regions(dirty_regions):
			print(self.__class__.__name__ + " in_dirty_regions, frame: " + str(self.get_scene().frame_no))
			self.h_draw(x_offset + self.bounds.x, y_offset + self.bounds.y, dirty_regions)
			self.last_drawn_bounds = self.bounds
			self.needs_redraw = False
			self.is_dirty = False
		elif self.intersects_dirty_regions(dirty_regions):
			print(self.__class__.__name__ + " intersects_dirty_regions, frame: " + str(self.get_scene().frame_no))
			self.h_draw(x_offset + self.bounds.x, y_offset + self.bounds.y, dirty_regions)
			self.last_drawn_bounds = self.bounds
			self.needs_redraw = False
			self.is_dirty = False
			dirty_regions.append(self.bounds)
			
	# Touch handlers
	
	def h_touch_began(self, touch):
		for t in self.touch_listeners:
			t(self, "began", touch)
			
	def h_touch_moved(self, touch):
		for t in self.touch_listeners:
			t(self, "moved", touch)
			
	def h_touch_ended(self, touch):
		for t in self.touch_listeners:
			t(self, "ended", touch)
			
			
class HContainer(HComponent):
	def __init__(self):
		HComponent.__init__(self)
		self.laf_prefix = "HContainer"
		self.components = []
		self.layout = HLayout(self)
		self.insets = HInset()
		
	def calculate_preferred_size(self):
		return self.layout.get_preferred_size()
		
	def add_component(self, comp, constraints=None):
		comp.owner = self
		if not comp.laf_loaded:
			comp.load_lookandfeel()
			comp.setup()
		self.components.append(comp)
		self.layout.add(comp, constraints)
		self.do_layout()
		self.needs_redraw = True
		
	def prefill_dirty_regions(self, dirty_regions):
		if self.is_dirty:
			dirty_regions.append(self.last_drawn_bounds)
		else:
			for comp in self.components:
				comp.prefill_dirty_regions(dirty_regions)
				
	def do_layout(self):
		self.layout.do_layout()
		for c in self.components:
			if isinstance(c, HContainer):
				c.do_layout()
				
	def pack(self):
		w, h = self.get_preferred_size()
		self.set_size(w, h)
		self.do_layout()
		
	def redraw_components_check(self, x_offset, y_offset, dirty_regions):
		x = self.bounds.x + x_offset
		y = self.bounds.y + y_offset
		for comp in self.components:
			comp.redraw_check(x, y, dirty_regions)
			if isinstance(comp, HContainer):
				comp.redraw_components_check(x, y, dirty_regions)
				
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
		self.laf_prefix = "HImage"
		self.stretch = False
		self.ignores_touches = True
		
	def set_image(self, img, img_size):
		self._img = img
		self._img_size = img_size
		self.needs_redraw = True
		
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
		self.needs_redraw = True
		
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
		self.laf_prefix = "HButton "
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
				
	def set_selected(self, selected):
		if selected <> self.is_selected:
			self.is_selected = selected
			self.needs_redraw = True
			
	def h_touch_began(self, touch):
		if(self.is_enabled):
			self.set_selected(True)
			
	def h_touch_ended(self, touch):
		if(self.is_enabled):
			self.set_selected(False)
			screen_x, screen_y = self.get_screen_origin().as_tuple()
			screen_bounds = Rect(screen_x, screen_y, self.bounds.w, self.bounds.h)
			if(touch.location in screen_bounds):
				for click in self.click_listeners:
					click(self)
					
					
################
################
################

class HLayout(object):
	def __init__(self, container):
		self.container = container
		self.pad = HInset()
		
	def add(self, comp, constraint):
		pass
		
	def do_layout(self):
		pass
		
	def get_preferred_size(self):
		return self.container.bounds.size()
		
################
################
################

# HInset used to for inset spacing in components and layouts

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
		
################
################
################

class HScene (Scene, HContainer):
	def __init__(self):
		Scene.__init__(self)
		HContainer.__init__(self)
		self.touch_map = {}
		self.needs_redraw = True
		self.laf_prefix = "HScene"
		self.load_lookandfeel()
		self.frame_no = 0
		
	def setup(self):
		pass
		
	def draw(self):
		dirty_regions = []
		self.prefill_dirty_regions(dirty_regions)
		if len(dirty_regions) > 0:
			print(dirty_regions)
		self.redraw_check(0, 0, dirty_regions)
		self.redraw_components_check(0, 0, dirty_regions)
		self.frame_no += 1
		
	def h_draw(self, x_offset, y_offset, dirty_regions):
		if self.needs_redraw:
			background(*self.laf["Background"])
		else:
			for region in dirty_regions:
				fill(*self.laf["Background"])
				rect(region.x, region.y, region.w, region.h)
				
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
		
		
class Demo(HScene):
	def setup(self):
		c = HButton()
		c.set_origin(500, 300)
		self.add_component(c)
		
run(Demo())

