# https://forum.omz-software.com/topic/3787/provide-button-press-feedback/5

import ui
class myview(ui.View):
	def __init__(self):
		b = ui.Button(name='button_name')
		b.frame=(10,10,32,32)
		b.title = 'test'
		b.background_color = 'green'
		b.action = self.button_tapped
		self.add_subview(b)
	def button_tapped(self,sender):
		sender.background_color = 'gray'
		ui.delay(self.button_tapped_end,1)
	def button_tapped_end(self):
		self['button_name'].background_color = 'green'
		
v = myview()
v.present()

