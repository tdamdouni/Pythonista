# coding: utf-8

# https://gist.github.com/omz/8220546

import console
import clipboard
import os

img = clipboard.get_image()
if img:
	img.save('temp.jpg')
	console.quicklook('temp.jpg')
	os.remove('temp.jpg')
else:
	print 'No image in clipboard.'