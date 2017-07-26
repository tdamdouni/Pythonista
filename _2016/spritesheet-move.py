# https://forum.omz-software.com/topic/3710/how-to-spritesheet-subtexture/4

from scene import *

gem_texture = [
Texture('plc:Gem_Orange').subtexture(Rect(0,.5,.5,.5)),
Texture('plc:Gem_Orange').subtexture(Rect(.5,.5,.5,.5)),
Texture('plc:Gem_Orange').subtexture(Rect(0,0,.5,.5)),
Texture('plc:Gem_Orange').subtexture(Rect(.5,0,.5,.5)),
]

class MyScene (Scene):
	def setup(self):
		self.background_color = 'black'
		self.gem = SpriteNode(gem_texture[0],
		scale = 4,
		position = self.size / 2,
		parent = self)
		
	def touch_began(self, touch):
		pass
		
	def update(self):
		# Update should change from gem_texture[0], in setup, to gem_texture[3], in update(). Its not changing it... is this not possible or am I missing something?
		self.gem.texture = gem_texture[3]

run(MyScene(), show_fps = True)
