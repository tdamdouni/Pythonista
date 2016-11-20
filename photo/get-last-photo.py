# Get the last photo, and show it in the console

import photos
all_assets = photos.get_assets()
last_asset = all_assets[-1]
img = last_asset.get_image()
img.show()

