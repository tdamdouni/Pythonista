# coding: utf-8
# Initial coding based on following url
# http://stackoverflow.com/questions/10269099/pil-convert-gif-frames-to-jpg
# Does not work for all gifs
#current code based on the following
#https://gist.github.com/BigglesZX/4016539
#some discussion and code here
#http://stackoverflow.com/questions/14550055/loss-of-data-when-extracting-frames-from-gif-to-png
#not all gifs work
#see the discussion in the pythonista forum
#https://forum.omz-software.com/topic/3256/support-for-animated-gifs-in-scene-module

import scene
import ui
from PIL import Image as PILImage
from PIL import ImageSequence
from io import BytesIO

class GifSpriteNode(scene.SpriteNode):
	def __init__(self, giffile, preload=False, *args, **kwargs):
		self.giffile = giffile
		self.mode = self.analyze_image()
		self.preload = preload
		self.pilimage = PILImage.open(giffile)
		self.palette = self.pilimage.getpalette()
		self.savefile = BytesIO()
		self.min_duration = 1.0/60
		self.default_duration = 1.0/60
		self.current_duration = self.default_duration
		self.last_frame = self.pilimage
		texture, duration = self.get_texture_and_duration()
		super(GifSpriteNode, self).__init__(texture, *args, **kwargs)
		self.orig_size = self.size
		self.preloaded_textures = []
		self.current_texture_index = 0
		if self.preload:
			while 1:
				self.preloaded_textures.append((texture, duration))
				try:
					self.pilimage.seek(self.pilimage.tell()+1)
					texture, duration = self.get_texture_and_duration()
					self.preloaded_textures.append((texture, duration))
				except EOFError:
					break
					
	def analyze_image(self):
		'''
		Pre-process pass over the image to determine the mode (full or additive).
		Necessary as assessing single frames isn't reliable. Need to know the mode
		before processing all frames.
		'''
		im = PILImage.open(self.giffile)
		results = {
		'size': im.size,
		'mode': 'full',
		}
		try:
			while True:
				if im.tile:
					tile = im.tile[0]
					update_region = tile[1]
					update_region_dimensions = update_region[2:]
					if update_region_dimensions != im.size:
						results['mode'] = 'partial'
						break
				im.seek(im.tell() + 1)
		except EOFError:
			pass
		return results['mode']
		
	def update(self, dt):
		self.current_duration -= dt
		if self.current_duration > self.min_duration:
			return
		if self.preload:
			self.current_texture_index = (self.current_texture_index + 1)%len(
			self.preloaded_textures)
			self.texture, self.current_duration = self.preloaded_textures[
			self.current_texture_index]
		else:
			try:
				self.texture, self.current_duration = self.get_texture_and_duration()
				self.pilimage.seek(self.pilimage.tell()+1)
			except EOFError:
				self.pilimage.seek(0)
		self.size = self.orig_size
		
	def get_texture_and_duration(self):
		if not self.pilimage.getpalette():
			self.pilimage.putpalette(self.palette)
		duration = self.pilimage.info['duration']/100.0
		if duration <= 0:
			duration = self.default_duration
		new_im = PILImage.new("RGBA", self.pilimage.size)
		if self.mode == 'partial':
			new_im.paste(self.last_frame)
		new_im.paste(self.pilimage, (0,0), self.pilimage.convert('RGBA'))
		self.last_frame = new_im
		self.savefile.seek(0)
		new_im.save(self.savefile, format='PNG')
		return (scene.Texture(ui.Image.from_data(self.savefile.getvalue())), duration)
		
		
if __name__ == '__main__':
	class MyScene (scene.Scene):
		def setup(self):
			self.toggle_state = False
			self.sprite0 = scene.SpriteNode(scene.Texture(ui.Image.named('Snake')),
			position=self.size/2,
			parent=self)
			'''self.sprite1 = GifSpriteNode('tunnelswirl.gif', preload=False,
			position=self.size/2)'''
			self.sprite1 = GifSpriteNode('tunnelswirl.gif', preload=True,
			position=self.size/2)
			'''self.sprite1 = GifSpriteNode('tumblr_mh8uaqMo2I1rkp3avo2_250.gif', preload=True,
			position=self.size/2)'''
			'''self.sprite1 = GifSpriteNode('EBY-nanoface-Pennywise-03k-40x.gif', preload=False,
			size=(400, 400),
			position=self.size/2)'''
			#gif from wikipedia gif page
			'''self.sprite1 = GifSpriteNode('Rotating_earth_(large).gif', preload=False,
			position=self.size/2)'''
			'''self.sprite1 = GifSpriteNode('9HjM5.gif', preload=True,
			position=self.size/2)'''
			'''self.sprite1 = GifSpriteNode('test_image1.gif', preload=True,
			position=self.size/2)'''
			
		def update(self):
			if self.toggle_state:
				self.sprite1.update(self.dt)
				
		def touch_began(self, touch):
			self.toggle_state = not self.toggle_state
			if self.toggle_state:
				self.sprite0.remove_from_parent()
				self.add_child(self.sprite1)
			else:
				self.sprite1.remove_from_parent()
				self.add_child(self.sprite0)
				
	scene.run(MyScene(), show_fps=True)

