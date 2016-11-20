# https://forum.omz-software.com/topic/3247/share-code-round-button

import ui, editor

def round_btn(w, title, factor=.7):
	btn = ui.Button(frame=(0, 0, w, w))
	btn.title = title
	btn.font = ('Arial Rounded MT Bold', w * factor)
	btn.corner_radius = btn.width / 2
	
	btn.bg_color = 'deeppink'
	btn.tint_color = 'white'
	
	return btn
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs) py3 only
		ui.View.__init__(self, *args, **kwargs)
		btn = round_btn(self.width * .8, 'IJ')
		btn.center = self.bounds.center()
		btn.y -= 22 # i will never figure out center :( i dont get it
		btn.touch_enabled = False
		self.add_subview(btn)
		
if __name__ == '__main__':
	factor = 1
	w = 375 * factor
	h = 667 * factor
	f = (0, 0, w, h)
	mc = MyClass(frame=f, bg_color = 'white')
	mc.present('sheet')
	#editor.present_themed(mc, theme_name='Cool Glow',
																																																																																								#style = 'sheet', animated=False)
# --------------------

