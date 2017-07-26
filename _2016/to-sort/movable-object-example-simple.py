# https://forum.omz-software.com/topic/3613/resizable-and-movable-view/5

import ui

class customView(ui.View):
	'''a view that can be moved and resized
	'''
	def __init__(self,**kvargs):
		super().__init__(self,**kvargs)
		self.button = ui.Button()
		self.button.image = ui.Image("iob:arrow_resize_24")
		self.button.frame = (10,10,24,24)
		self.button.touch_enabled = False
		self.add_subview(self.button)
	def touch_moved(self, touch):
		x,y = touch.location
		xp,yp = touch.prev_location
		dx = x-xp
		dy = y-yp
		if x < 40 and y < 40:
			self.width -= dx
			self.height -= dy
		self.x += dx
		self.y += dy
		
# a top level view
gv = ui.View(background_color='white',name='global view')
gv.present('fullscreen')

view2 = customView(background_color='white',name='view1')
gv.add_subview(view2)
s = view2.superview
s = s.width/2-20
view2.frame = (s+30, 10, s, s+60)
view2.border_width = 2
view2.border_color = '#0016ff'
view2.alpha = 0.9
view2.corner_radius = 15

