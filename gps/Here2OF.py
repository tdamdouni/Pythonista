
'''
Copyright 2015 Paul Sidnell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
Find the current location and build an OmniFocus note containing the address and
links to that location in various mapping apps, TomTom, Apple Maps, Google Maps,
Waze and Open Streetmap.

Easy to launch from the WorkFlow or Launch apps
'''

import location
import webbrowser
import urllib
from string import Template

def locationToNote( address, lat, long):
	
	tpl = Template (
		"$street\n" +
		"$city\n" +
		"$zip\n" + 
		"$country\n" +
		"\n" + 
		"Apple: http://maps.apple.com/?z=12&q=$lat,$long\n" +
		"\n" + 
		"Google: https://google.com/maps/place/$lat,$long/@$lat,$long,12z\n" + 
		"\n" + 
		"Open Street Map: http://www.openstreetmap.org/?mlat=$lat&mlon=$long#map=12/$lat/$long/m\n" + 
		"\n" +
		"TomTom: tomtomhome://geo:action=show&lat=$lat&long=$long&name=Pin\n" + 
		"\n" +
		"Waze: waze://?ll=$lat,$long&navigate=yes");
	
	params = {
		"street" : address.get("Street"),
		"city" : address.get("City"), \
		"zip" : address.get("ZIP"), \
		"country" : address.get("Country"),
		"lat" : lat, 
		"long" : long};
	
	return tpl.substitute(params);

location.start_updates();
here = location.get_location();
location.stop_updates();

lat = here.get("latitude");
long = here.get("longitude");
address = location.reverse_geocode(here)[0];
note = locationToNote(address, lat, long);

ofnote = {"name" : address.get("Street"), "note" : note};
webbrowser.open("omnifocus:///add?" + urllib.urlencode(ofnote).replace('+','%20'));
