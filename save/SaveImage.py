from __future__ import print_function
import clipboard
import urllib
import Image
import photos
import cStringIO

# Given an image URL in the clipboard, save the image to the iOS Camera Roll with Pythonista. Simple script with no error checks or other settings.

URL = clipboard.get()

file = Image.open(cStringIO.StringIO(urllib.urlopen(URL).read()))

photos.save_image(file)

print('Image Saved')
