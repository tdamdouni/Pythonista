# https://forum.omz-software.com/topic/2362/render_text-and-image_quad/2

# https://gist.github.com/anonymous/dfc5685a2b2a49762660

# coding: utf-8

from scene import *

class DigitNineScene(Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		pass
	
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		fill(1, 1, 1)
		pos = self.bounds.center().as_tuple()
		(img, siz) = render_text('9','Helvetica',40)
		rect(pos[0],pos[1],*siz)
		tint(0,0,0)
		image(img, pos[0], pos[1])
		tint(0.5,0,0)
		image_quad(img, pos[0], pos[1],
		            pos[0]+siz.w, pos[1],
		           pos[0], pos[1]+siz.h,
		           pos[0]+siz.w, pos[1]+siz.h,
		           
		           0,0,
		           siz.w,0,
		           0,siz.h,
		           siz.w, siz.h)
		           
run(DigitNineScene())