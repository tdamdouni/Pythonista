# https://forum.omz-software.com/topic/3394/custom-view-class-in-pyui-files-tip

import ui

class OwnerDrawn(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def draw(self):
		s = ui.Path.oval(*self.bounds)
		ui.set_color('red')
		s.fill()
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	# load a standard pyui file as normal. In the pyui file, there is
	# a custom View Control. its Custom View Class property in the
	# pyui file is set to OwnerDrawn.
	v = ui.load_view('Search_bar')
	v.present('sheet')
# --------------------

