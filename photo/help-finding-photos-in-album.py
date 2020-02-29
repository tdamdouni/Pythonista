# coding: utf-8

# https://forum.omz-software.com/topic/3046/help-finding-photos-in-album/7

from __future__ import print_function
import ui
import photos
import console
from objc_util import *

PHAssetCollection = ObjCClass('PHAssetCollection')
PHAsset = ObjCClass('PHAsset')

def main():

	console.clear()
	# Build dictionary filename: index
	fn_index = {}
	for ip in range(photos.get_count()):
		m = photos.get_metadata(ip)
		#print m
		fn = m.get('filename')
		fn_index[fn] = (ip,'')
		
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

# --------------------

fn_index = {photos.get_metadata(i)['filename']: (i, '')
            for i in range(photos.get_count())}

# --------------------

NSBundle.bundleWithPath_('/System/Library/Frameworks/Photos.framework').load()

# --------------------

