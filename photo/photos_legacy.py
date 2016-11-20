# https://gist.github.com/lukaskollmer/e6b0a7ffab8a8e5d7ae48b8bef481cd0

import photos

def pick_an_image(show_albums=False, include_metadata=False, original=True, raw_data=False, multi=False):
	assets = photos.get_assets()
	return photos.pick_asset(assets, multi=multi).get_image()
	
photos.pick_image = pick_an_image

