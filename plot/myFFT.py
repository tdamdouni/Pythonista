# https://gist.github.com/JMV38/ea55e0bb3b47885bb00d

# my FFT

from scene import *
from math import sqrt, sin, pi, floor
import Image, ImageDraw
#import Image

import ImageOps, ImageFilter
import numpy as np

class fftScene (Scene):
	def setup(self):
		self.setupData0()
		self.updateData1( self.pilImg0 )
		self.showTouch = False 
	
	def setupAllData(self):
		# image size
		s = 512
		self.img_size = s
		# now prepare image
		img_name = 'Test_Lenna'
		img = Image.open(img_name)
		img = img.resize((s, s), Image.BILINEAR)
		img = ImageOps.grayscale(img)
		# gray image for pil and RGBA image for scene
		self.pilImg0 = img

	def setupData0(self):
		# image size
		s = 512
		self.img_size = s
		# now prepare image
		img_name = 'Test_Lenna'
		img = Image.open(img_name)
		img = img.resize((s, s), Image.BILINEAR)
		img = ImageOps.grayscale(img)
		# gray image for pil and RGBA image for scene
		self.pilImg0 = img 
		self.sceneImg0 = load_pil_image(img.convert('RGBA'))
		
	def updateData1(self, pilImg):		
		# updates the FFT image from data
		pix = np.array(pilImg) 
		imgFFT = np.fft.fft2(pix)
		imgFFT = np.fft.fftshift(imgFFT)
		imgFFT = np.abs(imgFFT)
		imgFFT = np.log10(imgFFT + 1)
		maxi = np.max(imgFFT)
		mini = np.min(imgFFT)
		imgFFT = (imgFFT-mini) / (maxi-mini) * 255
		self.pilImg1 = Image.fromarray(imgFFT)
		self.sceneImg1= load_pil_image(self.pilImg1.convert('RGBA'))
		
	def draw(self):
		background(0, 0, 0)
		# tx = self.size.w/2 - self.img_size/2
		tx = self.img_size
		ty = self.size.h/2 - self.img_size/2
		image(self.sceneImg0, 0, ty)
		image(self.sceneImg1, tx, ty)
		if self.showTouch :
			fill(1,1,1)
			w = 20
			# ellipse(self.tpos.x-w/2, self.tpos.y-w/2, w, w)
			self.drawCircle(self.tpos.x-tx, self.img_size - (self.tpos.y-ty), w)
			
	def drawCircle(self,x,y,w):
		bbox =  (x - w/2, y - w/2, x + w/2, y + w/2)
		draw = ImageDraw.Draw(self.pilImg1)
		draw.ellipse(bbox, fill=0)
		del draw
		unload_image(self.sceneImg1)
		self.sceneImg1= load_pil_image(self.pilImg1.convert('RGBA'))

	def touch_began(self, touch):
		self.tpos = touch.location
		self.showTouch = True
		
	def touch_moved(self, touch):
		self.tpos = touch.location
				
	def touch_ended(self, touch):
		self.tpos = touch.location
		self.showTouch = False 

if __name__ == "__main__":
	run(fftScene(), frame_interval=1)
