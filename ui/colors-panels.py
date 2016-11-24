'''
Pythonista Forum - @Phuket2
'''
import ui, editor
from random import choice, randint

_colors=['rosybrown', 'antiquewhite', 'lightsteelblue', 'white', 'darkblue', 'darkviolet', 'plum', 'darkcyan', 'blanchedalmond', 'chocolate', 'sienna', 'tomato', 'peachpuff', 'lightyellow', 'bisque', 'aqua', 'oldlace', 'maroon', 'palegreen', 'chartreuse', 'darkturquoise', 'linen', 'magenta', 'lemonchiffon', 'powderblue', 'papayawhip', 'gold', 'khaki', 'lightseagreen', 'darkred', 'floralwhite', 'turquoise', 'mediumspringgreen', 'indianred', 'lightgreen', 'crimson', 'mintcream', 'lavender', 'purple', 'orchid', 'darkslateblue', 'whitesmoke', 'moccasin', 'beige', 'mistyrose', 'dodgerblue', 'hotpink', 'lightcoral', 'goldenrod', 'coral', 'cadetblue', 'black', 'mediumseagreen', 'gainsboro', 'paleturquoise', 'darkgreen', 'darkkhaki']

class Panel(ui.View):
	def __init__(self, text, *args, **kwargs):
		self.bg_color = 'cornflowerblue'
		super().__init__(*args, **kwargs)
		
		self.corner_radius = 6
		self.make_view(text)
		
	def make_view(self, text):
		lb = ui.Label(name = 'lb', frame = self.frame)
		lb.text = text
		lb.font=('Arial Rounded MT Bold', 24)
		lb.size_to_fit()
		lb.center = self.bounds.center()
		self.add_subview(lb)
		
def e(v, t, d, x, y):
	'''
	v = the view to animate
	t = duration
	d = delay
	x = x
	y = y
	'''
	def a():
		v.transform=ui.Transform()
		
	def complete():
		pass
		
	v.transform=ui.Transform.translation(x, y)
	ui.animate(a, duration = t, delay = d,  completion = complete)
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
if __name__ == '__main__':
	_use_theme = True
	animated  = False
	w, h = 600, 800
	f = (0, 0, w, h)
		
mc = MyClass(frame=f, bg_color='white')
		
if not _use_theme:
	mc.present('sheet', animated=animated)
else:
	editor.present_themed(mc, theme_name='Cool Glow', style='sheet', animated=False)
		
	r = ui.Rect(*mc.bounds).inset(20, 20)
	r.height = 100
	
	delay = .3
	x = choice([-1, 1, 0]) * mc.width
	y = choice([-1, 1, 0]) * mc.height
	for i in range(6):
		p = Panel(str(i),frame = r, bg_color=choice(_colors))
		mc.add_subview(p)
		
		e(p,.5, delay * (i*(i * .3)), x, y)
		r.y = r.max_y + 20

