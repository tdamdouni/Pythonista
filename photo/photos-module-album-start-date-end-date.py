# https://forum.omz-software.com/topic/3235/photos-module-album-start-date-end-date/4
from datetime import datetime
import photos

def get_album_dates(album:photos.AssetCollection) -> (datetime, datetime):
	assets = album.assets
	return (assets[0].creation_date, assets[-1].creation_date) if assets else (None, None)
		
# --------------------

