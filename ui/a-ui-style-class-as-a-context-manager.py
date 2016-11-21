# https://forum.omz-software.com/topic/3573/lab-a-ui-style-class-as-a-context-manager

# Pythonista Forum - @Phuket2
import ui, editor, copy
from time import sleep

class UIStyle(object):
	dict_list = []
	def __init__(self, *args, **kwargs):
		self.bg_color = 'white'
		self.border_color = 'black'
		self.corner_radius = 0
		self.text_color = 'black'
		self.tint_color = None
		self.font = ('Arial Rounded MT Bold', 22)
		self.flex = 'wh'
		self.alpha = 1.0
		self.apply_style_kwargs(**kwargs)
		
	def __enter__(self):
		__class__.dict_list.append(copy.copy(self.__dict__))
		return self
		
	def __exit__(self, type, value, traceback):
		self.__dict__.update(__class__.dict_list.pop())
		
	def apply_style_kwargs(self, **kwargs):
		# set our class attrs with kwargs , these attrs stick
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def apply_style(self, obj, **kwargs):
		'''
		apply the attrs in our dict to a ui object (obj)
		you can overwrite attrs, will not effect the dict as
		the class is a context manager and we use the with key word,
		so the enter and exit methods are called automatically.
		This can be done outside the class, but maybe this is more
		convienient.?
		'''
		with self as style:
			self.apply_style_kwargs(**kwargs)
			for k, v in self.__dict__.items():
				if hasattr(obj, k):
					setattr(obj, k, v)
					
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		pass
		
if __name__ == '__main__':
	_use_theme = False
	w, h = 600, 800
	f = (0, 0, w, h)
	
	# all the standard stuff
	style = 'sheet'
	mc = MyClass(frame=f)
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)
		
	# THE TEST STARTS BELOW
	
	# show UIStyle() working...
	s = UIStyle()
	
	# s.apply_style is wrapped in a with statement
	s.apply_style(mc, bg_color='deeppink') # override the bg_color
	sleep(2)
	print('s.bg_color=', s.bg_color)
	
	# keep in mind, s.apply_style is also using a with statement
	# this example just to show nesting is working
	with s:
		s.apply_style(mc, bg_color='green') # override the bg_color
		sleep(2)
		s.bg_color = 'orange' # we are still in a with block
		s.apply_style(mc) # override the bg_color
		sleep(2)
		s.bg_color = 'blue'
		s.apply_style(mc) # override the bg_color
		sleep(1)
		
	s.apply_style(mc)
	print('game over, the bg_color is still -', s.bg_color)
# --------------------

