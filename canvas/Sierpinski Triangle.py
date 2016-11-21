# coding: utf-8

# https://gist.github.com/ejetzer/7685495

from scene import *

def draw_triangle(a, b, c):
	for pt in (a, b, c):
		nxt = {a:b, b:c, c:a}[pt]
		line(pt[0], pt[1], nxt[0], nxt[1])
		
def more(a, b, c):
	# a, b, c are 2-tuples
	# Find the midpoints of a, b, c
	midxs = [(b[0] + a[0])/2,
	(c[0] + b[0])/2,
	(a[0] + c[0])/2]
	midys = [(b[1] + a[1])/2,
	(c[1] + b[1])/2,
	(a[1] + c[1])/2]
	midpts = tuple(zip(midxs, midys))
	triangles = [(a, midpts[0], midpts[2]),
	(b, midpts[0], midpts[1]),
	(c, midpts[1], midpts[2])]
	return triangles
	
def iteration(triangles):
	news = []
	for a, b, c in triangles:
		news += more(a, b, c)
	return news
	
class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		background(1, 1, 1)
		stroke(0, 0, 0)
		stroke_weight(1)
		self.triangles = [[(100, 100), (500, 700), (900, 100)]]
		self.count = 0
		
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		pass
		
	def touch_began(self, touch):
		background(1, 1, 1)
		for triangle in self.triangles:
			draw_triangle(*triangle)
		self.triangles = iteration(self.triangles)
		self.count += 1
		
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
run(MyScene())

