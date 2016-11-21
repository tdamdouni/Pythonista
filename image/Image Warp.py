# https://gist.github.com/jefflovejapan/5076080

# Image Warp
#
# Demonstrates an interesting use of the image_quad function
# to distort an image based on touch.

from scene import *
from math import sqrt, sin, pi, floor
import Image

M = 16 # number of vert. and horiz. quads in the mesh (16*16=256)

class ImageWarp (Scene):
	def setup(self):
		self.offsets = [[(0.0, 0.0) for x in xrange(M+1)] for y in xrange(M+1)]
		if self.size.w >= 700:
			# Use the original image on iPad:
			self.img = 'Test_Lenna'
			s = 512
		else:
			# Resize the image for small screens:
			s = 256
			img_name = 'Test_Lenna'
			img = Image.open(img_name).convert('RGBA')
			img = img.resize((s, s), Image.BILINEAR)
			self.img = load_pil_image(img)
		self.img_size = s
		self.m = s / M
		
	def draw_warped_image(self):
		m = self.m
		for x in xrange(M):
			for y in xrange(M):
				d = self.offsets
				# distances of the 4 corner points from their original position:
				d1 = d[x][y]; d2 = d[x + 1][y]
				d3 = d[x][y + 1]; d4 = d[x + 1][y + 1]
				image_quad(self.img,
				# distorted quad:
				x * m + d1[0], y * m + d1[1],
				x * m + m + d2[0], y * m + d2[1],
				x * m + d3[0], y * m + m + d3[1],
				x * m + m + d4[0], y * m + m + d4[1],
				# source quad in image:
				x * m, y * m, x * m + m, y * m,
				x * m, y * m + m, x * m + m, y * m + m)
				
	def bulge(self, touch_x, touch_y):
		# push mesh vertices away from touch location:
		m = self.m
		r = self.img_size / 5
		for x in xrange(0, M + 1):
			for y in xrange(0, M + 1):
				offset = self.offsets[x][y]
				dist = sqrt((x*m-touch_x + offset[0])**2.0 +
				(y*m-touch_y + offset[1])**2.0)
				dx = x*m - touch_x
				dy = y*m - touch_y
				unit_x = dx / dist if dist > 0 else 0.0
				unit_y = dy / dist if dist > 0 else 0.0
				b = self.dt * 50
				if dist < r:
					falloff = max(sin(dist/r*pi), 0)
					offset_x = unit_x * b * falloff + offset[0]
					offset_y = unit_y * b * falloff + offset[1]
					self.offsets[x][y] = (offset_x, offset_y)
					
	def revert(self):
		for x in xrange(0, M + 1):
			for y in xrange(0, M + 1):
				offset = self.offsets[x][y]
				offset_x = floor(offset[0] - cmp(offset[0], 0))
				offset_y = floor(offset[1] - cmp(offset[1], 0))
				self.offsets[x][y] = (offset_x, offset_y)
				
	def draw(self):
		background(0, 0, 0)
		push_matrix()
		tx = self.size.w/2 - self.img_size/2
		ty = self.size.h/2 - self.img_size/2
		translate(tx, ty)
		text('Touch the image to deform it.', 'Helvetica-Bold',
		18, self.img_size/2, -30, alignment=5)
		text('Use two fingers to revert.', 'Helvetica-Bold',
		18, self.img_size/2, -60, alignment=5)
		self.draw_warped_image()
		pop_matrix()
		if len(self.touches) ==0:
			return
		if len(self.touches) > 1:
			self.revert()
		else:
			loc = self.touches.values()[0].location
			touch_x, touch_y = loc.x - tx, loc.y - ty
			self.bulge(touch_x, touch_y)
			
run(ImageWarp(), frame_interval=1)

