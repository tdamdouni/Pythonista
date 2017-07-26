import photos

# Pick multiple images (with transparency) from the camera roll, crop them by their bounding box and save them back to the camera roll inside of a user defined Album.

#album=photos.create_album('Test')

cropped = []
converted = []

assets = photos.pick_asset(title='pick some assets', multi=True)
print(assets)

def crop_all(L):
	try:
		for asset in L:
		# get the original(True) image of the asset, crop it by the imagers bounding box and show it.
			asset.get_image(True).crop(asset.get_image(True).getbbox()).show()
			cropped.append(asset.get_image(True).crop(asset.get_image(True).getbbox()))
			converted.append(photos.create_image_asset(asset))
		#album.add _assets(L)
	except: None

crop_all(assets)

print(converted)
#print(cropped)
