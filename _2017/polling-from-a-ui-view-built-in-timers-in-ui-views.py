# # https://forum.omz-software.com/topic/4109/polling-from-a-ui-view-built-in-timers-in-ui-views/

# ui.delay

# --------------------

from ui import *
from functools import partial

def poll(interval):
	def interval_decorator(func):
		def func_wrapper(self, *args, **kwargs):
			with_args = partial(wrapped_func, self, *args, **kwargs)
			delay(with_args, interval)
			return func(self, *args, **kwargs)
		wrapped_func = func_wrapper
		return func_wrapper
	return interval_decorator
	
# --------------------

class CustomView(View):

	@poll(1)
	def get_text(self, name):
		print("Hello " + name)
		
	def will_close(self):
		cancel_delays()
		
if __name__ == '__main__':
	v = CustomView()
	v.background_color = 'white'
	v.present('sheet')
	
	v.get_text('John')
	
# --------------------

#polling

# --------------------

#coding: utf-8
from ui import *
from functools import partial

def poll(interval):
	def interval_decorator(func):
		def func_wrapper(self, *args, **kwargs):
			if self.polling and isinstance(self, View) and self.on_screen:
				with_args = partial(wrapped_func, self, *args, **kwargs)
				delay(with_args, interval)
				return func(self, *args, **kwargs)
			else:
				self._polling = False
		wrapped_func = func_wrapper
		return func_wrapper
	return interval_decorator
	
class CustomView(View):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._polling = False
		
	@poll(1)
	def get_text(self, name):
		print("Hello " + name)
		
	def will_close(self):
		self.polling = False
		
	@property
	def polling(self):
		return self._polling
		
	@polling.setter
	def polling(self, value):
		was_polling = self._polling
		self._polling = value
		if not was_polling and self._polling:
			self.get_text('John')
			
if __name__ == '__main__':
	v = View()
	v.background_color = 'white'
	v.present('sheet')
	
	c = CustomView()
	v.add_subview(c)
	
	c.polling = True
	
# --------------------

import ui, scene

class TimerView(ui.View):
	class TimerScene(scene.Scene):
		def update(self):
			self.view.superview.update()
			
	def create_sceneview(self):
		scene_view = scene.SceneView()
		scene_view.width = 0
		scene_view.height = 0
		scene_view.frame_interval = self.frame_interval
		scene_view.scene = TimerView.TimerScene()
		return scene_view
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.frame_interval = kwargs.get('frame_interval', 1)
		self.add_subview(self.create_sceneview())
		
	@property
	def start_time(self):
		return self.subviews[0].scene.t
		
	def draw(self):
		pass
		
	def update(self):
		self.set_needs_display()
		
if __name__ == '__main__':
	from time import localtime
	class DigitalClock(TimerView):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
		def draw(self):
			t = localtime()
			ui.draw_string("{:02}:{:02}:{:02}".format(
			t.tm_hour, t.tm_min, t.tm_sec),
			font=('Helvetica', 20),
			rect=(100, 100,0,0),
			alignment=ui.ALIGN_CENTER)
			
	v = DigitalClock(frame=(0,0,300, 300))
	v.present('sheet')
	
# --------------------

import ui
import asyncio
from time import localtime

class DigitalClock(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def draw(self):
		t = localtime()
		ui.draw_string("{:02}:{:02}:{:02}".format(
		t.tm_hour, t.tm_min, t.tm_sec),
		font=('Helvetica', 20),
		rect=(100, 100,0,0),
		alignment=ui.ALIGN_CENTER)
		
	def update(self, event_loop):
		self.set_needs_display()
		event_loop.call_later(.5, self.update, event_loop)
		
v = DigitalClock(frame=(0,0,300, 300), frame_interval=10)
v.present('sheet')

event_loop = asyncio.get_event_loop()
event_loop.call_soon(v.update, event_loop)
event_loop.run_forever()

# --------------------

import ui
import asyncio

class StopWatch(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.value = 0
		self.state = 'stop'
		
	def draw(self):
		t0 = (self.value//(600*60), self.value//600, self.value//10)
		t1 = (t0[0], t0[1]%60, t0[2]%60)
		ui.draw_string("{:02}:{:02}:{:02}".format(*t1),
		font=('Helvetica', 20),
		rect=(150, 0, 0, 0),
		color='black',
		alignment=ui.ALIGN_CENTER)
		
	def update(self, event_loop):
		if self.state == 'run':
			self.value += 1
		self.set_needs_display()
		event_loop.call_later(.1, self.update, event_loop)
		
def button_action(sender):
	v1 = sender.superview['view1']
	if sender.title == 'Reset':
		v1.value = 0
		v1.state = 'stop'
	elif sender.title == 'Start':
		v1.value = 0
		v1.state = 'run'
	elif sender.title == 'Stop':
		v1.state = 'stop'
		
		
v = ui.load_view()
v.present('sheet')

event_loop = asyncio.get_event_loop()
event_loop.call_soon(v['view1'].update, event_loop)
event_loop.run_forever()

# --------------------

def update(self, event_loop):
	if not self.on_screen:
		event_loop.stop()
		return
		
	self.set_needs_display()
	event_loop.call_later(.5, self.update, event_loop)

# --------------------

def button_action(sender):
	event_loop.call_soon(button_action_event_loop, sender)
	
def button_action_event_loop(sender):
	v1 = sender.superview['view1']
	if sender.title == 'Reset':
		v1.value = 0
		v1.state = 'stop'
	elif sender.title == 'Start':
		v1.value = 0
		v1.state = 'run'
	elif sender.title == 'Stop':
		v1.state = 'stop'
		
# --------------------


