# https://pythonista-app.slack.com/archives/codinghelp/p1483400029000975

import photos
from PIL import Image
from PIL.ExifTags import TAGS
import clipboard

def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	info = i._getexif()
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value
	return ret

images = photos.get_favorites_album().assets

data = get_exif(images[0])

print(data)

