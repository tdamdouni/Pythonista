from __future__ import print_function
#Gist ID: 9951701907ed328218dd

# https://gist.github.com/dave-britten/9951701907ed328218dd

import console
import photos
from PIL import Image
from PIL.ExifTags import TAGS

def adjust(dim, newdim):
	newdim = newdim.strip()
	try:
		if newdim[-1] == "%":
			newdim = int(dim * float(newdim[:-1]) / 100.0)
		else:
			newdim = int(newdim)
	except ValueError:
		newdim = dim
	return newdim
	
img = photos.pick_image(show_albums = True, include_metadata = False, original = True, raw_data = False)
if img is None:
	print("No image selected.")
else:
	#Get orientation from EXIF data.
	o = 1
	if img.format == "JPEG":
		tagid = [x[0] for x in TAGS.iteritems() if x[1] == "Orientation"][0]
		try:
			o = img._getexif()[tagid]
		except KeyError:
			pass
			
	#Apply rotate/flip as needed to get image upright.
	r, f = ((None, None), (None, Image.FLIP_LEFT_RIGHT), (Image.ROTATE_180, None), (Image.ROTATE_180, Image.FLIP_LEFT_RIGHT), (Image.ROTATE_90, Image.FLIP_LEFT_RIGHT), (Image.ROTATE_270, None), (Image.ROTATE_270, Image.FLIP_LEFT_RIGHT), (Image.ROTATE_90, None))[o - 1]
	
	if not (f is None):
		img = img.transpose(f)
	if not (r is None):
		img = img.transpose(r)
		
	width, height = img.size
	
	#Prompt for new width and height.
	width2 = adjust(width, console.input_alert("Width", "Enter new image width.", str(width)))
	
	height = int(height * (float(width2) / width))
	height2 = adjust(height, console.input_alert("Height", "Enter new image height.", str(height)))
	
	#Scale and save new image.
	img = img.resize((width2, height2), Image.ANTIALIAS)
	if photos.save_image(img):
		msg = "Saved."
	else:
		msg = "Save failed."
		
	console.alert(msg, button1 = "OK", hide_cancel_button = True)

