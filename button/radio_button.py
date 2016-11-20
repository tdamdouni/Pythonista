# https://gist.github.com/Phuket2/2117d9f7590f5a8d09cbd62d6291d826

import ui

class RadioButton(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		self.frame = (100, 100, 100, 100)
		self.touch_enabled = True
		self.selected = True
		
	def draw(self):
		r = ui.Rect(*self.bounds).inset(1,1)
		s = ui.Path.oval(*r)
		s.line_width = 2
		
		ui.set_color('silver')
		s.fill()
		ui.set_color('black')
		s.stroke()
		
		ui.set_color('white')
		r = ui.Rect(*self.bounds).inset(3, 3)
		s = ui.Path.oval(*r)
		s.line_width = 1
		s.stroke()
		if self.selected:
			ui.set_color('red')
			ui.set_shadow('black', 0, 0 , 15)
			r = ui.Rect(*self.bounds).inset(18, 18)
			s = ui.Path.oval(*r)
			s.fill()
		else:
			ui.set_color('darkgray')
			ui.set_shadow('black', 0, 0 , 15)
			r = ui.Rect(*self.bounds).inset(18, 18)
			s = ui.Path.oval(*r)
			s.fill()
			
	def touch_ended(self, touch):
		self.selected = not self.selected
		self.set_needs_display()
		
		
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		self.add_subview(RadioButton())
		
if __name__ == '__main__':
	w = 320
	h = 400
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white')
	mc.present('sheet')

