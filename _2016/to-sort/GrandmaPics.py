# coding: utf-8

# https://gist.github.com/wcaleb/5542308

# Clear console
from __future__ import print_function
import console
console.clear()

print("Tap a photo to fetch a new one!")
print("Finding cute grandkid photos ...")

from scene import *
import urllib2
import random
from bs4 import BeautifulSoup
from PIL import Image

flickr_method = 'flickr.photosets.getPhotos'
flickr_apikey = 'XXXX'
flickr_setid = 'XXXX'
flickr_request = 'http://api.flickr.com/services/rest/?method=' + flickr_method + '&api_key=' + flickr_apikey + '&photoset_id=' + flickr_setid

photo_list = []

def remove_id_from_list(the_list, id):
	return [value for value in the_list if value != id]

def get_photo_list():
	'''Get list of photo ids from photoset'''
	global photo_list, xml_soup
	xml = urllib2.urlopen(flickr_request)
	xml_soup = BeautifulSoup(xml)
	for photo in xml_soup.find_all('photo'):
		photo_list.append(photo.get('id'))

def get_photo():
	'''Select random photo and construct url to photo'''
	global photo_list
	if len(photo_list) > 0:	
		photo_id = random.choice(photo_list)
		photo_list = remove_id_from_list(photo_list, photo_id)
		for xml_line in xml_soup.find_all(id=photo_id):
			photo_url = 'http://farm' + xml_line.get('farm') + '.staticflickr.com/' + xml_line.get('server') + '/' + xml_line.get('id') + '_' + xml_line.get('secret') + '.jpg'
		p = open('photo.jpg', 'wb')
		p.write(urllib2.urlopen(photo_url).read())
		p.close()
	else:
		get_photo_list()

class MyScene (Scene):
	def setup(self):
		'''This will get photo and load it before the first frame is drawn.'''
		get_photo()
		im = Image.open('.jpg').resize((320,480), Image.ANTIALIAS)
		self.im = load_pil_image(im.convert('RGBA'))
	
	def draw(self):
		'''This will be called for every frame (typically 60 times per second).'''
		background(0, 0, 0)
		image(self.im, 0, 0)
		fill(0, 0, 0)
		for touch in self.touches.values():
		   ellipse(touch.location.x - 25, touch.location.y - 25, 50, 50)
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		'''Use touch to trigger new photo'''
		self.setup()

run(MyScene())

print('\n\nTouch play to run again!')
