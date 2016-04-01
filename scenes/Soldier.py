# https://gist.github.com/GuyCarver/4180945
#example of animated frames for a character walk.
#downloads a soldier sprite sheet, cuts out frames for the walk cycles in 4 directions
# and animates the character walking in the direction controlled by gravity.

from scene import *
from PIL import Image
import urllib, os

start = Point(3, 1) #the sheet has 8 sets of characters in a 4x2 grid.
ssize = Size(96, 128)
speed = 0.15
frames = [0, 1, 2, 1] #4 frames per walk cycle
dirs = [0, 3, 9, 6]	#start frame for direction
moveamt = 32
mov = [(0, -moveamt), (-moveamt, 0), (0, moveamt), (moveamt, 0)]
keycolor = (0, 255, 0, 255)
gravsense = 0.06

north = 0
south = 2
east = 1
west = 3

def wrap(v, ext):
	if v < 0:
		return ext + v
	elif v >= ext:
		return v - ext
	return v

def gravitydirections(dir):
	ax = abs(dir.x)
	ay = abs(dir.y)
	dx = 0
	dy = 0
	#If x is larger than the sensitivity then set east or west.
	if ax > gravsense:
		dx = west if dir.x > 0 else east
	#If y is larger than the sensitivity then set north or south.
	if ay > gravsense:
		dy = south if dir.y > 0 else north

	#return direction tuple in order of largest gravity direction.
	return dy if ay > ax else dx

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		if not os.path.exists('Images'):
			os.mkdir('Images')
			
		if not os.path.exists("Images/soldier2.png"):		
			url = urllib.urlopen('http://img63.imageshack.us/img63/4348/americanset.png')
			with open("Images/soldier2.png", "wb") as output:
				output.write(url.read())

		img = Image.open("Images/soldier2.png").convert('RGBA')
		img.show()
		strt = Point(start.x * ssize.w, start.y * ssize.h)
		img = img.crop((strt.x, strt.y,strt.x + ssize.w - 1, strt.y + ssize.h - 1))
		
		d = img.load()
		keycolor = d[0,0] #1st pixel is used as keycolor.
		for x in range(img.size[0]):
			for y in range(img.size[1]):
				p = d[x, y]
				if p == keycolor: #if keycolor set alpha to 0.
					d[x, y] = (p[0], p[1], p[2], 0)

		img.show()
					
		def getframe(x, y):
		 	nim = img.crop((x * 32, y * 32, (x+1) * 32, (y+1) * 32))
#		 	nim = nim.resize((16,16), Image.ANTIALIAS)
			return load_pil_image(nim)

		self.images = [ getframe(x,y) for y in xrange(4) for x in xrange(3) ]
		self.start = 0
		self.base = 0
		self.dir = 0
		self.delay = speed
		self.x = 400
		self.y = 400

	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		self.dir = gravitydirections(gravity())
		background(0, 0, 1)
		d = self.dir
		mv = mov[d]
		self.x += mv[0] * self.dt
		self.y += mv[1] * self.dt
		self.x = wrap(self.x, self.size.w)
		self.y = wrap(self.y, self.size.h)
		image(self.images[dirs[d] + frames[self.start]], self.x, self.y, 32, 32)
		self.delay -= self.dt
		if self.delay <= 0:
			self.delay += speed
			self.start += 1
			if self.start >= len(frames):
				self.start = 0
    
run(MyScene(), PORTRAIT)