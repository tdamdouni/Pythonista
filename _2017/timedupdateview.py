# https://forum.omz-software.com/topic/4109/polling-from-a-ui-view-built-in-timers-in-ui-views/36

import ui
import threading
import speech
from random import randint

class TimedUpdateView(ui.View):

	def __init__(self):
		self.updatex_interval = 5
		self.update_after_delay()
		
	def updatex(self):
		""" Say a random digit from 0 to 9 every 5 seconds. """
		speech.say('%s' % (randint(0, 9)))
		
	def update_after_delay(self):
		""" This just method calls the update method periodically """
		self.updatex()
		update_thread = threading.Timer(self.updatex_interval,
		self.update_after_delay).run()
		
if __name__ == "__main__":
	v = TimedUpdateView()
	v.present('sheet')

