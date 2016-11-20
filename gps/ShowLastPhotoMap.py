# Shows the location of the last photo in the canera roll in the Maps app.
# (thanks to @HyShai for pointing out that the latitude/longitude refs are necessary)

import photos
import webbrowser

meta = photos.get_metadata(-1)
gps = meta.get('{GPS}')
if gps:
	latitude = str(gps.get('Latitude', 0.0)) + gps.get('LatitudeRef', '')
	longitude =str(gps.get('Longitude', 0.0)) + gps.get('LongitudeRef', '')
	maps_url = 'safari-http://maps.apple.com/?ll=%f,%f' % (latitude, longitude)
	webbrowser.open(maps_url)
else:
	print 'Last photo has no location metadata.'

