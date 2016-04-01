# http://www.leancrew.com/all-this/2014/02/weather-underground-in-pythonista/
# http://www.wunderground.com/weather/api/
#!/usr/bin/python
import json
import requests
import time
from datetime import datetime
import location
import webbrowser
import BaseHTTPServer

########################## Functions ############################

def wunder(lat, lon, wukey):
  "Return a dictionary of weather data for the given location."
  
  # URLs
  baseURL = 'http://api.wunderground.com/api/%s/' % wukey
  conditionURL = baseURL + 'conditions/q/%f,%f.json' % (lat, lon)
  astroURL = baseURL + 'astronomy/q/%f,%f.json' % (lat, lon)
  radarURL = baseURL + 'radar/image.png' \
                     + '?centerlat=%f&centerlon=%f' % (lat, lon - 1) \
                     + '&radius=100&width=480&height=360&timelabel=1' \
                     + '&timelabel.x=10&timelabel.y=350' \
                     + '&newmaps=1&noclutter=1'

  # Collect data.
  c = requests.get(conditionURL)
  current = c.json()['current_observation']
  a = requests.get(astroURL)
  astro = a.json()['moon_phase']

  # Turn sun rise and set times into datetimes.
  rise = '%s:%s' % (astro['sunrise']['hour'], astro['sunrise']['minute'])
  set = '%s:%s' % (astro['sunset']['hour'], astro['sunset']['minute'])
  sunrise = datetime.strptime(rise, '%H:%M')
  sunset = datetime.strptime(set, '%H:%M')
  
  # Mapping of pressure trend symbols to words.
  pstr = {'+': 'rising', '-': 'falling', '0': 'steady'}

  # Construct the dictionary and return it.
  wudata = {'pressure': float(current['pressure_in']),
            'ptrend': pstr[current['pressure_trend']],
            'temp': current['temp_f'],
            'desc': current['weather'],
            'wind_dir': current['wind_dir'],
            'wind': current['wind_mph'],
            'feel': float(current['feelslike_f']),
            'sunrise': sunrise,
            'sunset': sunset,
            'moon_pct': float(astro['percentIlluminated']),
            'moon_age': int(astro['ageOfMoon']),
            'radar': radarURL}
  return wudata
            

def wuHTML(lat, lon, wukey):
  "Return HTML with WU data for given location."
  
  d = wunder(lat, lon, wukey)

  # Get data ready for presentation
  sunrise = d['sunrise'].strftime('%-I:%M %p').lower()
  sunset = d['sunset'].strftime('%-I:%M %p').lower()
  temp = '%.0f&deg;' % d['temp']
  pressure = 'Pressure: %.2f and %s' % (d['pressure'], d['ptrend'])
  wind = 'Wind: %s at %.0f mph' % (d['wind_dir'], d['wind'])
  feel = 'Feels like: %.0f&deg;' % d['feel']
  sun = 'Sunlight: %s to %s' % (sunrise, sunset)
  moon = 'Moon: %s%% at %s days' % (d['moon_pct'], d['moon_age'])

  # Assemble the HTML.
  html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
  <html>
  <head>
  <meta name="viewport" content = "width = device-width" />
  <title>Weather</title>
  <style type="text/css">
    body { font-family: Helvetica; }
    h1 { font-size: 175%%;
      text-align: center;
      margin-bottom: 0; }
    h2 { font-size: 125%%;
      margin-top: 0;
      margin-bottom: 0; }
    #now { margin-left: 0; }
    #gust { padding-left: 2.75em; }
    div p { margin-top: .25em;
      margin-left: .25em; }
  </style>
  </head>
  <body onload="setTimeout(function() { window.top.scrollTo(0, 1) }, 100);">
  <h1>%s &bull; %s </h1>

  <p><img width="100%%" src="%s" /></p>

  <p id="now">%s<br />
  %s<br />
  %s<br />
  %s<br />
  %s<br /></p>

  </body>
  </html>''' % (temp, d['desc'], d['radar'], wind, feel, pressure, sun, moon)

  return html


######################### Main program ##########################

# My Weather Underground key.
wukey = 'fa08c6bb4f65448c'

# Get the GPS info.
location.start_updates()
time.sleep(2)
loc = location.get_location()

# Generate the HTML.
html = wuHTML(loc['latitude'], loc['longitude'], wukey)

# Create the request handler.
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(s):
    """Respond to a GET request."""
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write(html)

# Start the server and show the page.
server = BaseHTTPServer.HTTPServer(('', 8888), MyHandler)
webbrowser.open('http://localhost:8888')
server.handle_request()

