# https://discourse.omnigroup.com/t/pythonista-3-script-to-save-current-location-to-omnifocus/25290

import location
import webbrowser
import time
import urllib.request, urllib.parse, urllib.error
from string import Template

def locationToNote( address, lat, lng):

	tpl = Template (
	"$name" +
	"$street" +
	"$city" +
	"$zip" +
	"$country" +
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
	
	name = sanitiseAddressField(address.get("Name"));
	street = sanitiseAddressField(address.get("Street"));
	
	if (name == street):
		street = "";
		
	params = {
	"name"    : name,
	"street"  : street,
	"city" :    sanitiseAddressField(address.get("City")),
	"zip" :     sanitiseAddressField(address.get("ZIP")),
	"country" : sanitiseAddressField(address.get("Country")),
	"lat" :     lat,
	"long" :    lng};
	
	return tpl.substitute(params);
	
def sanitiseAddressField(val):
	return (val + "\n") if val != None else "";
	
print("Getting Location...")
location.start_updates();
time.sleep(5);
here = location.get_location();
location.stop_updates();

lat = here.get("latitude");
lng = here.get("longitude");
address = location.reverse_geocode(here)[0];
timestr = time.strftime(" (%H:%M)");
note = locationToNote(address, lat, lng);
name = address.get("Name");
print("Street: " + name + timestr);
ofnote = {"name" : "Pin: " + name + timestr, "note" : note};
webbrowser.open("mapswithmepro://" + urllib.parse.urlencode(ofnote).replace('+','%20'));

