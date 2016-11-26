# https://forum.omz-software.com/topic/1487/is-it-possible-to-hide-the-stop-cross-in-the-upper-lefthand-corner

# @omz

# hide_title_bar=True not working on Pythonista3

from scene import *

class MyScene (Scene):
	def draw(self):
		background(0, 0, 1)
		
view = SceneView()
view.scene = MyScene()
view.present('fullscreen', hide_title_bar=True)

