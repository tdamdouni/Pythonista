# Inspired by: https://github.com/kultprok/pythonista-drafts-recipes/blob/master/weatherdata/weatherdata.py
''' Print out current weather at your current location. '''
import location, requests, time
def getLocation():
    location.start_updates()
    time.sleep(1)
    currLoc = location.get_location()
    location.stop_updates() # stop GPS hardware ASAP to save battery
    return currLoc

your_loc = location.reverse_geocode(getLocation())[-1]
# import pprint ; pprint.pprint(your_loc) # useful for debugging
# See: http://bugs.openweathermap.org/projects/api/wiki
base_url = 'http://api.openweathermap.org/data/2.5/weather'
url_fmt = '?q={City},+{State},+{CountryCode}'  # &units=metric'
the_url = base_url + url_fmt.format(**your_loc).replace(' ', '+')
print(the_url)
weather = requests.get(the_url).json()
if weather:
    # import pprint ; pprint.pprint(weather) # useful for debugging
    for item in ('temp_min', 'temp_max'):
        if item not in weather['main']:
            weather['main'][item] = None # create values if they are not present
    if 'weather' not in weather: # weather is optional in weather!!
        weather['weather'] = [ {'description' : 'not available'} ]
    for item in ('sunrise', 'sunset'):
        weather['sys'][item] = time.ctime(weather['sys'][item]).split()[3] # just time, not date
    print('''Current weather at {name}, {sys[country]} is {weather[0][description]}.
        Temprature: {main[temp]}c ({main[temp_min]}c / {main[temp_max]}c) (min / max)
        Pressure: {main[pressure]} hPa
        Humidity: {main[humidity]}%
        Sunrise: {sys[sunrise]}
        Sunset: {sys[sunset]}
        Weather information provided by openweathermap.org'''.format(**weather))
