# @ui
# https://gist.github.com/BashedCrab/6103019
#
# Hydrogen is a lightweight GUI framework for Pythonista
#
# Hydrogen        - https://gist.github.com/BashedCrab/5924965
#
# HydrogenLayouts - https://gist.github.com/BashedCrab/6103019
#
# HydrogenDemo    - https://gist.github.com/BashedCrab/5953776
#

from Hydrogen import HLayout
from scene import Size

# Column Layout places all components in a vertical column.
# All components get their preferred height.  Width can be preferred or fill
# the container
	
class HColumnLayout(HLayout):
	def __init__(self, container):
		HLayout.__init__(self, container)
		self.fill_width = True
	
	def do_layout(self):
		layoutSize = self.container.bounds.size()
		width = layoutSize.w - (self.container.insets.width() + self.pad.width())
		top = self.container.bounds.h - (self.container.insets.top + self.pad.top)
		left = self.container.insets.left + self.pad.left
		bottom = self.container.bounds.x + self.container.insets.bottom + self.pad.bottom
		for c in self.container.components:
			pref_size = c.get_preferred_size()
			c.bounds.h = pref_size.h
			if(pref_size.h > top - bottom):
				c.bounds.y = bottom
			else:
				c.bounds.y = top - c.bounds.h
			top = c.bounds.y - self.pad.height()
			if(self.fill_width):
				c.bounds.w = width
				c.bounds.x = left
			else:
				c.bounds.w = min(c.get_preferred_size().w, width)
				c.bounds.x = left + ((width - c.bounds.w) / 2)
			
	def get_preferred_size(self):
		w = 0
		h = 0
		for c in self.container.components:
			width, height = c.get_preferred_size().as_tuple()
			w = max(w, width)
			h += height + self.pad.height()
		w += self.container.insets.width()
		h += self.container.insets.height()
		return Size(w, h)
		
# BarLayout is meant to arrange 3 components on a title bar or status bar.
# Components can be aligned to the left edge, right edge or centred.
		
class HBarLayout(HLayout):
	def __init__(self, container):
		HLayout.__init__(self, container)
		self.comp_dict = {}

	def add(self, comp, constraint):
		self.comp_dict[constraint] = comp
			
	def do_layout(self):
		layoutSize = self.container.bounds.size()
		left = self.container.insets.left + self.pad.left
		right = layoutSize.w - (self.container.insets.right + self.pad.right)
		bottom = self.container.insets.bottom + self.pad.bottom
		top = layoutSize.h - (self.container.insets.top + self.pad.top)
		try:
			comp = self.comp_dict['left']
			pref_size = comp.get_preferred_size()
			comp.bounds.x = left
			comp.bounds.y = bottom
			comp.bounds.w = pref_size.w
			comp.bounds.h = top - bottom
			left += comp.bounds.w + self.pad.width()
		except KeyError:
			pass
		try:
			comp = self.comp_dict['right']
			pref_size = comp.get_preferred_size()
			comp.bounds.x = right - comp.bounds.w
			comp.bounds.y = bottom
			comp.bounds.w = pref_size.w
			comp.bounds.h = top - bottom
			right -= (comp.bounds.w + self.pad.width())
		except KeyError:
			pass
		try:
			comp = self.comp_dict['center']
			pref_size = comp.get_preferred_size()
			comp.bounds.x = left
			comp.bounds.y = bottom
			comp.bounds.w = right - left
			comp.bounds.h = top - bottom
		except KeyError:
			pass

	def get_preferred_size(self):
		w = 0
		h = 0
		for c in self.container.components:
			width, height = c.get_preferred_size().as_tuple()
			h = max(h, height)
			w += width + self.pad.width()
		w += self.container.insets.width()
		h += self.container.insets.height() + self.pad.height()
		return Size(w, h)
		
# Window layout is meant to arrange 3 components on a page or window
# The 'top' and 'bottom' components are aligned to their respective edges and preferred heights
# The 'center' component is given the remainder of the space
		
class HWindowLayout(HLayout):
	def __init__(self, container):
		HLayout.__init__(self, container)
		self.fill_width = True		
		self.comp_dict = {}
		
	def add(self, comp, constraints):
		if constraints is None:
			constraints = 'center'
		self.comp_dict[constraints] = comp
			
	def do_layout(self):
		layoutSize = self.container.bounds.size()
		width = layoutSize.w - (self.container.insets.width() + self.pad.width())
		top = self.container.bounds.h - (self.container.insets.top + self.pad.top)
		left = self.container.insets.left + self.pad.left
		bottom = self.container.insets.bottom + self.pad.bottom
		try:
			comp = self.comp_dict['bottom']
			prefSize = comp.get_preferred_size()
			comp.bounds.y = bottom
			comp.bounds.h = prefSize.h
			if(self.fill_width):
				comp.bounds.w = width
				comp.bounds.x = left
			else:
				comp.bounds.w = prefSize.w
				comp.bounds.x = left + (width - prefSize.w) / 2
			bottom += comp.bounds.h + self.pad.height()
		except KeyError:
			pass
		try:
			comp = self.comp_dict['top']
			prefSize = comp.get_preferred_size()
			comp.bounds.h = prefSize.h
			comp.bounds.y = top - prefSize.h
			if(self.fill_width):
				comp.bounds.w = width
				comp.bounds.x = left
			else:
				comp.bounds.w = prefSize.w
				comp.bounds.x = left + (width - prefSize.w) / 2
			top = comp.bounds.y - self.pad.height()
		except KeyError:
			pass
		try:
			comp = self.comp_dict['center']
			comp.bounds.y = bottom
			comp.bounds.h = top - bottom
			if(self.fill_width):
				comp.bounds.w = width
				comp.bounds.x = left
			else:
				prefSize = comp.get_preferred_size()
				comp.bounds.w = prefSize.w
				comp.bounds.x = left + (width - prefSize.w) / 2
		except KeyError:
			pass

	def get_preferred_size(self):
		w = 0
		h = 0
		for c in self.container.components:
			width, height = c.get_preferred_size().as_tuple()
			w = max(w, width)
			h += height + self.pad.height()
		w += self.container.insets.width()
		h += self.container.insets.height()
		return Size(w, h)