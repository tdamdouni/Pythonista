# coding: utf-8

# https://forum.omz-software.com/topic/2196/cover-flow-view/38

import ui
from PIL import Image
from io import BytesIO
from time import sleep
from math import exp, log, copysign, ceil

BGCOLOR = '#0F0F0F'

def pil_to_ui(img):
	b = BytesIO()
	img.save(b, "PNG")
	data = b.getvalue()
	b.close()
	return ui.Image.from_data(data)
	
	
class CoverFlow(ui.View):
	def __init__(self, images):
		self.images = [pil_to_ui(image) for image in images]
		if len(self.images) < 9:
			self.images *= int(ceil(9./len(self.images)))
		self.frame = (0, 0, 1024, 768)
		self.oldframe = (0, 0, 1024)
		self.background_color = BGCOLOR
		#Make frames for all views
		N = 9
		frames = []
		#Create frames
		for i in xrange(N):
			#Thanks to @JonB for this code.
			w=370/1024.*self.width*exp(-2.4*(abs((i-N/2.0+0.5)/N)**(1.38/N**0.25)))
			xc=512/1024.*self.width+copysign(470.0/1024*self.width*log(w/(370.0/1024*self.width)),i-N/2)
			yc= (192/1024.*self.width-w)
			frames.append((xc-0.5*w, yc+0.5*w, w, w))
			
		#Create subviews for the minimum of 9 images
		for index, frame in enumerate(frames):
			iv = ui.ImageView(frame=frame)
			iv.image = self.images[index]
			iv.prev_frame = iv.frame
			self.add_subview(iv)
			if index > 4:
				iv.send_to_back()
				
		#Handle any additional images that are provided
		for i in self.images[9:]:
			iv9 = ui.ImageView(frame=frames[-1])
			iv9.image = i
			iv9.prev_frame = iv9.frame
			self.add_subview(iv9)
			iv9.send_to_back()
			
	def layout(self):
		if self.frame != self.oldframe:
			N = 9
			frames = []
			#Create frames
			for i in range(N):
				#Thanks to @JonB for this code.
				w=370/1024.*self.width*exp(-2.4*(abs((i-N/2.0+0.5)/N)**(1.38/N**0.25)))
				xc=512/1024.*self.width+copysign(470.0/1024*self.width*log(w/(370.0/1024*self.width)),i-N/2)
				yc= (192/1024.*self.width-w)
				frames.append((xc-0.5*w, yc+0.5*w, w, w))
				
			for sv in self.subviews:
				self.remove_subview(sv)
			#Create subviews for the minimum of 9 images
			for index, frame in enumerate(frames):
				iv = ui.ImageView(frame=frame)
				iv.image = self.images[index]
				iv.prev_frame = iv.frame
				self.add_subview(iv)
				if index > 4:
					iv.send_to_back()
					
			#Handle any additional images that are provided
			for i in self.images[9:]:
				iv9 = ui.ImageView(frame=frames[-1])
				iv9.image = i
				iv9.prev_frame = iv9.frame
				self.add_subview(iv9)
				iv9.send_to_back()
			self.oldframe = self.frame
			
	def anim(self):
		#Change frames
		len_subviews = len(self.subviews)
		for i, sub in enumerate(self.subviews):
			next = self.subviews[(i + (1 if self.touch_direction else -1)) % len_subviews]
			sub.frame = next.prev_frame
		for sub in self.subviews:
			sub.prev_frame = sub.frame
			
		#Resort self.images
		if self.touch_direction:
			self.images = [self.images[-1]]+self.images
			self.images.pop(-1)
		else:
			self.images = self.images + [self.images[0]]
			self.images.pop(0)
		#Reorder layers based on the fact that biggest images are in front
		#Bring smallest images to front first
		for s in sorted(self.subviews, key=lambda x: x.frame[3]): s.bring_to_front()
		
	def touch_began(self, touch):
		self.touch_direction = None
		
	def touch_moved(self, touch):
		if touch.location != touch.prev_location:
			self.touch_direction = int(touch.location.x > touch.prev_location.x)
		else:
			pass
			
	def touch_ended(self, touch):
		if self.touch_direction != None:
			ui.animate(self.anim, duration=0.25)
			
if __name__ == '__main__':
	#Pick random images from default textures
	import os, random
	app_path = os.path.abspath(os.path.join(os.__file__, '../../../..'))
	os.chdir(app_path + '/Textures')
	imagenames = os.listdir(os.curdir)
	validnames = []
	for x in imagenames:
		if not (x.startswith('ionicons') or x.startswith('Typicons')):
			validnames.append(x)
			
	images = [Image.open(random.choice(validnames)) for x in xrange(15)]
	view = ui.View(background_color=BGCOLOR)
	cf = CoverFlow(images)
	view.add_subview(cf)
	cf.present(hide_title_bar=1)

