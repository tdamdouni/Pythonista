# https://forum.omz-software.com/topic/3526/removing-views-with-ui-transforms/8

'''
    Pythonista Forum - @Phuket2
'''
import ui

def quick_button(p):
	# p is the parent view
	_inset = 60
	btn = ui.Button(name='btn')
	btn.frame = ui.Rect(0, 0, p.width, p.width ).inset(_inset, _inset)
	btn.corner_radius = btn.width / 2
	btn.center = p.bounds.center()
	btn.title = 'Push Me'
	btn.bg_color = 'cornflowerblue'
	btn.tint_color = 'white'
	btn.font = ('Arial Rounded MT Bold', 48)
	p.add_subview(btn)
	return btn
	
def slide_in(p, v, duration = .5, reverse = False, delay = 0 ):
	v.x = p.width if not reverse else -p.width
	
	def animation():
		v.x = 0
		
	ui.animate(animation, duration = duration ,  delay=delay)
	
class MyClassB(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bg_color = 'purple'
		self.hidden = True
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		f = (0, 0, self.width, 44)
		cb = MyClassB(name = 'classb', frame = f)
		self.add_subview(cb)
		qb = quick_button(self)
		qb.action = self.my_action
		self.add_subview(qb)
		
	def my_action(self, sender):
		v = self['classb']
		v.hidden = False
		slide_in(self, self['classb'], reverse = False)
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=False)
# --------------------
'''
        Pythonista Forum - @Phuket2
'''
import ui

def quick_button(p, title = 'Push Me'):
	# p is the parent view
	_inset = 60
	btn = ui.Button(name='btn')
	btn.frame = ui.Rect(0, 0, p.width, p.width ).inset(_inset, _inset)
	btn.corner_radius = btn.width / 2
	btn.center = p.bounds.center()
	btn.title = title
	btn.bg_color = 'cornflowerblue'
	btn.tint_color = 'white'
	btn.font = ('Arial Rounded MT Bold', 24)
	p.add_subview(btn)
	return btn
	
def slide_in(p, v, duration = .5, reverse = False, delay = 0, compl=None):
	v.x = -p.width
	x = p.width
	y = 0
	def a():
		v.transform=ui.Transform.translation(x, y)
		v.hidden = False
		
	#def compl():
		#pass
		
	ui.animate(a, duration = duration ,  delay=delay, completion = compl)
	
def slide_out(p, v, duration = .5, reverse = False, delay = 0 ):
	v.x = 0
	x = p.width
	y = 0
	
	def a():
		v.transform=ui.Transform()
		
	def compl():
		v.hidden = True
		p.remove_subview(v)
		
	v.transform=ui.Transform.translation(x, y)
	ui.animate(a, duration = duration ,  delay=delay, completion = compl)
	
class MyClassB(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bg_color = 'purple'
		self.hidden = True
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		f = (0, 0, self.width, 44)
		cb = MyClassB(name = 'classb', frame = f)
		self.add_subview(cb)
		qb = quick_button(self, title = 'Slide out')
		qb.enabled = False
		qb.action = self.my_action
		
		
	def my_action(self, sender):
		# disable our button as the view is removed. this button is
		# no longer relevant
		self['btn'].enabled = False
		slide_out(self, self['classb'], duration = 2)
		
	def slide_in_complete(self):
		# activate other parts of our ui once the slide_in is complete
		self['btn'].enabled = True
		
if __name__ == '__main__':
	w, h = 320, 480
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=True)
	slide_in(mc, mc['classb'] , duration = 1, compl = mc.slide_in_complete)
# --------------------

