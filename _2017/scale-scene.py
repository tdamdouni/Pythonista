# https://forum.omz-software.com/topic/4098/possible-to-resize-spritenode-image/2

# @ omz I'd recommend setting the scale attribute. Setting the size (as @ccc has shown) would also work, but you would need to set it again when you change the texture of a sprite.
# It might actually be easier to set the scale of the entire scene instead of scaling each card individually.

import scene

class MyScene(scene.Scene):
	def setup(self):
		scene.SpriteNode('card:BackBlue2', parent=self, position=(100, 130))
		scene.SpriteNode('card:BackRed2', parent=self, position=(300, 220), size=(240, 380))
		
if __name__ == '__main__':
	scene.run(MyScene())

