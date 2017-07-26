# https://forum.omz-software.com/topic/3613/resizable-and-movable-view/6

import ui

class customView(ui.View):
	'''a view that can be moved and resized
	'''
	def __init__(self,**kvargs):
		super().__init__(self,**kvargs)
		self.frame = (0,0,500,500)
		self.wmin = 300
		self.hmin = 300
		iv = ui.ImageView()
		iv.image = ui.Image('iob:arrow_expand_24')
		iv.frame = (500-28, 500-28, 24, 24)
		iv.flex = 'LT'
		self.add_subview(iv)
		iv = ui.ImageView()
		iv.image = ui.Image('iob:ios7_circle_outline_32')
		iv.frame = (500-32, 500-32, 32, 32)
		iv.flex = 'LT'
		self.add_subview(iv)
	def touch_moved(self, touch):
		x,y = touch.location
		xp,yp = touch.prev_location
		dx = x-xp
		dy = y-yp
		if x > self.width - 40 and y > self.height - 40:
			self.width += dx
			self.height += dy
			if self.width < self.wmin: self.width = self.wmin
			if self.height < self.hmin: self.height = self.hmin
		else:
			self.x += dx
			self.y += dy
			
# a top level view
gv = ui.View(background_color='white',name='global view')
gv.present('fullscreen')

# the custom view
view2 = customView(background_color='white',name='view2')
gv.add_subview(view2)
s = view2.superview
s = s.width/2-20
view2.frame = (s+30, 10, s, s+60)
view2.border_width = 2
view2.border_color = '#0016ff'
view2.alpha = 0.9
view2.corner_radius = 15

# something to put inside
view3 = ui.View(background_color='red',name='view3')
view3.frame = (20,20,300,150)
view3.flex = 'BR' # this defines how the content will resize
view2.add_subview(view3)

view4 = ui.View(background_color='orange',name='view4')
view4.frame = (20,200,300,200)
view4.flex = 'WH' # this defines how the content will resize
view2.add_subview(view4)

