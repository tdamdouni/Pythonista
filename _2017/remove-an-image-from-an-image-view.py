# https://forum.omz-software.com/topic/4329/image-image-nil

# remove an image from an image view

from ui import *


class MyView(View):
	def __init__(self):
		self.width = 320
		self.height = 320
		
		iv = ImageView()
		iv.background_color = '#ffff00'
		iv.width = 50
		iv.height = 50
		iv.center = self.center
		iv.image = Image('iob:folder_24')
		self.add_subview(iv)
		self.iv = iv
		
		b = Button()
		b.title = 'Remove Me'
		b.width = 100
		b.height = 44
		b.center = self.center
		b.y = self.bounds.y + 10
		b.action = self.remove_image
		self.add_subview(b)
		
	def remove_image(self, sender):
		self.iv.image = None
		
view = MyView()
view.present('sheet')

