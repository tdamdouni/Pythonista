# https://forum.omz-software.com/topic/3662/creating-a-sunset-scene

from scene import *
import time

class FirstScene(Scene):
	def setup(self):
		self.start_time = time.time()
		SpriteNode(anchor_point=(0, 0), color='white', parent=self, size=self.size)

def update(self):
	newColor = ['blue','green']
	if not self.presented_scene and time.time() - self.start_time > 2:
		SpriteNode(anchor_point=(0, 0), color= newColor[0], parent=self,
		size=self.size)
		self.start_time = time.time()
	if not self.presented_scene and time.time() - self.start_time > 2:
		SpriteNode(anchor_point=(0, 0), color= newColor[1], parent=self,
		size=self.size)
main_view = SceneView()
main_view.scene = FirstScene()
main_view.present(hide_title_bar=True, animated=False)

