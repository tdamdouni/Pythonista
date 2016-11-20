# coding: utf-8

# https://forum.omz-software.com/topic/3124/using-my-own-images-in-the-scene-module-help-would-be-appreciated

from scene import *

class Game (Scene):
	def setup(self):
		self.background_color = '#000000'
		ground = Node(parent=self)
		x = 0
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Ground_SnowMid', position=(x, 0))
			ground.add_child(tile)
			x += 64
		self.player = SpriteNode('') #This is where I want to add an image of my own.
		self.player.anchor_point = (0.5, 0)
		self.player.position = (self.size.w/2, 32)
		self.add_child(self.player)
		
if __name__ == '__main__':
	run(Game(), LANDSCAPE, show_fps=True)
	
# ui.Image.named(my_image_name)

# That's not quite correct. SpriteNode either takes a scene.Texture object or a string (which is basically a shortcut for Texture(image_name)). You could also create a Texture from a ui.Image, but that wouldn't be necessary here (that's basically just for drawing custom shapes etc. without a corresponding image file).

# When you import a photo, it gets a file name in the library. It should be possible to just replace 'plf:Ground_SnowMid' with something like 'Image01.jpg' (or whatever the name of your imported photo is). Note that the extension (jpg, png...) is required, and that the name is case-sensitive, so if the filename is 'IMAGE.JPG', using 'image.jpg' wouldn't work. Files from the photo library tend to have all-uppercase names.

