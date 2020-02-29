from __future__ import print_function
# Get the oldest screenshot image, and delete it from the library

import photos
album = photos.get_screenshots_album()
screenshots = album.assets
if not screenshots:
	print('You have no screenshots in your library.')
else:
	oldest = screenshots[0]
	if oldest.can_delete:
		# This will automatically show a confirmation dialog:
		oldest.delete()
	else:
		print('Oldest screenshot is not deletable')

