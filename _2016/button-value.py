# https://forum.omz-software.com/topic/3792/simple-button-to-choose-path/2

import ui
class myview(ui.View):
	def __init__(self):
		b1 = ui.Button()
		b1.frame=(10,10,100,32)
		b1.title = 'path1'
		b1.action = self.button_tapped
		self.add_subview(b1)
		b2 = ui.Button()
		b2.frame=(120,10,100,32)
		b2.title = 'path2'
		b2.action = self.button_tapped
		self.add_subview(b2)
	def button_tapped(self,sender):
		path = sender.title
		print(path)
v = myview()
v.present()

