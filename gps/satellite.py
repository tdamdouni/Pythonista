#!python2
# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/00b98ddb293412a30801

# 48.1843641777,11.5729847479

from __future__ import print_function
import urllib2
import json
import time
from io import BytesIO
from PIL import Image

URL="https://api.nasa.gov/planetary/earth/imagery?lon={}&lat={}&date={}&api_key={}"
API_KEY="ymjXp9qz2jJDR5tNEb0qa5YekynvAcVLJvKVcxYH"

def get_satellite_image(location=None,date=None):
	if location is None:
		location=(48.1843641777,11.5729847479) #Coordinates of New Paltz
	if date is None:
		date=time.strftime("%Y-%m-%d")

	lat,lon=location

	req_url=URL.format(str(lon),str(lat),date,API_KEY)
	req=json.loads(urllib2.urlopen(req_url).read())

	image_url=req["url"]
	print("Image at "+image_url)
	image = urllib2.urlopen(image_url)
	b=BytesIO(image.read())
	return b

def get_stitched_satellite_image(l=(48.1843641777,11.5729847479),date=None):
	d=0.025
	coords = [l,#Original
				(l[0]+d,l[1]),(l[0],l[1]+d),(l[0]-d,l[1]),(l[0],l[1]-d),#Horizontally adjacent
				(l[0]+d,l[1]+d),(l[0]+d,l[1]-d),(l[0]-d,l[1]-d),(l[0]-d,l[1]+d)]#Diagonally adjacent
	
	coords.sort()
	image_files=[get_satellite_image(c,date) for c in coords]
	images=[Image.open(i) for i in image_files]
	imsize=512
	
	canvas=Image.new('RGB',(imsize*3,imsize*3))
	index=0
	for y in range(2,-1,-1):
		for x in range(3):
			coords=(x*imsize,y*imsize)
			canvas.paste(images[index],coords)
			index+=1		
	return canvas
	
def save_satellite_image(location=None,date=None,filename='out.png'):
	Image.open(get_satellite_image(location,date)).save(filename)

def save_stitched_satellite_image(location=(48.1843641777,11.5729847479),date=None,filename='out.png'):
	get_stitched_satellite_image(location,date).save(filename)
		
if __name__ == "__main__":
	save_stitched_satellite_image((48.18,11.57))
