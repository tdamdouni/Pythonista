# -*- coding: utf-8 -*-
# https://gist.github.com/hiilppp/8268816
# To call script from Drafts, use the follwing URLs as URL Actions:
# - <pythonista://insert_location.py?action=run&argv=[[draft]]&argv=address>
#   (Will insert the address of your current location.)
# - <pythonista://insert_location.py?action=run&argv=[[draft]]&argv=link>
#   (Will insert a Google Maps link to your current location.)
 
import location
import re
import sys
import urllib
import webbrowser
 
a = re.sub(r"(.*\S)$", "\\1 ", sys.argv[1])
a = re.sub(r" \n$", "\n", a)
 
location.start_updates()
b = location.get_location()
location.stop_updates()
 
if sys.argv[2] == "address":
	b = location.reverse_geocode({"latitude": b["latitude"], "longitude": b["longitude"]})
	b = b[0]["Street"] + ", " + b[0]["ZIP"] + " " + b[0]["City"] + ", " + b[0]["Country"]
	# b = re.sub(r"(P|p)latz", "\\1l.", b)
	# b = re.sub(r"(S|s)trasse", "\\1tr.", b)
	# b = re.sub(r", Switzerland", "", b)
	b = b.encode("utf-8")
else:
	b = "<http://maps.google.com/?q=" + str(b["latitude"]) + "," + str(b["longitude"]) + ">"
 
c = a + b
 
webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(c))