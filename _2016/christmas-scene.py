# https://forum.omz-software.com/topic/3926/transparent-scene-background-using-objc_utils/12

from objc_util import *
from scene import *
import ui

glClearColor = c.glClearColor
glClearColor.restype = None
glClearColor.argtypes = [c_float, c_float, c_float, c_float]
glClear = c.glClear
glClear.restype = None
glClear.argtypes = [c_uint]
GL_COLOR_BUFFER_BIT = 0x00004000

def glkView_drawInRect_(_self, _cmd, view, rect):
	glClearColor(1, 0, 0, 0.3)
	glClear(GL_COLOR_BUFFER_BIT)
	
MyGLViewDelegate = create_objc_class('MyGLViewDelegate', methods=[glkView_drawInRect_], protocols=['GLKViewDelegate'])

class ChristmasScene(Scene):
	def setup(self):
		objv = ObjCInstance(self.view)
		objv.glkView().setOpaque_(False)
		sp = SpriteNode('emj:Christmas_Tree', anchor_point=(0,0), position=(500,300), parent=self)
	def draw(self):
		glClearColor(0, 0, 0, 0)
		glClear(GL_COLOR_BUFFER_BIT)

# The rest of the code is the same as the most recent reply. No need to set up a separate delegate. 

#class ChristmasScene(Scene):
	#def setup(self):
		#objv = ObjCInstance(self.view)
		
		#delegate = MyGLViewDelegate.alloc().init()
		#objv.glkView().setDelegate_(delegate)
		#objv.glkView().setOpaque_(False)
		
		#sp = SpriteNode('emj:Christmas_Tree', anchor_point=(0,0), position=(500,300), parent=self)
		
w, h = ui.get_window_size()
webview = ui.WebView(frame=(w/4,0,w/2,h))
webview.load_url('http://google.com')
gameview = SceneView()
gameview.scene = ChristmasScene()

gameview.add_subview(webview)
webview.send_to_back()

gameview.present('full_screen')


