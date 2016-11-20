# https://forum.omz-software.com/topic/3509/try-to-get-pictures-from-ipad-from-specific-album

import photos

# Go through all albums...
for album in photos.get_albums():
	# ...find the one with the correct name...
	if album.title == "App_Python kopie":
		# ...and put it in a variable, then stop the loop.
		my_album = album
		break
		
last_asset = my_album.assets[-1]
last_asset.get_image().show()

# For ui (buttons, etc.)
import ui

img = ui.Image("IMG_1234.JPG")
img.show()

# For PIL (image editing and processing)
import PIL.Image

img = PIL.Image.open("IMG_1234.JPG")
img.show()


import photos
for album in photos.get_albums():
	if album.title == "App_Python kopie":
		my_album = album
		break
last_asset = my_album.assets[-1]
last_asset.get_image().show()

