# https://forum.omz-software.com/topic/4108/how-do-i-convert-a-ui-image-into-a-scene-spritenode

import scene

def make_oval_sprite(width=100, height=100, fg_color='blue', bg_color='grey'):
	with scene.ui.ImageContext(width, height) as ctx:
		scene.ui.set_color(bg_color)
		scene.ui.Path.rounded_rect(0, 0, width, height, height / 10).fill()
		scene.ui.set_color(fg_color)
		scene.ui.Path.oval(0, 0, width, height).fill()
		return ctx.get_image()
		return scene.Texture(ctx.get_image())
		
class MyScene(scene.Scene):
	def setup(self):  # scene.SpriteNode() wants an image name, not an image.
		scene.SpriteNode(make_oval_sprite(), parent=self, position=(200,200))
		
scene.run(MyScene())
# make_oval_sprite().show()

