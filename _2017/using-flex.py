# https://forum.omz-software.com/topic/4344/flex-and-ui-object-initial-settings-chicken-before-egg

from ui import *

class MyView(View):
	def __init__(self):
		self.background_color = 'white'
		
		yellow = View(background_color='yellow', flex='RBW')
		yellow.frame = (20, 20, self.width - 20, 60)
		self.add_subview(yellow)
		
v = MyView()
v.present('fullscreen')

