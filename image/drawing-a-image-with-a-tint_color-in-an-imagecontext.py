# https://forum.omz-software.com/topic/3133/drawing-a-image-with-a-tint_color-in-an-imagecontext

import ui

class MyClass(ui.View):
	def __init__(self, image_name, tint_color = 'black',
	shape_bg_color = 'orange', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.image_name = image_name
		self.image_margin = (20, 20)
		self.tint_color = tint_color
		self.shape_bg_color = shape_bg_color
		
	def draw(self):
		with ui.GState():
			ui.set_color(self.shape_bg_color)
			shape = ui.Path.oval(*self.bounds)
			shape.fill()
			ui.set_color(self.tint_color)
		img = ui.Image.named(self.image_name)
		img_rect = ui.Rect(*self.bounds).inset(*self.image_margin)
		if img:
			img.with_rendering_mode(ui.RENDERING_MODE_TEMPLATE).draw(*img_rect)
			
if __name__ == '__main__':
	wh = 300
	mc = MyClass('iow:ios7_stopwatch_256', frame = (0, 0, wh, wh),
	bg_color = 'purple', shape_bg_color = 'white',
	tint_color = 'black')
	mc.present('sheet')

