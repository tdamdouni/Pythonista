# https://gist.github.com/anonymous/ae9572e2d0ba1b1f99f8282cac3adaea

# https://forum.omz-software.com/topic/4138/getting-notification-on-navigationview-go-back

import ui
from functools import partial

class SimpleNavigationView(ui.View):
	def push_view(self, v):
		if self.current_view:
			self.stack.append(self.current_view)
			self.remove_subview(self.current_view)
			self.add_left_buttonitem(self.pop_view)
		if v.bt_subview:
			self.add_right_buttonitem(v.bt_subview)
		else:
			self.right_button_items = []
		self.current_view = v
		self.add_subview(v)
		
	def pop_view(self, sender):
		self.remove_subview(self.current_view)
		self.current_view = self.stack.pop()
		self.add_subview(self.current_view)
		self.add_right_buttonitem(self.current_view.bt_subview)
		if self.stack:
			self.add_left_buttonitem(self.pop_view)
		else:
			self.left_button_items = []
			
	def add_close_buttonitem(self):
		close = ui.ButtonItem()
		close.image = ui.Image.named('ionicons-close-24')
		close.action = self.bt_close
		self.left_button_items = [close]
		
	def add_left_buttonitem(self, action):
		left = ui.ButtonItem()
		left.image = ui.Image.named('ionicons-arrow-left-b-24')
		left.action = action
		self.left_button_items = [left]
		
	def add_right_buttonitem(self, action):
		right = ui.ButtonItem()
		right.image = ui.Image.named('ionicons-arrow-right-b-24')
		right.action = action
		self.right_button_items = [right]
		
	def bt_close(self, sender):
		self.close()
		
	def bt_subview(self, i, sender):
		subview = ui.load_view(self.subviews_pyui[i])
		if i < (len(self.subviews_pyui)-1):
			subview.bt_subview = self.bt_subviews[i+1]
		else:
			subview.bt_subview = None
		self.push_view(subview)
		
	def make_bt_subview(self):
		for i in range(len(self.subviews_pyui)-1, 0, -1):
			self.bt_subviews[i] = partial(self.bt_subview, i)
			
	def __init__(self, w=600, h=400, subviews_pyui=None):
		super().__init__(frame=(0,0,w,h))
		self.subviews_pyui = subviews_pyui
		self.bt_subviews = [None]*len(self.subviews_pyui)
		self.stack = []
		self.current_view = None
		if len(self.subviews_pyui) > 1:
			self.main_view = ui.load_view(self.subviews_pyui[0])
			self.make_bt_subview()
			self.main_view.bt_subview = self.bt_subviews[1]
			self.push_view(self.main_view)
			
			
SimpleNavigationView(w=600, h=400,
        subviews_pyui=('navtest_mainview', 'navtest_subview1', 'navtest_subview2')
            ).present('sheet') #,   hide_title_bar=True)

