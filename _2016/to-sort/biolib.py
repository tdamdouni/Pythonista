# coding: utf-8

# https://forum.omz-software.com/topic/2894/biolib

# coding: utf-8

import Image

def bencode(filename,plain_text): # returns true or false depending on if it successfully saves the photo.
	try:
		coded_image_width = len(plain_text)*5
		bioMessage = Image.new("RGB",(coded_image_width,1),(255,0,0))
		bioMessageLoaded = bioMessage.load()
		newPixelPosition = [0,0]
		for char in plain_text:
			asciiEdition = ord(char)
			bioMessageLoaded[newPixelPosition[0],0] = (asciiEdition,asciiEdition,asciiEdition)
			
			newPixelPosition[0] += 5
		bioMessage.save(filename)
		return True
	except:
		return False
		
def bedecode(coded_image): # returns a string of the decoded message.
	encodedPNG = Image.open(coded_image)
	encodedPNGLoaded = encodedPNG
	endtxt = ""
	newGrabPosition = [0,0]
	charsAmount = encodedPNG.size[0] / 5
	for reading in range(charsAmount):
		pixel = encodedPNG.getpixel((newGrabPosition[0],0))
		endtxt += chr(pixel[0])
		
		newGrabPosition[0] += 5
	return endtxt

