# coding: utf-8

# https://forum.omz-software.com/topic/2918/picencode

from __future__ import print_function
from PIL import Image
import sys

def encode(filename,plain_text,X=16): # returns true or false depending on if it successfully saves the photo.
	g = 0
	b = X
	while not len(plain_text)/3 == len(plain_text)/3.0:
		plain_text = plain_text +'a'
		g = g+1
	r = 0
	x = 1
	y = 0
	if b > (len(plain_text)/3):
		b = (len(plain_text)/3) + 1
	test = [plain_text[i:i+3] for i in range(0, len(plain_text), 3)]
	for t in test:
		if x == b:
			x = 0
			y = y + 1
		x = 1 + x
	r = (b - (len(test)%b))//256
	x = 1
	z = y +1
	y = 0
	bioMessage = Image.new("RGB",(b,z),(255,255,255))
	bioMessageLoaded = bioMessage.load()
	for t in test:
		if x == b:
			x = 0
			y = y + 1
		asciiEdition1 = int(ord(t[0]))
		asciiEdition2 = int(ord(t[1]))
		asciiEdition3 = int(ord(t[2]))
		#print asciiEdition1,asciiEdition2,asciiEdition3
		bioMessageLoaded[x,y] = (asciiEdition1,asciiEdition2,asciiEdition3)
		
		x = 1 + x
	b = (b - (len(test)%b))%256
	bioMessage.putpixel((0,0),(r,g,b))
	bioMessage.save(filename)
	
def decode(filename):
	print("Decoding")
	image = Image.open(filename)
	r,g,b = image.getpixel((0,0))
	r = r*256 + b
	pixels = {}
	t =0
	for y in xrange(image.size[1]):
		for x in xrange(image.size[0]):
			pixels[t] = image.getpixel((x,y))
			t=t+1
	char_set = []
	for x in pixels.keys():
		if x > 0:
			t = pixels[x]
			char_set.append(t[0])
			char_set.append(t[1])
			char_set.append(t[2])
			
	test = char_set
	if not r == 0:
		real_data = char_set[:(-r*3)+3]
	else:
		real_data =char_set
	data = ''
	for x in real_data:
		data = data + chr(x)
	if not g ==0:
		data =data[:-g]
	return data

