# Get the last photo, and convert it to grayscale, saving the edit in-place

import photos
album = photos.get_recently_added_album()
last = album.assets[-1]
if last.can_edit_content:
	img = last.get_image()
	grayscale_img = img.convert('L')
	grayscale_img.save('.edit.jpg', quality=90)
	last.edit_content('.edit.jpg')
else:
	print('The asset is not editable')

