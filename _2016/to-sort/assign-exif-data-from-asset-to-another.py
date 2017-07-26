# coding: utf-8

# https://forum.omz-software.com/topic/3580/photo-asset-location-setting-does-not-set-gps-exifs

import photos

def main():
	c = photos.get_assets(media_type='image')
	ps = photos.pick_asset(assets=c, title='Pick photos', multi=True)
	for p in ps:
		print(p.location)
		if p.location:
			# Photo has GPS tags
			prev_location = p.location
		else:
			# Photos does not have GPS tags, use previous if any
			if prev_location:
				p.location = prev_location
				
if __name__ == '__main__':
	main()

