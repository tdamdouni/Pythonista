# https://forum.omz-software.com/topic/3180/understanding-ui-transform-rotation/4

import ui

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def draw(self):
		s = ui.Path.rect(100, 100, 200, 200)
		with ui.GState():
			ui.set_color('deeppink')
			s.fill()
			
		with ui.GState():
			# Move the origin (0, 0) to the center of the rectangle:
			ui.concat_ctm(ui.Transform.translation(200, 200))
			# Rotate the coordinate system:
			ui.concat_ctm(ui.Transform.rotation(.45))
			# Move the origin back, so that the rectangle's coordinates are valid:
			ui.concat_ctm(ui.Transform.translation(-200, -200))
			ui.set_color('red')
			s.fill()
			
if __name__ == '__main__':
	w = 600
	h = 800
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white')
	mc.present('sheet')

