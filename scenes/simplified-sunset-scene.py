# https://forum.omz-software.com/topic/3662/creating-a-sunset-scene/4

# @omz

from scene import *
import colorsys

class SunsetScene(Scene):
	def setup(self):
		self.background_color = 'black'
		self.b = 0.0
		
	def update(self):
		# NOTE: self.t is a built-in timestamp variable, no need to calculate this yourself.
		if self.t > 0.1:
			self.background_color = colorsys.hsv_to_rgb(0.56, 0.88, self.b)
			self.b += 0.005
			
main_view = SceneView()
main_view.scene = SunsetScene()
main_view.present(hide_title_bar=True, animated=False)

