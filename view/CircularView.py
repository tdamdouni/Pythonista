# coding: utf-8

# https://forum.omz-software.com/topic/2902/circle-view-for-ui/4

import ui

class CircularView(ui.View):
	def __init__(self):
		pass
		
#    def draw(self):
#        oval = ui.Path.oval(0,0, self.width, self.height)
#        rect = ui.Path.rect(0,0, self.width, self.height)
#        #rect.append_path(oval)
#        ui.Path.add_clip(oval)
#        ui.set_color('white')
#        oval.fill()
		def draw(self):
			oval = ui.Path.oval(*self.bounds)
			rect = ui.Path.rect(*self.bounds)
			oval.append_path(rect)
			oval.eo_fill_rule = True
			oval.add_clip()
			ui.set_color('white')
			rect.fill()
			
if __name__ == '__main__':
	cv = CircularView()
	cv.present('sheet')

