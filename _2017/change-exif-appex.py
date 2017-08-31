# https://forum.omz-software.com/topic/4101/using-appex-to-modify-a-photo-creation-date-directly/11

# https://forum.omz-software.com/topic/4296/get-image-name-in-share-extension-native-apps-can

'''
Program to order photos in ios photo app.
author jmv38, may 28th 2017.
this program is intended to be called from photo app after selecting some photos
it will set all photos to same date+time (smallest or biggest) or it will add/subtract
some seconds to the photos.
It uses exif.ui interface, and you have to add exif.py to the callable scripts for auick access.
'''

import appex
import photos
import time
import datetime
from objc_util import ObjCInstance
import ui
import json

def assets_for_attachments(attachments):
	'''
	convert all photo attachments (from appex) to a list of photo assets
	it uses a precomputed dictionnary managed by load_assets_for_attachments()
	if the attachement is not found in dictionnary, the json file is update (once)
	this dramatically speeds up the process (json file is updated only when needed)
	'''
	assetsUpdated = False
	localIds = load_assets_for_attachments()
	matching_assets = []
	if type(attachments) != type([]):
		attachments = [attachments]
	for a in attachments:
		if (not a in localIds) and not assetsUpdated:
			save_assets_for_attachments()
			assetsUpdated = True
			localIds = load_assets_for_attachments()
		if a in localIds:
			id = localIds[a]
			matching_assets.append(photos.get_asset_with_local_id(id))
	return matching_assets
	
def save_assets_for_attachments():
	'''
	tricks from OMZ to link assets and attachements
	generates a dictionnary saved in a jason text file:
	dic[attachement]=asset.local_id
	'''
	all_assets = photos.get_assets()
	asset_path = {}
	for a in all_assets:
		objc_asset = ObjCInstance(a)
		path_orig = str(objc_asset.pathForOriginalFile())
		path_edit = str(objc_asset.pathForFullsizeRenderImageFile())
		id = a.local_id
		asset_path[path_orig] = id
		asset_path[path_edit] = id
	f = open("exif.txt", "w", encoding="utf-8")
	json.dump(asset_path, f)
	f.close()
	
def load_assets_for_attachments():
	'''
	loads a json text file of a dictionnary: dic[attachement]=asset.local_id
	'''
	try:
		f = open("exif.txt", "r", encoding="utf-8")
		localIds = json.load(f)
		f.close()
	except:
		# it assumes the only error is when the file doesnt exist yet
		save_assets_for_attachments()
		f = open("exif.txt", "r", encoding="utf-8")
		localIds = json.load(f)
		f.close()
	return localIds
	
def delta(s):
	''' shift the asset creation time by the specified seconds
	'''
	for asset in assets:
		asset.creation_date = asset.creation_date + datetime.timedelta(seconds = s)
		
def plus10(sender):
	delta(10)
	
def plus1(sender):
	delta(1)
	
def minus10(sender):
	delta(-10)
	
def minus1(sender):
	delta(-1)
	
def minDate(sender):
	'''Find oldest date/time and Apply it to all selected photos
	'''
	mini = assets[0].creation_date
	for asset in assets:
		current = asset.creation_date
		if current < mini:
			mini = current
	for asset in assets:
		asset.creation_date = mini
		
def maxDate(sender):
	'''Find most recent date/time and Apply it to all selected photos
	'''
	maxi = assets[0].creation_date
	for asset in assets:
		current = asset.creation_date
		if current > maxi:
			maxi = current
	for asset in assets:
		asset.creation_date = maxi
		
def testTool(sender):
	# just for interactive testing
	pass
	
def main():

	global testing
	testing = False
	
	if not appex.is_running_extension() and not testing:
		print('This script is intended to be run from the sharing extension.')
		return
		
	global attachments
	attachments = appex.get_attachments()
	
	global assets
	assets = assets_for_attachments(attachments)
	v = ui.load_view('exif')
	v.present('sheet')
	
if __name__ == '__main__':
	main()

