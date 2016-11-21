# https://forum.omz-software.com/topic/3547/tip-ui-rect-if-you-are-not-using-it-for-ui-you-should/2

# Pythonista Forum - @Phuket2
import ui, editor

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		self.sv = None
		self.v_gap = 10     # vertical space between views
		self.make_view()
		
	def make_view(self):
		sv = ui.ScrollView(frame = self.bounds.inset(20, 20))
		sv.flex = 'wh'
		sv.bg_color = 'white'
		sv.corner_radius = 3
		self.sv = sv
		self.add_subview(sv)
		
	def add_view(self, h):
		parent = self.sv  # our parent is the ScrollView
		r = ui.Rect(0, 0, parent.width, h).inset(5, 5)
		v = ui.View(frame = r)
		v.y = self.calc_y()
		v.border_width = 1
		v.corner_radius = 6
		v.flex = 'w'
		parent.add_subview(v)
		parent.content_size = (0, v.frame.max_y + self.v_gap )
		
	def calc_y(self):
		# returns the new y for the next element that will be added to
		# scrollview.
		
		# seems stupid to do this.  i am tending more to do this style
		# now. have a var that points to our parent contextually.
		# i make less mistakes this way, and think faster
		parent = self.sv  # our parent is the ScrollView
		
		if not len(parent.subviews):
			return self.v_gap
			
		return parent.subviews[len(parent.subviews)-1].frame.max_y + self.v_gap
		
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	w, h = 320, 568 # iphone 5 up
	f = (0, 0, w, h)
	style = 'sheet'
	animated = False
	
	mc = MyClass(frame=f, bg_color='white', name = 'ScrollView Test')
	
	if not _use_theme:
		mc.present(style=style, animated=animated)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=animated)
	# its just an example... we do the call to create the scrollview
	# views here.
	h_list = [100, 200, 50, 100, 60, 80, 90, 300, 44, 60, 90, 300, 90]
	for h in h_list:
		mc.add_view(h)
# --------------------
# Pythonista Forum - @Phuket2
import ui, editor

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		self.sv = None
		self.v_gap = 10     # vertical space between views
		self.make_view()
		
	def make_view(self):
		sv = ui.ScrollView(frame = self.bounds.inset(20, 20))
		sv.flex = 'wh'
		sv.bg_color = 'white'
		sv.corner_radius = 3
		self.sv = sv
		self.add_subview(sv)
		
	def add_view(self, h):
		parent = self.sv  # our parent is the ScrollView
		r = ui.Rect(0, 0, parent.width, h).inset(5, 5)
		v = ui.View(frame = r)
		v.y = self.calc_y()
		v.border_width = 1
		v.corner_radius = 6
		v.flex = 'w'
		parent.add_subview(v)
		
		# added this
		r = ui.Rect(0, 0, v.height, v.height).inset(10, 10)
		btn = ui.Button(name = 'btn', frame = r)
		btn.choice = False  # dynamically added attr
		btn.image = ui.Image.named('iob:ios7_checkmark_outline_256')
		btn.tint_color = 'lightgray'
		btn.action = self.action
		v.add_subview(btn)
		
		parent.content_size = (0, v.frame.max_y + self.v_gap )
		
	def calc_y(self):
		# returns the new y for the next element that will be added to
		# scrollview.
		
		# seems stupid to do this.  i am tending more to do this style
		# now. have a var that points to our parent contextually.
		# i make less mistakes this way, and think faster
		parent = self.sv  # our parent is the ScrollView
		
		if not len(parent.subviews):
			return self.v_gap
			
		return parent.subviews[len(parent.subviews)-1].frame.max_y + self.v_gap
		
	def action(self, sender):
		# added this
		# the action for the button
		parent = self.sv  # our parent is the ScrollView
		for v in parent.subviews:
			btn = v['btn']
			btn.tint_color = 'lightgray'
			btn.choice = False
			
		sender.tint_color = 'deeppink'
		sender.choice = True
		
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	w, h = 320, 568 # iphone 5 up
	f = (0, 0, w, h)
	style = ''
	animated = False
	
	mc = MyClass(frame=f, bg_color='white', name = 'ScrollView Test')
	
	if not _use_theme:
		mc.present(style=style, animated=animated)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=animated)
	# its just an example... we do the call to create the scrollview
	# views here.
	#h_list = [80, 80, 80, 80, 60, 80, 90, 300, 44, 60, 90, 300, 90]
	h_list = [80] * 20
	for h in h_list:
		mc.add_view(h)
# --------------------

