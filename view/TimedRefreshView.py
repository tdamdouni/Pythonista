# see:  http://omz-forums.appspot.com/pythonista/post/6170731750621184
# code: https://github.com/cclauss/Pythonista_ui/blob/master/TimedRefreshView.py

import datetime, threading, ui

class TimedRefreshView(ui.View):
	def __init__(self):
		self.width = 300
		self.add_subview(self.make_button())
		self.add_subview(self.make_textview())
		self.present('sheet')
		self.refresh_cycle()
		
	def refresh_action(self, sender):
		print('refresh_action({}, {})'.format(self, sender))
		self['textfield'].text = str(datetime.datetime.now())
		
	def refresh_cycle(self):
		if self.on_screen:
			print('tick')
			self.refresh_action(None)
			refresh_thread = threading.Timer(2, self.refresh_cycle).run()
			
	def make_button(self):
		button = ui.Button(name='button', title='Refresh time')
		button.action = self.refresh_action
		button.width  = self.width
		return button
		
	def make_textview(self):
		tf = ui.TextField(name='textfield', frame=self.bounds)
		offset = self['button'].height
		tf.y      += offset
		tf.height -= offset
		tf.border_color = (0, 0, 1)
		tf.border_width = 2
		tf.alignment = ui.ALIGN_CENTER
		tf.text = str(datetime.datetime.now())
		return tf
		
tr_view = TimedRefreshView()

