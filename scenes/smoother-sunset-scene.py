# https://forum.omz-software.com/topic/3662/creating-a-sunset-scene/3

from scene import *
import time
import colorsys
colors = []

for i in range(0, 100, 1):
	b = i / 100.0
	color = colorsys.hsv_to_rgb(0.56, 0.88, (b))
	colors.append(color)
	
	
i = 0
class sunsetScene(Scene):
	def setup(self):
		# get starting time
		self.start_time = time.time()
		global i
		self.background_color = 'black'
		
	def update(self):
		global i
		# update background color after .1 seconds
		if time.time() - self.start_time > .1:
		
			self.background_color = colors[i]
			if i <  (len(colors)-1):
				i+=1
			self.start_time = time.time()
			
			
main_view = SceneView()
main_view.scene = sunsetScene()
main_view.present(hide_title_bar=True, animated=False)```

