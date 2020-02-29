from __future__ import print_function
#prompt user for search string, call google geocoding api,
#and extract information from the returned json

import urllib
import json

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'

while True:
    address = raw_input('Enter location: ')
    if len(address) < 1 : break 
    
    #take users entry and construct a URL as a properly encoded parameter
    #and use urllib to retrieve the text from the google geocoding API. 
    url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
    
    print('Retrieved', url)
    uh = urllib.urlopen(url)
    data = uh.read()
    print('Retrieved', len(data), 'characters')
    
    try: js = json.loads(str(data))
    except: js = None 
    if 'status' not in js or js['status'] != 'OK':
        print('==== Failure to Retrieve ====')
        print(data)
        continue 
    print(json.dumps(js, indent=4))
    
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    print('lat', lat, 'lng', lng) 
    location = js['results'][0]['formatted_address']
    print(location)