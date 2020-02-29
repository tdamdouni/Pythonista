# coding: utf-8

# https://forum.omz-software.com/topic/1935/how-can-i-convert-a-pil-image-to-a-ui-image/20

from __future__ import print_function
import ui
import io
from PIL import ImageOps, ImageDraw
from PIL import Image
import numpy as np
import StringIO

import console

# numpy <=> pil
def np2pil(arrayIn):
	imgOut = Image.fromarray(arrayIn)
	return imgOut
	
def pil2np(imgIn,arrayOut=None):
	if arrayOut == None:
		arrayOut = np.array(imgIn)
		return arrayOut
	else:
		arrayOut[:] = np.array(imgIn)
		return None
		
		
# pil <=> ui
def pil2ui(imgIn):
	with io.BytesIO() as bIO:
		imgIn.save(bIO, 'PNG')
		imgOut = ui.Image.from_data(bIO.getvalue())
	del bIO
	return imgOut
	
def ui2pil(imgIn):
	# create a fake png file in memory
	memoryFile = StringIO.StringIO( imgIn.to_png() )
	# this creates the pil image, but does not read the data
	imgOut = Image.open(memoryFile)
	# this force the data to be read
	imgOut.load()
	# this releases the memory from the png file
	memoryFile.close()
	return imgOut
	
# numpy <=> ui
def np2ui(arrayIn):
	# this is a lazy implementation, maybe could be more efficient?
	return pil2ui( np2pil(arrayIn) )
	
def ui2np(imgIn):
	# this is a lazy implementation, maybe could be more efficient?
	return pil2np( ui2pil(imgIn) )
	
	
if __name__ == "__main__":
	# testing the functions above
	
	img = Image.open('Test_Lenna')
	s = 256
	img = img.resize((s, s), Image.BILINEAR)
	img = ImageOps.grayscale(img)
	
	console.clear()
	
	print( 'test: open a pil image:')
	img.show()
	
	print('- ')
	print( 'test: pil image => return a new np array')
	print(' ')
	arr = pil2np(img)
	print(arr)
	
	print('- ')
	print( 'test: pil image => write into existing np array')
	print(' ')
	pil2np(img.rotate(90), arr)
	print(arr)
	
	print('- ')
	print( 'test:  np array => return a new pil image')
	img1 = np2pil(arr)
	img1.show()
	
	# test: pil2ui verification is done via a popover
	iv = ui.ImageView(frame=(0,0,256,256))
	iv.name = 'pil2ui'
	iv.image = pil2ui(img)
	iv.present('popover', popover_location=(600,100))
	
	print('- ')
	print( 'test:  ui image => return a new pil image (rotated by -90Â° to prove pil type)')
	img2 = ui2pil(iv.image).rotate(-90)
	print( type(img2))
	img2.show()
	
	# test: np2ui verification is done via a popover
	iv2 = ui.ImageView(frame=(0,0,256,256))
	iv2.name = 'np2ui'
	iv2.image = np2ui(arr)
	iv2.present('popover', popover_location=(300,100))
	
	print('- ')
	print( 'test:  ui image => return a new np array')
	arr2 = ui2np(iv2.image)
	print( arr2)

