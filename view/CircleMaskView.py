# coding: utf-8

# https://forum.omz-software.com/topic/2904/share-circle-view-mask-view-food-for-thought

import ui
import photos

class ImageMaskCircle(ui.View):
	def layout(self):
		self.frame = self.superview.bounds
		
	def draw(self):
		# https://forum.omz-software.com/topic/2902/circle-view-for-ui
		# @omz solution
		oval = ui.Path.oval(*self.bounds)
		rect = ui.Path.rect(*self.bounds)
		oval.append_path(rect)
		oval.eo_fill_rule = True
		oval.add_clip()
		ui.set_color('white')
		rect.fill()
		
class TestClass(ui.View):
	def __init__(self, image_mask = None, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.iv = ui.ImageView()
		self.iv.image = ui.Image.from_data(photos.pick_image(raw_data=True))
		self.add_subview(self.iv)
		self.add_subview(image_mask)
		
	def layout(self):
		self.iv.frame = self.bounds
		
if __name__ == '__main__':
	f = (0,0, 80, 80)
	im = ImageMaskCircle()
	tc = TestClass(im, frame = f)
	tc.present('sheet')

