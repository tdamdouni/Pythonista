# https://forum.omz-software.com/topic/3809/display-gif/15

from scene import *

class MyScene(Scene):
	def setup(self):
		img = 'horse2.gif'
		texture = Texture(img)
		background = SpriteNode(texture)
		background.size = self.size
		background.anchor_point = 0,0
		background.position = 0,0
		self.add_child(background)
		
run(MyScene())

