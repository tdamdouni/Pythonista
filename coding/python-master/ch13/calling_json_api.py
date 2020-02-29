from __future__ import print_function
#The program will prompt for a location, contact a web service and retrieve JSON for the web service 
#and parse that data, and retrieve the first place_id from the JSON. 
#A place ID is a textual identifier that uniquely identifies a place as within Google Maps.

#To complete this assignment, you should use this API endpoint that has a static subset of the Google Data:
#http://python-data.dr-chuck.net/geojson

#Please run your program to find the place_id for Univeristy of Stellenbosch. Make sure to enter the name and case exactly

import urllib
import json

serviceurl = 'http://python-data.dr-chuck.net/geojson?'

#Prompt for a location
address = raw_input('Enter location: ')

#Friendly note: A web API is an interface with URLs as the controls. 
#In that respect, the entire web is a sort of API. 
#You try to access a URL in your browser (also known as a request), 
#and a web server somewhere makes a bunch of complicated decisions based on that 
#and sends you back some content (also known as a response). A standard web API works the same way.

#The key difference between an ordinary URL and a URL that is part of a web API 
#is that an ordinary URL sends back something pretty designed to look good in your browser, 
#whereas a web API URL sends back something ugly designed to be read by a computer.
#Web APIs are a way to strip away all the extraneous visual interface 
#that you dont care about and get at the data.

#Parameters are information you can supply as part of the URL in order to define what you want.

url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})

print('Retrieving', url)

uh = urllib.urlopen(url)

data = uh.read()

print('Retrieved',len(data),'characters')

js = json.loads(data)

place_id = js['results'][0]['place_id']

print(place_id)