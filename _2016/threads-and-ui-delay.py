# https://forum.omz-software.com/topic/3849/threads-and-ui-delay

from requests_futures.sessions import FuturesSession
from concurrent.futures import *
import re
import ui
import requests

class SyncBackend (object):
	URL = 'http://tycho.usno.navy.mil/cgi-bin/timer.pl'
	RE_TIME = re.compile('<BR>(.*?)\t.*Universal Time')
	
	def __init__(self, time_callback):
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.time = ''
		self.cb = time_callback
		self.running = True
		self.run_one()
		
	def run_one(self):
		self.future = self.executor.submit(self.worker)
		self.future.add_done_callback(self.callback)
		
	def worker(self):
		resp =  requests.get(self.URL)
		return self.RE_TIME.search(resp.text).group(1)
		
	def callback(self, future_state):
		try:
			self.time = future_state.result()
			self.cb(self.time)
		except Exception as e:
			print(e)
		if self.running:
			self.run_one()
			
	def cancel(self):
		self.running = False
		
class TestView(ui.View):

	def __init__(self):
		self.create_layout()
		
		self.request_counter = 0
		self.sync = SyncBackend(self.callback)
		
		self.counter = 0
		ui.delay(self.increment_counter, 0.05)
		
	def increment_counter(self):
		self.counter += 1
		self.counter_label.text = str(self.counter)
		
		ui.delay(self.increment_counter, 0.05)
		
	def callback(self, new_time):
		self.request_counter += 1
		self.time_label.text = str(self.request_counter) + ' - ' + new_time
		
	def will_close(self):
		self.sync.cancel()
		
	def create_layout(self):
		self.background_color = 'white'
		self.counter_label = ui.Label()
		self.time_label = ui.Label()
		self.counter_label.width = self.time_label.width = 300
		self.counter_label.height = self.time_label.height = 200
		self.counter_label.center = (self.width * 0.5, self.height * 0.3)
		self.time_label.center = (self.width * 0.5, self.height * 0.6)
		self.counter_label.flex = self.time_label.flex = 'LRTB'
		self.counter_label.text_color = self.time_label.text_color = 'black'
		self.counter_label.text = self.time_label.text = 'Start'
		self.add_subview(self.counter_label)
		self.add_subview(self.time_label)
		
v = TestView()
v.present('sheet')

