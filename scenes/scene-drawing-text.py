# coding: utf-8

# https://forum.omz-software.com/topic/2945/scene_drawing-text-crashes-python3-beta

import scene, scene_drawing

class P3CrashingScene(scene.Scene):
	def draw(self):
		x, y = self.size / 2
		scene_drawing.text('Python3', x=x, y=y)
		
scene.run(P3CrashingScene())

