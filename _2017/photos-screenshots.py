# https://forum.omz-software.com/topic/4453/new-photos-module-read-metadata

import photos
album = photos.get_screenshots_album()
screenshots = album.assets
x = screenshots[0]
attr_lst = [a for a in dir(x) if not a.startswith('_')]

for k in attr_lst:
    print(k, getattr(x , k))

print(help(x))
