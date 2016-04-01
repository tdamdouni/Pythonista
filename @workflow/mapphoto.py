# https://gist.github.com/m42e/c800eb4be47eb1788d87

# coding: utf-8

import photos
import clipboard
import webbrowser


img = photos.pick_image(include_metadata=True)
meta=img[1]

gps = meta.get('{GPS}')

if gps:
  latitude = str(gps.get('Latitude', 0.0)) + gps.get('LatitudeRef', '')
  longitude =str(gps.get('Longitude', 0.0)) + gps.get('LongitudeRef', '')
  clipboard.set('%s, %s' % (latitude, longitude))
else:
  clipboard.set('Last photo has no location metadata.')

webbrowser.open('workflow://')