# https://forum.omz-software.com/topic/3662/creating-a-sunset-scene/2

from scene import *
import time
import colorsys
colors = []

for i in range(0, 100, 1):
	b = i / 100.0
	color = colorsys.hsv_to_rgb(0.56, 0.88, (b))
	colors.append(color)
	print(color)

i= -1
class sunsetScene(Scene):
	def setup(self):
		# get starting time
		self.start_time = time.time()
		global i
		if i <  (len(colors)-1):
			i+=1
		SpriteNode(anchor_point=(0, 0), color= colors[i], parent=self,
		size=self.size)
		
	def update(self):
		# move to new scene after 2 seconds
		if not self.presented_scene and time.time() - self.start_time > .2:
			self.present_modal_scene(sunsetScene())
			
main_view = SceneView()
main_view.scene = sunsetScene()
main_view.present(hide_title_bar=True, animated=False)

