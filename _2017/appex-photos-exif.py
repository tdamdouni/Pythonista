# https://forum.omz-software.com/topic/4101/using-appex-to-modify-a-photo-creation-date-directly/9

import appex
import photos
from objc_util import ObjCInstance

def assets_for_attachments(attachments):
	all_assets = photos.get_assets()
	matching_assets = []
	for a in all_assets:
		objc_asset = ObjCInstance(a)
		path_orig = str(objc_asset.pathForOriginalFile())
		path_edit = str(objc_asset.pathForFullsizeRenderImageFile())
		if path_orig in attachments or path_edit in attachments:
			matching_assets.append(a)
	return matching_assets
	
attachments = appex.get_attachments()
assets = assets_for_attachments(attachments)
# Now you can use the photos module to manipulate the assets...

