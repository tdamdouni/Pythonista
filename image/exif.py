# coding: utf-8

# http://www.leancrew.com/all-this/2014/02/photo-locations-with-apple-maps/

import Image
import photos, console

ph = photos.pick_image()
console.clear()
exif = ph._getexif()
print exif