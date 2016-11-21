# https://forum.omz-software.com/topic/3235/photos-module-album-start-date-end-date/4

def get_album_dates(album:photos.AssetCollection) -> (datetime.datetime, datetime.datetime):
	assets = album.assets
	if len(assets) == 0:
		return (None, None)
	else:
		return (assets[0].creation_date, assets[-1].creation_date)
		
# --------------------

