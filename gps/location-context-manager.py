# https://forum.omz-software.com/topic/3440/suggestion-location-context-manager

import location


class LocationManager (object):
	def __enter__(self):
		location.start_updates()
		
	def __exit__(self):
		location.stop_updates()
# --------------------
with LocationManager():
	# Do stuff that requires `location` here...
	...
	
# --------------------

import contexlib
import location

@contexlib.contexmanager
def location_enabled():
	location.start_updates()
	yield
	location.stop_updates()
# --------------------
with location_enable():
	# Do location stuff here...
	...
# --------------------

