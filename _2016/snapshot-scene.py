# coding: utf-8

import ui
import console
class SnapshotView(ui.View):
	def __init__(self):
		self.frame = (0,0,540,576)
		self.snapshots = []
		lb = ui.Label(frame = (0,0,  self.width, 44))
		lb.text = 'Testing'
		lb.alignment = ui.ALIGN_CENTER
		self.add_subview(lb)
		self.background_color = 'white'
		
	#def draw(self):
		#self.screenshot_action()
		
	# copied from @omz post, made some changes to
	# work in your class
	def take_screenshot(self):
		with ui.ImageContext(self.width, self.height) as c:
			self.draw_snapshot()
			self.snapshots.append(c.get_image())
			
if __name__ == '__main__':
	ssv = SnapshotView()
	ssv.present('sheet')
	ssv.take_screenshot()
	ssv.snapshots[0].show()

