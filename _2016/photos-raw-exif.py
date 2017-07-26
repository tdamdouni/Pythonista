#!python2

import Image
import photos, console

ph = photos.pick_image()
console.clear()
exif = ph._getexif()
print exif
