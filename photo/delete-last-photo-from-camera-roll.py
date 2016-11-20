# coding: utf-8

# https://forum.omz-software.com/topic/2915/delete-photos-from-camera-roll/3

from objc_util import *
import threading
import photos
NSBundle.bundleWithPath_('/System/Library/Frameworks/Photos.framework').load()
PHAssetCollection = ObjCClass('PHAssetCollection')
PHAsset = ObjCClass('PHAsset')
PHPhotoLibrary = ObjCClass('PHPhotoLibrary')
PHAssetChangeRequest = ObjCClass('PHAssetChangeRequest')

if not photos.is_authorized():
	# This shows the photo access permission dialog as a side-effect:
	photos.get_count()
	
def delete_last_photo():
	result = PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(2, 206, None)
	coll = result.firstObject()
	assets = PHAsset.fetchAssetsInAssetCollection_options_(coll, None)
	a = assets.lastObject()
	lib = PHPhotoLibrary.sharedPhotoLibrary()
	def change_block():
		req = PHAssetChangeRequest.deleteAssets_([a])
	def perform_changes():
		lib.performChangesAndWait_error_(change_block, None)
	t = threading.Thread(target=perform_changes)
	t.start()
	t.join()
	
if __name__ == '__main__':
	delete_last_photo()

