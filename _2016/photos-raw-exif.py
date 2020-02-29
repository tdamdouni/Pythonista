#!python2

from __future__ import print_function
import Image
import photos, console

ph = photos.pick_image()
console.clear()
exif = ph._getexif()
print(exif)
