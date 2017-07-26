# https://gist.github.com/anonymous/25858010405ba6ea4fed7526e4d95a12

import ui

class SplitView (ui.View):
	def __init__(self, master_width=300, child_min=300, mv=ui.View()):
		'''
		:master_width: the width of the master view
		:child_min: the minimum size of the child before going to a nav view
		'''
		self.width = 800
		self.height = 800
		self.master_width = master_width
		self.mv = mv
		self.child = ui.View()
		self.mv.name = 'mv'
		self.child.name = 'child'
		self.mv.background_color = (.67, .96, 1.0)
		self.child.background_color = (.81, 1.0, .38)
		self.mv.x = 0
		self.mv.y=0
		self.mv.flex = 'H'
		self.mv.height = self.height
		self.mv.width = self.master_width
		self.mv.height = self.height
		self.mv.background_color = 'blue'
		self.child.flex='WHL'
		self.child.x = mv.width
		self.child.height = self.height
		self.add_subview(self. mv)
		self.add_subview(self.child)
		self.nav = ui.NavigationView(self.mv)
		self.nav.hidden = True
		self.nav.width = self.width
		self.nav.height = self.height
		self.nav.flex = 'WH'
		self.add_subview(self.nav)
		self.child_min = child_min
		
	def pop_child(self, view):
		pass
		
	def did_load(self):
		# This will be called when a view has been fully loaded from a UI file.
		pass
		
	def will_close(self):
		# This will be called when a presented view is about to be dismissed.
		# You might want to save data here.
		pass
		
	def draw(self):
		pass
		
	def is_big_enough(self):
		'''checks if we can actually fit everything'''
		if self.child_min + self.mv.width > self.width:
			return False
		else:
			return True
			
	def layout(self):
		# This will be called when a view is resized. You should typically set the
		# frames of the view's subviews here, if your layout requirements cannot
		# be fulfilled with the standard auto-resizing (flex) attribute.
		if self.is_big_enough():
			self.nav.hidden = True
			self.child.x = self.mv.width
			self.child.hidden = False
			self.mv.hidden = False
		else:
			self.child.hidden = True
			self.mv.hidden = True
			self.nav.hidden = False
			
	def touch_began(self, touch):
		# Called when a touch begins.
		pass
		
	def touch_moved(self, touch):
		# Called when a touch moves.
		pass
		
	def touch_ended(self, touch):
		# Called when a touch ends.
		pass
		
	def keyboard_frame_will_change(self, frame):
		# Called when the on-screen keyboard appears/disappears
		# Note: The frame is in screen coordinates.
		pass
		
	def keyboard_frame_did_change(self, frame):
		# Called when the on-screen keyboard appears/disappears
		# Note: The frame is in screen coordinates.
		pass
		
v = SplitView()
