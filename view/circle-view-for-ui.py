# coding: utf-8

# https://forum.omz-software.com/topic/2902/circle-view-for-ui/4

import ui

class CircularView(ui.View):
	def __init__(self):
		pass
		
	def draw(self):
		oval = ui.Path.oval(0,0, self.width, self.height)
		rect = ui.Path.rect(0,0, self.width, self.height)
		#rect.append_path(oval)
		ui.Path.add_clip(oval)
		ui.set_color('white')
		oval.fill()
		
		
if __name__ == '__main__':
	cv = CircularView()
	cv.present('sheet')
	
#==============================

def draw(self):
	oval = ui.Path.oval(*self.bounds)
	rect = ui.Path.rect(*self.bounds)
	oval.append_path(rect)
	oval.eo_fill_rule = True
	oval.add_clip()
	ui.set_color('white')
	rect.fill()
	
#==============================


import ui
import webbrowser
#these are fillers for phhton 3 changes
try:
	import cStringIO
	print("old cString")
except ImportError:
	from io import StringIO as cStringIO
	print("new stringIO")
try:
	import urllib2
	print(urllib2)
except ImportError:
	import urllib3 as urllib2
	print(urllib3,' as urllib2')
from PIL import Image, ImageOps, ImageDraw
import io
import Image


def circleMaskViewFromURL(url):
	url=url
	#load image from url and show it
	file=cStringIO.StringIO(urllib2.urlopen(url).read())
	
	img = Image.open(file)
	
	#begin mask creation
	bigsize = (img.size[0] * 3, img.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(img.size, Image.ANTIALIAS)
	
	img.putalpha(mask)
	
	#show final masked image
	img.show()
	img=pil2ui(img)
	
	return img
	
# pil <=> ui
def pil2ui(imgIn):
	with io.BytesIO() as bIO:
		imgIn.save(bIO, 'PNG')
		imgOut = ui.Image.from_data(bIO.getvalue())
	del bIO
	return imgOut
	
	
	
	
	
	
if __name__=="__main__":

	#tests
	circleMaskViewFromURL("http://vignette2.wikia.nocookie.net/jamesbond/images/3/31/Vesper_Lynd_(Eva_Green)_-_Profile.jpg/revision/latest?cb=20130506215331")

