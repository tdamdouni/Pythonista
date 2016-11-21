#!python2

# https://gist.github.com/C0deH4cker/20403fcfab8cbb3bbf5a

from scene import *
from PIL import Image

import urllib, os

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		load_image('Hamster_Face')
		
		if not os.path.exists("explosion.png"):
		  url = urllib.urlopen("http://i821.photobucket.com/albums/zz133/Roach615/RMXP%20LISTING/Explosion-06.png")
		  with open("explosion.png", "wb") as output:
			  output.write(url.read())
		
		img = Image.open("explosion.png").convert('RGBA')
		self.images = []
		for y in range(5):
			for x in range(5):
				self.images.append(img.crop((x * 96, y * 96, (x+1) * 96, (y+1) * 96)))
		
		self.explode = False
		self.alive = True
	
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		
		if self.explode:
			image(load_pil_image(self.images[self.i]), 115, 200, 96, 96)
			self.i += 1
			if self.i == 25:
				self.explode = False
		
		if self.alive:
			image('Hamster_Face', 115, 200, 96, 96)
	
	def touch_began(self, touch):
		if not self.explode:
			if self.alive:
				self.alive = False
				self.explode = True
				self.i = 0
			else:
				self.alive = True
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

run(MyScene())
