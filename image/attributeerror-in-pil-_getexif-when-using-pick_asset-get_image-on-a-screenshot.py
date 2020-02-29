# coding: utf-8

# https://forum.omz-software.com/topic/3584/attributeerror-in-pil-_getexif-when-using-pick_asset-get_image-on-a-screenshot

from __future__ import print_function
import console
import photos
from PIL import Image
b = console.alert('use','','pick_image','pick_asset',hide_cancel_button=True)
if b == 1 :
	img = photos.pick_image()
else:
	p = photos.pick_asset() # Get asset
	img = p.get_image()         # Get PIL from asset
exif_info = img._getexif()                          # Extract exifs from photo
print(exif_info)

