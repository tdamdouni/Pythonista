# https://forum.omz-software.com/topic/4209/ui-button-inheritance-issue/2

import ui
#import random
from random import choice

Image_One = ui.Image.named('iob:alert_256')
Image_Two = ui.Image.named('iob:alert_circled_256')
PIC_LIST = [Image_One,Image_Two]

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.img_view = None
		self.btn = None
		
		self.make_view()
		
	def make_view(self):
		# create the ui.Image
		self.img_view = ui.ImageView(frame = (150,0,170,110),
		background_color = 'white',
		border_color = 'black',
		border_width = 10)
		# create the ui.Button
		self.btn = ui.Button(frame=(0,0,150,110),
		title='Hit Me',
		action=self.btn_hit)
		
		# add objects to the view
		self.add_subview(self.img_view)
		self.add_subview(self.btn)
		
	def btn_hit(self, sender):
		#self.img_view.image =  PIC_LIST[random.randint(0,1)]
		self.img_view.image = choice(PIC_LIST)
		
if __name__ == '__main__':
	f = (0, 0, 400, 600)
	v = MyClass(frame = f, background_color = 'white')
	v.present(style='sheet')

