# coding: utf-8

# https://gist.github.com/Phuket2/7474c485ace1ef68d112

# https://forum.omz-software.com/topic/2911/share-page-indicator-ui-view

import ui
'''
        Date: 10 March 2016
        Pythonista 2.01 beta

        PageIndicator Class
        ===================
        An attempt to mimick the page indicator found in some iOS interfaces
        supports circles/rects, defaults to circles.

        Most of the settings are done at creation time. Something, you would
        normally initialse and only set the display page.

        Feel free to use it, chop it up, improve it, ignore it.
        Pythonista Forum : @Phuket2
'''
class PageIndicator(ui.View):
	def __init__(self, *args, **kwargs):
	
		# default values. all attrs can be changed in kwargs
		
		self.num_pages = 5                              # number of pages/dots
		self.w = 12                                             # cell width
		self.h = 12                                             # cell height
		self.factor = .8                                        # the drawing cell is inset
		self.selected = 0                               # the selected page
		self.on_color = 'orange'                # color used when page is selected
		self.off_color = 'gray'         # color used when page not selected
		self.shape = 'oval'                             # valid shapes as text, oval and rect
		
		# set the attrs to the kwargs
		for k,v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)
				
		# just like doing this
		parent = kwargs.get('parent', None)
		if parent: parent.add_subview()
		
		self.set_page(self.selected)
		
	def layout(self):
		# ui callback
		self.width = self.w * self.num_pages
		self.height = self.h
		
	def next(self):
		if self.selected == self.num_pages - 1:
			pg_num = 0
		else:
			pg_num = self.selected + 1
			
		self.set_page(pg_num)
		
	def prev(self):
		if self.selected == 0:
			pg_num = self.num_pages - 1
		else:
			pg_num = self.selected - 1
			
		self.set_page(pg_num)
		
	def set_page(self, pg_no):
		self.selected = pg_no % self.num_pages
		self.set_needs_display()
		return
		if pg_no < self.num_pages:
			self.selected = pg_no
		else:
			self.selected = 0
			
		self.set_needs_display()
		
	def draw(self):
		# draws the cirles/ovals to the ImageContext of the Custom View
		# the Pythonista Docs states, for Custom Views the ImageContext
		# is automatically setup for you.
		ui.set_color(self.off_color)
		
		is_oval = True if self.shape.lower() == 'oval' else False
		
		for i in range(0,self.num_pages +1):
			r = ui.Rect(self.w * i, 0, self.w, self.h).inset(self.w - (self.w * self.factor), self.h - (self.h * self.factor))
			
			if is_oval:
				shape = ui.Path.oval(*r)
			else:
				shape =         ui.Path.rect(*r)
				
			if i == self.selected:
				ui.set_color(self.on_color)
				shape.fill()
				ui.set_color(self.off_color)
			else:
				shape.fill()
				
def make_button(name, title, action):
	# just for testing
	btn = ui.Button(name = name, title = title)
	btn.action = action
	btn.width = 100
	btn.height = 32
	btn.border_width = .5
	btn.corner_radius = 3
	btn.font = ('<System-Bold>', 14)
	btn.bg_color = 'gray'
	btn.tint_color = 'orange'
	return btn
	
class TestClass(ui.View):
	# just for testing
	def __init__(self, image_mask = None, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		# Init the PageIndicator and add it to the subview
		self.pg_ind = PageIndicator(off_color = 'gray', num_pages = 9, shape = 'oval')
		self.add_subview(self.pg_ind)
		
		btn = make_button('Next', 'Next', self.next_page)
		self.add_subview(btn)
		btn.x = self.center[0] - btn.width / 2
		btn.y = 100
		
		btn = make_button('Previous', 'Previous', self.prev_page)
		self.add_subview(btn)
		btn.x = self.center[0] - btn.width / 2
		btn.y = 142
		
		
	def next_page(self, sender):
		self.pg_ind.next()
		
	def prev_page(self, sender):
		self.pg_ind.prev()
		
	def layout(self):
		pg_ind = self.pg_ind
		pg_ind.y = self.bounds.height - (pg_ind.h + 10)
		pg_ind.x = (self.bounds.width / 2 ) - (pg_ind.width / 2)
		
		
if __name__ == '__main__':
	f = (0,0, 200, 300)
	tc = TestClass( frame = f, bg_color = 'white')
	tc.present('sheet', animated = False)

