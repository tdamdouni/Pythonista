# -*- coding: utf-8 -*-

import requests, json, webbrowser, urllib, sys

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Get your api key from https://code.google.com/apis/console/, you MUST add the Places API permission to it
GOOGLE_PLACES_URI = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}&sensor=false&key={1}'
APPLE_MAPS_URI = 'safari-http://maps.apple.com/?q={0}'
#call this script in pythonista for ios pythonista://GoogleToAppleMaps?action=run&argv=[prompt]

def main():
	if len(sys.argv) < 2:
		print('You must send the serch term as the first argument of this script')
	else:
		search_term = sys.argv[1]
		r = requests.get(GOOGLE_PLACES_URI.format(search_term, API_KEY))
		contents = json.loads(r.content)
		if r.status_code == requests.codes.ok:
			print('Place search success')
			# Search successful get first result
			first = contents['results'][0]
			#name = first['name']
			#latlong = first['geometry']
			address = first['formatted_address'].encode('utf-8')
			print(address)
			webbrowser.open(APPLE_MAPS_URI.format(urllib.quote(address)))
		else:
			print('Error obtaining place')
			
if __name__ == '__main__':
	main()

