# coding: utf-8

# https://forum.omz-software.com/topic/3107/two-instances-of-labels-updated-by-time

import ui
import datetime as dt

class TimerExample(ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.timer1_label = None
		self.timer1_start_time= 0
		self.timer1_btn = None
		self.timer1_running = False
		self.make_view()
		
	def make_view(self):
		lb = ui.Label()
		lb.font = ('Arial Rounded MT Bold', 44)
		lb.alignment = ui.ALIGN_CENTER
		lb.text = '00:00:00'
		lb.size_to_fit()
		lb.x = 10
		lb.y = 10
		
		self.add_subview(lb)
		self.timer1_label = lb
		
		btn= ui.Button()
		btn.font = lb.font
		btn.title = 'Start'
		btn.border_width = 2
		btn.corner_radius = 6
		btn.size_to_fit()
		btn.x = lb.x + lb.width + 20
		self.add_subview(btn)
		btn.action = self.toggle_timer1
		self.timer1_btn = btn
		
		
	def update_timer1(self):
		if not self.timer1_running:
			return
			
		td = dt.datetime.now() - self.timer1_start_time
		self.timer1_label.text = str(td.seconds)
		ui.delay(self.update_timer1, 1)
		
		
	def toggle_timer1(self, sender):
		if not self.timer1_running:
			self.timer1_running = True
			self.timer1_btn.title = 'Stop'
			self.timer1_start_time = dt.datetime.now()
			ui.delay(self.update_timer1, 0)
		else:
			self.timer1_running = False
			ui.cancel_delays()
			self.timer1_btn.title = 'Start'
			
	def will_close(self):
		# window is going to close save anything you need to here
		# also stop ui.delay
		ui.cancel_delays()
		self.timer1_running = False
		
		
		
		
if __name__ == '__main__':
	f = (0, 0, 600, 800)
	v = TimerExample(frame = f, bg_color = 'white')
	v.present('sheet')

