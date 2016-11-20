# https://forum.omz-software.com/topic/3504/lab-ui-animate-sliding-in-views

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor

def slide_up(p, v, reverse = False, delay = 1.0 ):
	v.y = p.height if not reverse else -p.height
	
	def animation():
		v.y = 0
		
	ui.animate(animation, delay)
	
def slide_in(p, v, reverse = False, delay = 1.0 ):
	v.x = p.width if not reverse else -p.width
	
	def animation():
		v.x = 0
		
	ui.animate(animation, delay)
	
class MyClass2(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bg_color = 'deeppink'
		btn = ui.Button(frame=(30, 30, 100, 100))
		btn.title = 'hit me'
		btn.border_width =2
		btn.border_color = 'white'
		btn.corner_radius = btn.width / 2
		self.add_subview(btn)
		
	def draw(self):
		# do a draw, just to see how it works
		r = ui.Rect(*self.bounds).inset(20, 20)
		s = ui.Path.rect(*r)
		s.line_width = 10
		ui.set_color('blue')
		s.stroke()
		
		
class MyClass(ui.View):
	#def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		
	def add_view(self, v):
		self.add_subview(v)
		# comment out either line below for 1 effect
		slide_up(self, v, reverse=False, delay = 3)
		slide_in(self, v, reverse=False, delay=.8)
		
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 540, 540
	f = ui.Rect(0, 0, w, h)
	style='sheet'
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style = style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)
	mc2 = MyClass2(frame = f)
	mc.add_view(mc2)

