# https://forum.omz-software.com/topic/2544/wish-list-for-next-release/129

class MyShape(object):
	shapes = [ui.Path.rect, ui.Path.oval, ui.Path.rounded_rect]
	
	def __init__(self, r = ui.Rect(0, 0, 100, 100),
	shape_index = 0, *args, **kwargs):
		self.r = r
		self.radius = 6
		
	shape = self.shapes[shape_index]
	
	if shape_index == 2:
	# rounded rect
		self.shape = shape(*r, self.radius)
		else:
			self.shape = shape(*r)
			
	def draw_me(self):
		with ui.GState():
		ui.set_color('yellow')
		self.shape.fill()

