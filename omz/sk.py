# https://forum.omz-software.com/topic/2801/spritekit/7

from objc_util import *
import ui
from  SKExample import *

class MyView (ui.View):
	def __init__(self):
		self.flex = 'WH'
		
		global skview
		z = ui.get_screen_size()
		self.background_color = '#b3cdff'
		
		skview = createSKView(0,0, z.width,z.height -64)
		sz = CGSize(z.width, z.height-64)
		scene = createSampleScene(sz)
		skview.presentScene_(scene)
		
		self_objc = ObjCInstance(self)
		self_objc.addSubview_(skview)
		
		
	def will_close(self):
		global skview
		skview.paused = True
		#skview.presentScene_(None)
		#skview = None
		
		
		
if __name__ == '__main__':
	v = MyView()
	v.present('fullscreen')

