# https://forum.omz-software.com/topic/3513/lab-playing-with-ui-transforms-high-level-access

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor
from random import choice, randrange
import time, sys
import copy

class obj_effect(object):
	'''
	just an idea....Sorry not well thought out.
	a class/wrapper that simplifies transformations for a given
	object.
	only scratching the surface here.
	Some will think its too high level and a waste. But
	i am sure something like this could help people make more
	intresting ui's when ui is not their focus.
	As i say, this is just food for thought, needs a lot more work.
	
	I am sure there is a better way to factor the code, but need to
	start somewhere.
	but starting idea, i try to get...
	
	1. named effects, being able to pass all attrs via kwargs to each effect.
	2. can be used as a context manager - 'with' keyword
	
	so much more can be done.  at the moment using doing scale, but
	could use rotate and translation.
	Also could use a queue of sorts that was aware of the duration
	and delay.when you add a object to the queue it could for example
	set the delay correctly as an accumulated value. well something
	like that.
	
	3.Also implementation of ui.Transform.invert reversing
	transformations.
	
	But many things wrong with this example.  eg. you can keep
	touching the button, currently no way to know a set of cmds
	have completed to block unintended multiple presses.
	
	'''
	dict_list = []
	def __init__(self, obj, *args, **kwargs):
		self.obj = obj
		self.duration = .5
		self.delay = 0
		self.x = 1.2
		self.y = 1.2
		self.complete = self.completion
		
	def _do_effect_scale(self):
		def ani():
			self.obj.transform=ui.Transform()
			
		self.obj.transform=ui.Transform.scale(self.x, self.y )
		ui.animate(ani,duration=self.duration, delay = self.delay, completion = self.complete)
		
	def grow(self, **kwargs):
		self.set_kwargs(**kwargs)
		self._do_effect_scale()
		
	def rotate(self, **kwargs):
		self.set_kwargs(**kwargs)
		self.x = -1
		self.y = -1
		self._do_effect_scale()
		
		
	def flip_h(self, **kwargs):
		self.set_kwargs(**kwargs)
		self.x = -1
		self.y = 1
		self._do_effect_scale()
		
	def flip_v(self, **kwargs):
		self.set_kwargs(**kwargs)
		self.x= 1
		self.y = -1
		self._do_effect_scale()
		
	def set_kwargs(self, **kwargs):
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def completion(self):
		# poor attempt to capture the calling function...
		# sys._getframe(x).f_code.co_name,was just a idea, does not work
		# sure there is another way, was hoping for something simple
		print(sys._getframe().f_code.co_name, time.strftime('%H:%M:%S'))
		pass
		
	def __enter__(self):
		__class__.dict_list.append(copy.copy(self.__dict__))
		return self
		
	def __exit__(self, type, value, traceback):
		self.__dict__.update(__class__.dict_list.pop())
		
		
		
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		
		# create a button for testing
		btn = ui.Button(title = 'Hello',frame = (0, 0, 200, 200))
		btn.font = ('Arial Rounded MT Bold', 48)
		btn.border_width = 2
		btn.border_color = 'orange'
		btn.size_to_fit()
		btn.width=btn.height = btn.width + 20
		btn.corner_radius = btn.width / 2
		btn.center = self.bounds.center()
		btn.bg_color = 'cornflowerblue'
		btn.y -= 36
		btn.action = self.btn_action
		self.add_subview(btn)
		self.eo = obj_effect(btn)
		
	def btn_action(self, sender):
		# apply an effect/s to a ui element. do this first as its async,
		# then do your stuff after
		with self.eo as effect:
			effect.grow(x = 1.8, y = 1.8, delay = 0)
			
		with self.eo as effect:
			effect.rotate(delay = 2, duration = 1)
			
		with self.eo as effect:
			effect.grow(delay = 1.6)
			
		with self.eo as effect:
			effect.flip_v(delay = 2.3)
			
		with self.eo as effect:
			effect.flip_h(delay = 2.9)
			
		# debug-look to see if the context is working....
		# appears to be
		print(self.eo.__dict__)
		
		# do something...
		print('i did something at -', time.strftime('%H:%M:%S'))
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 320, 480
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet', animated=False)
# --------------------

