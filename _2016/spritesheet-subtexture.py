# https://forum.omz-software.com/topic/3710/how-to-spritesheet-subtexture

from scene import *

class MyScene (Scene):
	def setup(self):
		self.background_color = 'black'
		
		self.sprite_sheet = SpriteNode()
		
		self.sprite_sheet.position = self.size / 2
		self.sprite_sheet.scale = 2
		
		self.sprite_sheet.texture = Texture('plc:Gem_Orange').subtexture(Rect(0,0,.5,.5))
		self.add_child(self.sprite_sheet)
		
	def touch_began(self, touch):
		pass
				
	def Update(self):
		pass
		
run(MyScene(), show_fps = True)

