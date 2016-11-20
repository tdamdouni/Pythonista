# coding: utf-8

# https://forum.omz-software.com/topic/3612/how-to-use-a-unicode-character-as-a-movable-object-in-scene

from scene import *
class example(Scene):
	def draw(self):
		image(render_text(str(unichr(9812)), font_size = 80)[0], examplex, exampley)
		
from scene import *
class test(Scene):
	def setup(self):
		self.background_color = 'beige'
		self.test = LabelNode(unichr(9812), 500, 500)
run(test())

from scene import *
class test(Scene):
	def setup(self):
		self.background_color = 'beige'
		self.test = LabelNode(unichr(9812), position=(500, 500), color='black', parent=self)
run(test())

