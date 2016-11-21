# https://gist.github.com/Phuket2/bda7d14d4581dd535370687ac6a9a598

import ui
import datetime as dt
from time import time, strftime

_sfn = 'Arial Rounded MT Bold'

def current_time_str():
	return strftime('%H:%M:%S')
	
def _make_label(name, text, font, color):
	lb = ui.Label(name ='head')
	lb.text = text
	lb.font = font
	lb.text_color = color
	lb.size_to_fit()
	return lb
	
class DashBoardPanel(ui.View):
	# add more functionality to the base class
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.header = None
		self.border_color = 'black'
		self.border_width = 2
		self.corner_radius = 6
		
	def make_title(self, title_text):
		lb = _make_label('head', title_text, (_sfn, 22), 'red' )
		lb.x = (self.width / 2) - (lb.width / 2)
		lb.y = 10
		self.header = lb
		self.add_subview(lb)
		
	def update(self):
		pass
		
		
class TimePanel(DashBoardPanel):
	def __init__(self, *args, **kwargs):
		DashBoardPanel.__init__(self, *args, **kwargs)
		self.time_lb = None
		
		self.make_title('Current Time')
		self.make_time_display()
		
	def make_time_display(self):
		lb = _make_label('time', current_time_str(), (_sfn, 32), 'darkblue' )
		lb.x = (self.width / 2) - (lb.width / 2)
		lb.y = 40
		self.time_lb = lb
		self.add_subview(lb)
		
	def update(self):
		self.time_lb.text = current_time_str()
		
		
class WeatherPanel(DashBoardPanel):
	def __init__(self, *args, **kwargs):
		DashBoardPanel.__init__(self, *args, **kwargs)
		
		
		self.make_title('My Weather')
		
class TwitterFeed(DashBoardPanel):
	def __init__(self, *args, **kwargs):
		DashBoardPanel.__init__(self, *args, **kwargs)
		self.make_title('Twitter')
		self.header.text_color = 'orange'
		
class DashBoard(ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.panels = []
		self.updates_running = False
		
		self.make_view()
		
	def make_view(self):
		lb = _make_label('head', 'My DashBoard', (_sfn, 36), 'darkblue' )
		lb.x = (self.width / 2) - (lb.width / 2)
		lb.y = 10
		self.add_subview(lb)
		
	def add_panel(self, panel):
		self.panels.append(panel)
		self.add_subview(panel)
		
	def start_panel_updates(self):
		if self.updates_running:
			return
			
		self.updates_running = True
		ui.delay(self.do_updates, 0)
		
	def do_updates(self):
		if not self.on_screen:
			ui.cancel_delays()
			return
			
		# the panel base class has a update() method that just passes.
		# so its safe to call the method. it needs to be overriden in the
		# child class for it to do anything.
		for panel in self.panels:
			panel.update()
			
		ui.delay(self.do_updates, 1)
		
	def layout(self):
		# normally would position the panels here, to be orientation
		# friendly and screen size friendly. Just hard coded in this
		# example
		pass
		
		
		
if __name__ == '__main__':
	f = (0, 0, 800, 600)
	db = DashBoard(frame = f, bg_color = 'lightblue')
	tp = TimePanel(frame =(20, 100, 200, 100), bg_color = 'white')
	db.add_panel(tp)
	
	f = (tp.x + tp.width + 20, tp.y, 200, 100)
	wp = WeatherPanel(frame = f, bg_color = 'white')
	db.add_panel(wp)
	
	f = (wp.x + wp.width + 20, wp.y, 200, 100)
	twp = TwitterFeed(frame = f, bg_color = 'lightyellow')
	db.add_panel(twp)
	
	
	db.present('sheet')
	
	db.start_panel_updates()

