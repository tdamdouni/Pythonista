import ui
from math import pi, sin, cos, radians

def draw_pie(p, r, fill_color='black'):
	p = max(0.0, min(1.0, p))
	with ui.ImageContext(r * 2, r * 2) as ctx:
		ui.set_color(fill_color)
		path = ui.Path()
		center = ui.Point(r, r)
		path.move_to(center.x, center.y)
		start = radians(-90)
		end = start + p * radians(360)
		path.add_arc(r, r, r, start, end)
		path.close()
		ui.set_color(fill_color)
		path.fill()
		return ctx.get_image()
		
pie_img = draw_pie(0.75, 200)
pie_img.show()

# --------------------

def draw_pie(p, r, fill_color='black'):
	p = max(0.0, min(1.0, p))
	ui.set_color(fill_color)
	path = ui.Path()
	center = ui.Point(r, r)
	path.move_to(center.x, center.y)
	start = radians(-90)
	end = start + p * radians(360)
	path.add_arc(r, r, r, start, end)
	path.close()
	ui.set_color(fill_color)
	path.fill()
	
# --------------------

class PieView (ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(*args, **kwargs)
		self._progress = 0.0
		
	@property
	def progress(self):
		return self._progress
		
	@progress.setter
	def progress(self, value):
		self._progress = value
		self.set_needs_display()
		
	def draw(self):
		draw_pie(self.progress, self.width*0.5)
		
# --------------------

def draw_pie_image(p, r, fill_color='black'):
	with ui.ImageContext(r*2, r*2) as ctx:
		draw_pie(p, r, fill_color)
		return ctx.get_image()
		
# --------------------

# ...
def draw(self):
	SomeOtherViewClass.draw(self)
#--------------------
#draw_pie()--------------------
#draw--------------------
import ui
from math import pi, sin, cos, radians

def draw_pie(p, r, fill_color='black'):
	p = max(0.0, min(1.0, p))
	with ui.ImageContext(r * 2, r * 2) as ctx:
		ui.set_color(fill_color)
		path = ui.Path()
		center = ui.Point(r, r)
		path.move_to(center.x, center.y)
		start = radians(-90)
		end = start + p * radians(360)
		path.add_arc(r, r, r, start, end)
		path.close()
		ui.set_color(fill_color)
		path.fill()
		return ctx.get_image()
		
pie_img = draw_pie(0.75, 200)
pie_img.show()
#--------------------
#draw_pie--------------------
#draw--------------------
#ImageContext

# --------------------

def draw_pie(p, r, fill_color='black'):
	p = max(0.0, min(1.0, p))
	ui.set_color(fill_color)
	path = ui.Path()
	center = ui.Point(r, r)
	path.move_to(center.x, center.y)
	start = radians(-90)
	end = start + p * radians(360)
	path.add_arc(r, r, r, start, end)
	path.close()
	ui.set_color(fill_color)
	path.fill()
	
# --------------------

class PieView (ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(*args, **kwargs)
		self._progress = 0.0
		
	@property
	def progress(self):
		return self._progress
		
	@progress.setter
	def progress(self, value):
		self._progress = value
		self.set_needs_display()
		
	def draw(self):
		draw_pie(self.progress, self.width*0.5)
		
# --------------------

def draw_pie_image(p, r, fill_color='black'):
	with ui.ImageContext(r*2, r*2) as ctx:
		draw_pie(p, r, fill_color)
		return ctx.get_image()
		
# --------------------

# ...
def draw(self):
	SomeOtherViewClass.draw(self)
	
# --------------------

