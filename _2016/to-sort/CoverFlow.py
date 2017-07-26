# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/1eb8702f85521004477b

import ui
from PIL import Image
from io import BytesIO
from math import exp, log, copysign, ceil

BGCOLOR = '#0F0F0F'

def pil_to_ui(img):
	b = BytesIO()
	img.save(b, "PNG")
	data = b.getvalue()
	b.close()
	return ui.Image.from_data(data)

				
class CoverFlow(ui.View):
	def __init__(self, images, frame=None):
		self.images = [pil_to_ui(image) for image in images]
		if len(self.images) < 9:
			self.images *= int(ceil(9./len(self.images)))
		if frame:
			self.frame = frame
		self.oldframe = None
		self.background_color = BGCOLOR
		self.prev_frames = []
		
	def layout(self):
		if self.frame != self.oldframe:
			N = 9
			self.frames = []
			#Create frames
			for i in range(N):
				#Thanks to @JonB for this code.
				w=370/1024.*self.width*exp(-2.4*(abs((i-N/2.0+0.5)/N)**(1.38/N**0.25)))
				xc=512/1024.*self.width+copysign(470.0/1024*self.width*log(w/(370.0/1024*self.width)),i-N/2)
				yc= (192/1024.*self.width-w)
				self.frames.append((xc-0.5*w, yc+0.5*w, w, w))
			
			for sv in self.subviews:
				self.remove_subview(sv)
			self.prev_frames = []
			#Create subviews for the minimum of 9 images
			for index, frame in enumerate(self.frames):
				iv = ui.ImageView(frame=frame)
				iv.image = self.images[index]
				self.prev_frames.append(iv.frame)
				self.add_subview(iv)
				if index > 4:
					iv.send_to_back()
					
			#Handle any additional images that are provided
			for i in self.images[9:]:
				iv9 = ui.ImageView(frame=self.frames[-1])
				iv9.image = i
				self.prev_frames.append(iv9.frame)
				self.add_subview(iv9)
				iv9.send_to_back()
			self.oldframe = self.frame
			
	def animate(self):
		len_subviews = len(self.subviews)
		
		for i, sub in enumerate(self.subviews):
			if sub.frame == self.frames[-	1]:
				sub.alpha = 0
			elif sub.frame == self.frames[0]:
				sub.alpha = 1
		
		def anim():
			#Change frames
			for i, sub in enumerate(self.subviews):
				next = (i + (1 if self.touch_direction else -1)) % len_subviews
				sub.frame = self.prev_frames[next]

		#Animate
		ui.animate(anim, 0.25)
		#Re-sort self.images
		if self.touch_direction:
			self.images = [self.images[-1]]+self.images
			self.images.pop(-1)
		else:
			self.images = self.images + [self.images[0]]
			self.images.pop(0)
		
		#Reorder layers based on the fact that biggest images are in front,
		#Bring smallest images to front first
		for s in sorted(self.subviews, key=lambda x: x.frame[3]): s.bring_to_front()
		
		#Reassign prev_frame
		for index, sub in enumerate(self.subviews):
			self.prev_frames[index] = sub.frame
			
	def touch_began(self, touch):
		self.touch_direction = None

	def touch_moved(self, touch):
		if touch.location != touch.prev_location:
			self.touch_direction = int(touch.location[0] > touch.prev_location[0])
		else:
			pass

	def touch_ended(self, touch):
		if self.touch_direction != None:
			#ui.animate(self.anim, duration=0.25)
			self.animate()

if __name__ == '__main__':
	#Pick random images from default textures
	import os, random
	
	app_path = os.path.abspath(os.path.join(os.__file__, '../../../..'))
	
	try:
		os.chdir(app_path + '/Textures')
	except OSError:
		#1.5 compatibility
		app_path = os.path.abspath(os.path.join(os.__file__, '../..'))
		os.chdir(app_path + '/Textures')
	imagenames = os.listdir(os.curdir)
	validnames = []
	for x in imagenames:
		if not (x.startswith('ionicons') or x.startswith('Typicons')):
			validnames.append(x)
	
	#create view
	images = [Image.open(random.choice(validnames)) for x in xrange(15)]
	CoverFlow(images).present()