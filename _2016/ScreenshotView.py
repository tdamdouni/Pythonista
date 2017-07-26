# https://github.com/cclauss/Pythonista_ui/blob/master/ScreenshotView.py

import datetime, ui

class ScreenshotView(ui.View):
	def __init__(self):
		self.width = 300
		self.add_subview(self.make_button())
		self.add_subview(self.make_textview())
		self.present('sheet')
		
	def get_shapshot(self):
		with ui.ImageContext(self.width, self.height) as context:
			self.draw_snapshot()
			return context.get_image()
			
	def screenshot_action(self, sender):
		print('Saving screenshots into local files:')
		for i in range(3):  # save three screenshots in a row
			now = str(datetime.datetime.now())
			self['textfield'].text = now
			filename = 'Screenshot_{}.png'.format(now.replace(' ', '_'))
			print('> ' + filename)
			with open(filename, 'wb') as out_file:
				out_file.write(self.get_shapshot().to_png())
				
	def make_button(self):
		button = ui.Button(name='button', title='Save three screenshots')
		button.action = self.screenshot_action
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
		
view = ScreenshotView()

