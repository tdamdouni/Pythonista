# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/653e36a0b00a3eb79e7f

from __future__ import print_function
from images2gif import writeGif
from PIL import Image, ImageDraw
import console

W, H = 1024,1024
RESOLUTION = 5
FG, BG = '#ffbb00', '#009bff'

#FG, BG = '#000000', '#ffffff'
class Rect:
	def __init__(self, left, top, width, height):
		self.left = left
		self.right = left + width
		self.top = top
		self.bottom = top+height
		
		self.centerx = left + (width/2)
		self.centery = top + (height/2)
		
		self.width = width
		self.height = height
		
		self.bbox = (left, top), (self.right, self.bottom)
	
def drawSierpinski(surf, rect, fgcolor=FG, bgcolor=BG, level=6, topshade=True):
	try:
		rect.left
	except AttributeError:
		left, top, width, height = rect
		rect = Rect(left, top, width, height)
	
	if level == 0:
		return
	
	quarterWidth = (rect.width/4)+rect.left
	threeQuarterWidth = (rect.width/4*3)+rect.left
	
	topRect = Rect(quarterWidth, rect.top, (rect.width / 2), (rect.height / 2))
	leftRect = Rect(rect.left, rect.centery, (rect.width/2), (rect.height/2))
	rightRect = Rect(rect.centerx, rect.centery, (rect.width / 2), (rect.height / 2))
	
	#Shade topleft
	if topshade:
		surf.rectangle((rect.left, rect.top, rect.centerx, rect.bottom), fill=bgcolor)
	#outer triangle
	surf.polygon([(rect.centerx,rect.top),(rect.left,rect.bottom),(rect.right,rect.bottom)],fgcolor)
	#inner upside-down triangle
	surf.polygon([(quarterWidth,rect.centery),(rect.centerx,rect.bottom),(threeQuarterWidth, rect.centery)],bgcolor)
	
	#do recursive calls
	drawSierpinski(surf, topRect, fgcolor, bgcolor, level-1, topshade)
	drawSierpinski(surf, leftRect, fgcolor, bgcolor, level-1, topshade)
	drawSierpinski(surf, rightRect, fgcolor, bgcolor, level-1, topshade)
	
	return im

def make_sierpinski(level, topshade=True):
	im = Image.new('RGB', (W, H), (255,255,255))
	surf = ImageDraw.Draw(im)
	
	drawSierpinski(surf, Rect(0, 0, W, H), FG, BG, level, topshade)
	return im

im = Image.new('RGB', (W, H), (255,255,255))
surf = ImageDraw.Draw(im)

#sierpinski = drawSierpinski(surf, (0, 0, W, H), level=7)
sierpinski1 = make_sierpinski(RESOLUTION)
sierpinski1.show()
sierpinski2 = make_sierpinski(RESOLUTION+1)
sierpinski2.show()

images = []
for x in range(0, W/2, W/64):
	a = sierpinski1.crop((x, x, W, W)).resize((512, 512), Image.ANTIALIAS)
	b = sierpinski2.crop((x, x, W, W)).resize((512, 512), Image.ANTIALIAS)
	
	alpha = x / float(W/2)
	images.append(Image.blend(a, b, alpha))
	console.clear()
	print(str(alpha*100)+'%')

console.clear()
print('writing...')

writeGif('sierpinski.gif', images, 2.0/len(images))