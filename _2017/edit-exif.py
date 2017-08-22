# https://forum.omz-software.com/topic/4101/using-apex-to-modify-a-photo-creation-date-directly/2

import photos, dialogs

asset = photos.pick_asset()
new_date = dialogs.datetime_dialog('Set Creation Date')
asset.creation_date = new_date
