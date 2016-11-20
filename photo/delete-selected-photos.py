# coding: utf-8

# https://forum.omz-software.com/topic/3037/script-to-delete-selected-photos

from objc_util import *
import threading
import photos
import console
import ui

NSBundle.bundleWithPath_('/System/Library/Frameworks/Photos.framework').load()
PHAssetCollection = ObjCClass('PHAssetCollection')
PHAsset = ObjCClass('PHAsset')
PHPhotoLibrary = ObjCClass('PHPhotoLibrary')
PHAssetChangeRequest = ObjCClass('PHAssetChangeRequest')

class MyView(ui.View):

	def will_close(self):
# Back to home screen
#webbrowser.open('launcher://crash')
		pass
def select_photos():
	console.clear()
	back = MyView(frame=(0,0,500,500))
	back.present('sheet')
	todels=photos.pick_image(include_metadata=True,original=True,raw_data=False,multi=True)
	
# todels = list of tuples
# [(image,metadata),(image,metadata),...]

# Build dictionary filename: index
fn_index = {}
for ip in range(photos.get_count()):
	m = photos.get_metadata(ip)
	fn = m.get('filename')
	fn_index[fn] = ip
	# that could be a problem if two photos have the same filename, what happens if you download the same file (fi from Dropbox) more than once.
	
# pick_image seems to display "camera roll" which seems to be all photos in sequence like
# - type = 2: smartalbum
# - subtype = 209: smartalbumlibrary
result = PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(2, 209, None)
coll = result.firstObject()
assets = PHAsset.fetchAssetsInAssetCollection_options_(coll, None)

# create array of assets to be deleted
a_del = []
for todel in todels:
	fn = todel[1].get('filename')
	ia = fn_index[fn] # file ame -> index
	a = assets.objectAtIndex_(ia)
	a_del.append(a)
	
lib = PHPhotoLibrary.sharedPhotoLibrary()
def change_block():
	# standad delete will ask a confirmation by specifying the number of photos to be deleted but by showing only one
	req = PHAssetChangeRequest.deleteAssets_(a_del)
	
def perform_changes():      lib.performChangesAndWait_error_(change_block, None)

t = threading.Thread(target=perform_changes)
t.start()
t.join()
if name == 'main':
	select_photos()

