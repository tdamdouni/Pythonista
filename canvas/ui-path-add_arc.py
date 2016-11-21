# https://forum.omz-software.com/topic/3310/i-need-help-using-ui-path-add_arc

def draw_arc(rect):
	r = ui.Rect(*rect)
	s = ui.Path()
	s.move_to(r.center()[0], r.center()[1])
	s.add_arc(r.center()[0], r.center()[1], r.width / 2,math.radians(0), math.radians(45))
	
	s.eo_fill_rule = False
	s.close()
	ui.set_color('black')
	s.line_width = .3
	s.stroke()
# --------------------

def draw_arc(rect):
	r = ui.Rect(*rect)
	s = ui.Path()
	s.move_to(r.center()[0], r.center()[1])
	s.add_arc(r.center()[0], r.center()[1], r.width / 2,math.radians(0), math.radians(45))
	
	s.eo_fill_rule = False
	s.close()
	ui.set_color('black')
	s.line_width = .3
	s.stroke()
# --------------------
import ui
import math

with ui.ImageContext(100, 100) as ctx:
	r = ui.Rect(0,0,100,100)
	s = ui.Path()
	radius = r.width / 2
	start = 0
	finish = 90
	start = math.radians(start)
	finish = math.radians(finish)
	x = r.center()[0]+radius * math.cos(start)
	y = r.center()[1]+radius * math.sin(start)
	s.move_to(x, y)
	s.add_arc(r.center()[0], r.center()[1], radius, start, finish)
	s.eo_fill_rule = False
	#s.close()
	ui.set_color('black')
	s.line_width = 1
	s.stroke()
	#s.fill()
	img = ctx.get_image()
	img.show()
# --------------------
import ui, editor
import math

def draw_arc(rect):
	r = ui.Rect(*rect)
	s = ui.Path()
	
	radius = r.width / 2
	
	start = 0
	finish = 90
	start = math.radians(start)
	finish = math.radians(finish)
	
	#x = radius * math.cos(start)
	#y = radius * math.sin(finish)
	x = r.center()[0]+radius * math.cos(start)
	y = r.center()[1]+radius
	
	s.move_to(x, y)
	s.add_arc(r.center()[0], r.center()[1], radius, start, finish)
	
	s.eo_fill_rule = False
	#s.close()
	ui.set_color('black')
	s.line_width = 1
	s.stroke()
	#s.fill()
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def draw(self):
	
		r = ui.Rect(10, 10, 200, 200)
		s = ui.Path.oval(*r)
		ui.set_color('deeppink')
		s.fill()
		draw_arc(r.inset(10, 10))
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=False)
# --------------------
y = r.center()[1]+radius * math.sin(start)# --------------------
import ui, editor
import math, time

def draw_arc(rect, start, finish, offset = -90):
	r = ui.Rect(*rect)
	s = ui.Path()
	
	radius = r.width / 2
	
	start = math.radians(start + offset)
	finish = math.radians(finish + offset )
	
	x = r.center()[0]+radius * math.cos(start)
	y = r.center()[1]+radius * math.sin(start)
	
	s.move_to(x, y)
	s.add_arc(r.center()[0], r.center()[1], radius, start, finish)
	
	ui.set_color('white')
	s.line_width = 15
	s.line_cap_style = ui.LINE_CAP_ROUND
	s.stroke()
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.deg = 0
		
	def draw(self):
		r = ui.Rect(10, 10, 200, 200)
		s = ui.Path.oval(*r)
		ui.set_color('deeppink')
		s.fill()
		draw_arc(r.inset(20, 20), 0 , self.deg)
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=False)
	for i in range(0, 360):
		mc.deg = i
		mc.set_needs_display()
		time.sleep(.015)
# --------------------

