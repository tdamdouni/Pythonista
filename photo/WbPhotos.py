# coding: utf-8

# https://gist.github.com/wbogers/44f6a49ac858a0cb0917c3dbb79e1c79

# https://forum.omz-software.com/topic/3144/list-of-photo-albums-with-properties

from functools import reduce
from objc_util import ObjCClass, ObjCInstance
from sys import maxint

# Load the Photos framework
ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/Photos.framework').load()

# Album types
__USER_ALBUM = 1
__SMART_ALBUM = 2

# Album subtypes / smart album subtypes
ALBUM_REGULAR = 2
ALBUM_CLOUD_SHARED = 101
ALBUM_ANY = maxint
ALBUM_SMART_GENERIC = 200
ALBUM_SMART_PANORAMAS = 201
ALBUM_SMART_VIDEOS = 202
ALBUM_SMART_FAVORITES = 203
ALBUM_SMART_TIMELAPSES = 204
ALBUM_SMART_ALL_HIDDEN = 205
ALBUM_SMART_RECENTLY_ADDED = 206
ALBUM_SMART_BURSTS = 207
ALBUM_SMART_SLOMO_VIDEOS = 208
ALBUM_SMART_USER_LIBRARY = 209
ALBUM_SMART_SELF_PORTRAITS = 210
ALBUM_SMART_SCREENSHOTS = 211
ALBUM_SMART_ANY = maxint

# Media types
MEDIA_TYPE_UNKNOWN = 0
MEDIA_TYPE_IMAGE = 1
MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_AUDIO = 3

def all_albums():
	# Return all albums (user + smart)
	user = user_albums()
	smart = smart_albums()
	albums = reduce(lambda x,y: dict(x, **y), (user, smart))
	return albums
	
def user_albums(subtype=ALBUM_ANY):
	# Return a dictionary with titles and identifiers of user albums
	return __get_albums(__USER_ALBUM, subtype)
	
def smart_albums(subtype=ALBUM_SMART_ANY):
	# Return a dictionary with titles and identifiers of smart albums
	return __get_albums(__SMART_ALBUM, subtype)
	
def album(identifier, title=""):
	# Fetch the album for the specified identifier and check if it's found
	PHAssetCollection = ObjCClass("PHAssetCollection")
	result = PHAssetCollection.fetchAssetCollectionsWithLocalIdentifiers_options_([identifier], None)
	album_details = dict()
	if result.count() != 0:
		if title == "":
			album_details["title"] = str(result.objectAtIndex_(0).localizedTitle())
		else:
			album_details["title"] = title
		album_details["type"] = __localized_type_description(result.objectAtIndex_(0).assetCollectionSubtype())
		album_details["number_of_photos"] = int(__get_asset_count(result.objectAtIndex_(0), MEDIA_TYPE_IMAGE))
		album_details["number_of_videos"] = int(__get_asset_count(result.objectAtIndex_(0), MEDIA_TYPE_VIDEO))
		start_date, end_date = __get_album_dates(result.objectAtIndex_(0))
		album_details["start_date"] = start_date
		album_details["end_date"] = end_date
		return album_details
	else:
		return None
		
def __get_albums(type, subtype):
	# Helper function: constructs dictionary with user / smart albums
	# Sort albums in ascending order, based on their localized title
	PHAssetCollection = ObjCClass("PHAssetCollection")
	NSSortDescriptor = ObjCClass("NSSortDescriptor")
	PHFetchOptions = ObjCClass("PHFetchOptions")
	fetchOptions = PHFetchOptions.alloc().init().autorelease()
	fetchOptions.sortDescriptors = [NSSortDescriptor.sortDescriptorWithKey_ascending_("localizedTitle", True)]
	# Fetch the albums with the specified type and return a list of their unique identifiers
	result = PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(type, subtype, fetchOptions)
	albums = dict()
	for index in range(result.count()):
		# Get each PHAssetCollection object and save (key,value) = (title,identifier)
		collection = result.objectAtIndex_(index)
		if type == __SMART_ALBUM:
			albums[__localized_smart_album_title(collection.assetCollectionSubtype())] = str(collection.localIdentifier())
		else:
			albums[str(collection.localizedTitle())] = str(collection.localIdentifier())
	# Return the dictionary with titles and identifiers
	return albums
	
def __get_asset_count(album, media_type):
	PHAsset = ObjCClass("PHAsset")
	NSPredicate = ObjCClass("NSPredicate")
	PHFetchOptions = ObjCClass("PHFetchOptions")
	fetchOptions = PHFetchOptions.alloc().init().autorelease()
	fetchOptions.predicate = NSPredicate.predicateWithFormat_("mediaType==" + str(media_type))
	assets = PHAsset.fetchAssetsInAssetCollection_options_(album, fetchOptions)
	return assets.count()
	
def __get_album_dates(album):
	PHAsset = ObjCClass("PHAsset")
	NSSortDescriptor = ObjCClass("NSSortDescriptor")
	PHFetchOptions = ObjCClass("PHFetchOptions")
	fetchOptions = PHFetchOptions.alloc().init().autorelease()
	fetchOptions.sortDescriptors = [NSSortDescriptor.sortDescriptorWithKey_ascending_("creationDate", True)]
	result = PHAsset.fetchAssetsInAssetCollection_options_(album, fetchOptions)
	if result.count()!=0:
		start_date = result.firstObject().creationDate()
		end_date = result.lastObject().creationDate()
		return (start_date, end_date)
	else:
		return (None, None)
		
def __localized_smart_album_title(subtype):
	if subtype == ALBUM_SMART_GENERIC:
		return "Generiek"
	elif subtype == ALBUM_SMART_PANORAMAS:
		return "Panorama's"
	elif subtype == ALBUM_SMART_VIDEOS:
		return "Video's"
	elif subtype == ALBUM_SMART_FAVORITES:
		return "Favorieten"
	elif subtype == ALBUM_SMART_TIMELAPSES:
		return "Tijdsverloop"
	elif subtype == ALBUM_SMART_ALL_HIDDEN:
		return "Verborgen"
	elif subtype == ALBUM_SMART_RECENTLY_ADDED:
		return "Recent toegevoegd"
	elif subtype == ALBUM_SMART_BURSTS:
		return "Bursts"
	elif subtype == ALBUM_SMART_SLOMO_VIDEOS:
		return "Vertraagd"
	elif subtype == ALBUM_SMART_USER_LIBRARY:
		return "Alle foto's"
	elif subtype == ALBUM_SMART_SELF_PORTRAITS:
		return "Selfies"
	elif subtype == ALBUM_SMART_SCREENSHOTS:
		return "Screenshots"
	else:
		return "Onbekend"
		
def __localized_type_description(type):
	if type == ALBUM_CLOUD_SHARED:
		return "Gedeeld album"
	elif type >= ALBUM_SMART_GENERIC:
		return "Slim album"
	else:
		return "Standaard album"

