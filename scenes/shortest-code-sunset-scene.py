# https://forum.omz-software.com/topic/3662/creating-a-sunset-scene/5

# @omz

from scene import *
import colorsys
A = Action

class SunsetScene(Scene):
	def setup(self):
		self.background_color = 'black'
		def transition(node, p):
			node.background_color = colorsys.hsv_to_rgb(0.56, 0.88, p)
		self.run_action(A.sequence(A.wait(0.1), A.call(transition, 1.0)))
		
main_view = SceneView()
main_view.scene = SunsetScene()
main_view.present(hide_title_bar=True, animated=False)

