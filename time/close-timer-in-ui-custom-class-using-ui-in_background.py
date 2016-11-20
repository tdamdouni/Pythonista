# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2489/close-timer-in-ui-custom-class-using-ui-in_background_

import ui
import datetime, time

class Test (ui.View):
	def __init__(self, duration = 1.0):
		self.frame = (0,0,300,300)
		self.background_color = 'white'
		btn = ui.Button(title = 'start')
		btn.width = 100
		btn.border_width = .5
		# hmmmmmmm, center does not work ( as you would expect it too )
		# eg. btn.center = self.center
		btn.center = (self.center[0], self.center[1] - (44/2))
		btn.action = self.auto_close_timer
		self.add_subview(btn)
		self.auto_close_duration = float(duration)
		
	@ui.in_background
	def auto_close_timer(self, sender):
		# try to stay responsive regardless of the time
		# set.  its not meant to be exact, but its very close
		# for this close enough
		sender.enabled = False
		n = self.auto_close_duration
		st = datetime.datetime.now()
		while True:
			n -= self.auto_close_duration / 10.
			if n < 0.0 : break
			time.sleep(self.auto_close_duration / 10.)
		#print datetime.datetime.now() - st
		self.name = str(datetime.datetime.now() - st)
		sender.enabled = True
		
		
if __name__ == '__main__':
	t = Test(1.5)
	t.present('sheet')
	
### ---

import ui
import datetime, time

class Test (ui.View):
	def __init__(self, duration = 1.0):
		self.frame = (0,0,300,300)
		self.background_color = 'white'
		btn = ui.Button(title = 'start')
		btn.width = 100
		btn.border_width = .5
		# hmmmmmmm, center does not work ( as you would expect it too )
		# eg. btn.center = self.center
		btn.center = (self.center[0], self.center[1] - (44/2))
		btn.action = self.auto_close_timer
		self.add_subview(btn)
		self.auto_close_duration = float(duration)
		
	@ui.in_background
	def auto_close_timer(self, sender):
		# try to stay responsive regardless of the time
		# set.  its not meant to be exact, but its very close
		# for this close enough
		sender.enabled = False
		n = self.auto_close_duration
		st = datetime.datetime.now()
		while True:
			n -= self.auto_close_duration / 10.
			if n < 0.0 : break
			time.sleep(self.auto_close_duration / 10.)
		#print datetime.datetime.now() - st
		self.name = str(datetime.datetime.now() - st)
		sender.enabled = True
		
		
if __name__ == '__main__':
	t = Test(1.5)
	t.present('sheet')
	
###==============================

import ui
import datetime, time

class Test (ui.View):
	def __init__(self, duration = 1.0):
		self.frame = (0,0,300,300)
		self.background_color = 'white'
		btn = ui.Button(title = 'start')
		btn.width = 100
		btn.border_width = .5
		# hmmmmmmm, center does not work ( as you would expect it too )
		# eg. btn.center = self.center
		btn.center = (self.center[0], self.center[1] - (44/2))
		btn.action = self.JonB_way
		self.fire_obj = btn
		self.add_subview(btn)
		self.auto_close_duration = float(duration)
		self.start = None
		
	def JonB_way(self, sender):
		self.fire_obj.enabled = False
		self.start = datetime.datetime.now()
		ui.delay(self.fire_delay, self.auto_close_duration)
		
	def fire_delay(self):
		self.name = str(datetime.datetime.now() - self.start)
		self.fire_obj.enabled = True

