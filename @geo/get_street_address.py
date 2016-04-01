import location, webbrowser #, time

def getLocation():
    location.start_updates()
#   time.sleep(1)
    currLoc = location.get_location()
    location.stop_updates()  # stop GPS hardware ASAP to save battery
    return currLoc

def getStreetAddress(loc = getLocation()):
    return location.reverse_geocode(loc)[0]

street_address = '{Street}, {City}, {Country}'.format(**getStreetAddress())
print(street_address)
map_URL = 'http://maps.google.com?q=' + street_address.replace(' ', '+')
print(map_URL)  # also try safari-http://
webbrowser.open(map_URL)