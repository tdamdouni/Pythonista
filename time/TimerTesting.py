# https://gist.github.com/Phuket2/8eb2e601fb0df240f7713eaa966d361d

from threading import Timer
import threading
import datetime as dt
from datetime import timedelta
import ui

class MyTimer(object):
	def __init__(self, *args, **kwargs):
	
		self.thread = None
		
		
		self.start_time = None
		self.finish_time = None
		self.paused = False
		self.lap = []
		
		self.running = False
		self.interval = 1
		self.count = 0
		self.last_checked = dt.datetime.now()
		
		self.terminated_func = None
		self.finished_func = None
		self.interval_func = None
		
		self.duration = 30
		self.max_iterations = 40
		
		self.interval_func = self.debug_interval_func
		self.finished_func = self.debug_finished_func
		self.terminated_func = self.debug_terminated_func
		
		
	def main_loop(self):
		print('in main_loop')
		self.start_time = dt.datetime.now()
		while True:
			# see if we have been cancelled
			if self.event.isSet():
				self.release()
				return
				
			# check the time between calls. if its less than the interval
			# property, we record the time and do nothing else
			td = dt.datetime.now() - self.last_checked
			if td.seconds < self.interval:
				self.last = dt.datetime.now()
			else:
				# td = a timedelta which we get the number of elpased seconds
				td = dt.datetime.now() - self.start_time
				
				# see if we exceeded the duration
				if self.duration:
					if td.seconds >= self.duration:
						self.finish_time = dt.datetime.now()
						if self.finished_func:
							self.finished_func()
						self.release()
						return
						
				# see if we exceed the max iterations
				if self.max_iterations:
					if self.count >= self.max_iterations:
						self.finish_time = dt.datetime.now()
						self.release()
						return
						
				if self.interval_func:
					if not self.paused:
						self.interval_func(self)
						
				self.last_checked = dt.datetime.now()
				self.count += 1
				
				
	def start_thread(self , sender = None):
		print('in start thread')
		if self.thread:
			if self.thread.isAlive():
				print('thread failed - thread still running') # debug
				return
				
		if self.thread:
			self.thread = None
			
		self.thread =threading.Thread(target = self.main_loop)
		self.event = threading.Event()
		self.thread.start()
		
	def elpased_time(self, sender = None):
		td = dt.datetime.now() - self.start_time
		print(str(td))
		
	def release(self, sender = None):
		# deal with the threading first
		if self.thread:
			if self.thread.isAlive():
				self.event.set()
				
		self.thread = None
		print('released')
		
	def stop(self, sender = None):
		if self.terminated_func:
			self.terminated_func()
		self.event.set()
		
	def debug_finished_func(self):
		print('in debug_finished_func')
		print('duration elapased')
		print(self.elpased_time())
		
	def debug_interval_func(self, timer_obj):
		print('in debug_interval_func -', timer_obj.count)
		
	def debug_terminated_func(self):
		print('in debug_terminated_func -')
		
		
if __name__ == '__main__':
	w = 800
	h = 400
	f = (0, 0, w, h)
	v = ui.View(frame = f, bg_color = 'white', cancel = True)
	def make():
		mt = MyTimer()
		btn = ui.Button()
		btn.title = 'start'
		btn.border_width = .5
		btn.action =mt.start_thread
		btn.frame = (0,0,100,32)
		btn.bg_color = 'pink'
		v.add_subview(btn)
		
		btn = ui.Button()
		btn.title = 'new'
		btn.border_width = .5
		btn.action =mt.elpased_time
		btn.frame = (0,0, 200, 64)
		btn.y = 200
		btn.bg_color = 'orange'
		v.add_subview(btn)
		
		btn = ui.Button()
		btn.title = 'exit'
		btn.border_width = .5
		btn.action =mt.stop
		btn.frame = (0,0, 200, 64)
		btn.y = 250
		btn.bg_color = 'orange'
		v.add_subview(btn)
		
	v.present('sheet', animated = False)
	make()
	#mt = MyTimer()
	#mt.start_thread()

