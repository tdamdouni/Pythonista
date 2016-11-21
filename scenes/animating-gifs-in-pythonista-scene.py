# coding: utf-8

# https://gist.github.com/balachandrana/c1580fff9477d58fd0cf25c898471597

# https://forum.omz-software.com/topic/3256/support-for-animated-gifs-in-scene-module/3

import scene
import ui
from PIL import Image as PILImage

class MyScene (scene.Scene):
	def setup(self):
		self.im = PILImage.open('tunnelswirl.gif')
		self.mypalette = self.im.getpalette()
		self.savefile = 'tmp.png'
		self.toggle_state = False
		self.sprite = scene.SpriteNode(scene.Texture(ui.Image.named('Snake')),
		position=self.size/2,
		parent=self)
		
	def update(self):
		if self.toggle_state:
			try:
				self.im.putpalette(self.mypalette)
				new_im = PILImage.new("RGBA", self.im.size)
				new_im.paste(self.im)
				new_im.save(self.savefile)
				self.sprite.texture = scene.Texture(ui.Image.named(self.savefile))
				self.im.seek(self.im.tell()+1)
			except EOFError:
				self.im.seek(0)
				#self.im.close()
				#self.im = PILImage.open('tunnelswirl.gif')
				#self.mypalette = self.im.getpalette()
				
	def touch_began(self, touch):
		self.toggle_state = not self.toggle_state
		if not self.toggle_state:
			self.sprite.texture = scene.Texture(ui.Image.named('Snake'))
			
scene.run(MyScene(), show_fps=True)

