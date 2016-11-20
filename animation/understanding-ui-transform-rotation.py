# https://forum.omz-software.com/topic/3180/understanding-ui-transform-rotation

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
			ui.concat_ctm(ui.Transform.rotation(.45))
			ui.set_color('red')
			s.fill()
			
			
if __name__ == '__main__':
	w = 600
	h = 800
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white')
	mc.present('sheet')
# --------------------

