# coding: utf-8

# https://github.com/cvpe/Pythonista-scripts

# IdentifyAlbumOfPhotos.py
# - scan all photos with photos module
# - store their file name in a dictionary "name->index"
# - scan all photos with Photos Objc Framework
# - get their album name and update dictionary as "name->index,album"
 
from __future__ import print_function
import ui
import photos
import console
from objc_util import *

NSBundle.bundleWithPath_('/System/Library/Frameworks/Photos.framework').load()
PHAssetCollection = ObjCClass('PHAssetCollection')
PHAsset = ObjCClass('PHAsset')

def main():

	console.clear()
	#p = photos.pick_image(show_albums=True, include_metadata=True, original=True, raw_data=False, multi=True)
	# Build dictionary filename: index
	fn_index = {photos.get_metadata(i).get('filename'): (i, '')
                    for i in xrange(photos.get_count())}

	# - type = 1: album
	# - subtype = 2: regular album
	result = PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(1,2, None)
	#print result
	for i in range(result.count()):
		coll = result.objectAtIndex_(i)
		album = str(coll.localizedTitle())
		assets = PHAsset.fetchAssetsInAssetCollection_options_(coll, None)
		for j in range(assets.count()):
			a = assets.objectAtIndex_(j)		
			fn = str(a.valueForKey_('filename'))
			tuple = fn_index[fn]
			ip = tuple[0]
			fn_index[fn] = (ip,album)
			
	# print filename -> album,index
	print(fn_index)

main()	
