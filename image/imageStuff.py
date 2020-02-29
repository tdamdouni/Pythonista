# coding: utf-8

# imageStuff.py

from __future__ import print_function
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
	print((urllib3,' as urllib2'))
from PIL import Image, ImageOps, ImageDraw
import io
import Image

#url = "https://d1w2poirtb3as9.cloudfront.net/d28b29f37088409b5041.jpeg"


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

