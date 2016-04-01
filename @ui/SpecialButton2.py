# coding: utf-8

import ui

class MyButtonClass(ui.View):
	def __init__(self,x,y,width,height,color):
		self.color = color
		self.x = x
		self.y = y
		self.height = height
		self.width = width

	def draw(self):
		path = ui.Path.rect(0, 0, self.width, self.height)
		ui.set_color(self.color)
		path.fill()
		img = ui.Image.named('Girl')
		img.draw()

	def touch_began(self, touch):
		self.color = 'green'
		self.set_needs_display()

	def touch_moved(self, touch):
		self.color = 'white'
		self.set_needs_display()
		
	def touch_ended(self, touch):
		self.color = 'blue'
		self.set_needs_display()

class SpecialButton2(object):
	def __init__(self):
		#self.view = ui.load_view('SpecialButton')
		self.view = ui.View()
		self.view.background_color = 'white'
		self.view.present('fullscreen')
		img = ui.Image.named('Girl')
		width,height = img.size
		img = None
		self.btn = MyButtonClass(100,100,width,height,'red')
		self.view.add_subview(self.btn)

SpecialButton2()
