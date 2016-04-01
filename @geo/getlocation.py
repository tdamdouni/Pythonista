import console
console.show_activity()
def getLocation():
    import location
    import datetime
    import time
    "Returns current location"
    location.start_updates()
    time.sleep(3)
    current = location.get_location()
    location.stop_updates()
    address = location.reverse_geocode({'latitude': current['latitude'], 'longitude': current['longitude']})
    loc = address[0]['Street'] + ', ' + address[0]['City'] + ', ' + address[0]['Country'] 
    return loc
    
if __name__ == '__main__':
    getLocation()