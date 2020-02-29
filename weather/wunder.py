#!/usr/bin/python

from __future__ import print_function
import json
import urllib
import time
from datetime import datetime, timedelta
import cgi

############################### Functions #################################

def wunder(lat, lon, wukey):
  "Return a dictionary of weather data for the given location."
  
  # Day names
  d0 = datetime.today().strftime('%A')
  d1 = (datetime.today() + timedelta(days=1)).strftime('%A')
  d2 = (datetime.today() + timedelta(days=2)).strftime('%A')
  d3 = (datetime.today() + timedelta(days=3)).strftime('%A')

  # URLs
  baseURL = 'http://api.wunderground.com/api/%s/' % wukey
  dataURL = baseURL + 'conditions/astronomy/hourly10day/q/%f,%f.json' % (lat, lon)
  radarURL = baseURL + 'radar/image.png' \
                     + '?centerlat=%f&centerlon=%f' % (lat, lon - 1) \
                     + '&radius=100&width=480&height=360&timelabel=1' \
                     + '&timelabel.x=10&timelabel.y=350' \
                     + '&newmaps=1&noclutter=1'

  # Collect data.
  ca = urllib.urlopen(dataURL).read()
  j = json.loads(ca)
  current = j['current_observation']
  astro = j['moon_phase']
  hourly = j['hourly_forecast'][:72]

  # Turn sun rise and set times into datetimes.
  rise = '%s:%s' % (astro['sunrise']['hour'], astro['sunrise']['minute'])
  set = '%s:%s' % (astro['sunset']['hour'], astro['sunset']['minute'])
  sunrise = datetime.strptime(rise, '%H:%M')
  sunset = datetime.strptime(set, '%H:%M')
  
  # Mapping of pressure trend symbols to words.
  pstr = {'+': 'rising', '-': 'falling', '0': 'steady'}
  
  # Forecast for the next 12 hours.
  today = {'name': '12 hours', 'forecast': []}
  for h in hourly[0:13:3]:
    f = [h['FCTTIME']['civil'],
         h['condition'],
         h['temp']['english'] + '&deg;']
    today['forecast'].append(f)
  
  # Forecasts for the next 2 days.
  tomorrow = {'name': d1, 'forecast': []}
  dayafter = {'name': d2, 'forecast': []}

  for h in hourly:
    if (h['FCTTIME']['weekday_name'] == d1) and \
       (h['FCTTIME']['hour'] in ['4', '8', '12', '16', '20']):
      f = [h['FCTTIME']['civil'],
           h['condition'],
           h['temp']['english'] + '&deg;']
      tomorrow['forecast'].append(f)

    if (h['FCTTIME']['weekday_name'] == d2) and \
       (h['FCTTIME']['hour'] == '0'):
      f = [h['FCTTIME']['civil'],
           h['condition'],
           h['temp']['english'] + '&deg;']
      tomorrow['forecast'].append(f)

    if (h['FCTTIME']['weekday_name'] == d2) and \
       (h['FCTTIME']['hour'] in ['4', '8', '12', '16', '20']):
      f = [h['FCTTIME']['civil'],
           h['condition'],
           h['temp']['english'] + '&deg;']
      dayafter['forecast'].append(f)

    if (h['FCTTIME']['weekday_name'] == d3) and \
       (h['FCTTIME']['hour'] == '0'):
      f = [h['FCTTIME']['civil'],
           h['condition'],
           h['temp']['english'] + '&deg;']
      dayafter['forecast'].append(f)
  
  # Construct the dictionary and return it.
  wudata = {'pressure': float(current['pressure_in']),
            'ptrend': pstr[current['pressure_trend']],
            'temp': current['temp_f'],
            'desc': current['weather'],
            'wind_dir': current['wind_dir'],
            'wind': current['wind_mph'],
            'gust': float(current['wind_gust_mph']),
            'feel': float(current['feelslike_f']),
            'sunrise': sunrise,
            'sunset': sunset,
            'radar': radarURL,
            'today': today,
            'tomorrow': tomorrow,
            'dayafter': dayafter}
  return wudata
            

def wuHTML(lat, lon, wukey):
  "Return HTML with WU data for given location."
  
  d = wunder(lat, lon, wukey)

  # Get data ready for presentation
  sunrise = d['sunrise'].strftime('%-I:%M %p').lower()
  sunset = d['sunset'].strftime('%-I:%M %p').lower()
  temp = '%.0f&deg;' % d['temp']
  pressure = 'Pressure: %.2f and %s' % (d['pressure'], d['ptrend'])
  wind = 'Wind: %s at %.0f mph, gusting to %.0f mph' %\
         (d['wind_dir'], d['wind'], d['gust'])
  feel = 'Feels like: %.0f&deg;' % d['feel']
  sun = 'Sunlight: %s to %s' % (sunrise, sunset)
  htmplt = '<tr><td class="left">%s</td><td class="center">%s</td>' +\
           '<td class="right">%s</td></tr>'
  hours = [ htmplt % tuple(f) for f in d['today']['forecast'] ]
  today = '\n'.join(hours)
  hours = [ htmplt % tuple(f) for f in d['tomorrow']['forecast'] ]
  tomorrow = '\n'.join(hours)
  hours = [ htmplt % tuple(f) for f in d['dayafter']['forecast'] ]
  dayafter = '\n'.join(hours)

  # Assemble the HTML.
  html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta name="viewport" content = "width = device-width" />
<title>Weather</title>
<style type="text/css">
  body { font-family: Helvetica; }
  p { margin-bottom: 0; }
  h1 { font-size: 175%%;
    text-align: center;
    margin-bottom: 0; }
  h2 { font-size: 125%%;
    margin-top: .5em ;
    margin-bottom: .25em; }
  table { width: 90%%; }
  td.left { text-align: right;
    padding-right: 1em;
    width: 30%%; }
  td.center { width: 50%%; }
  td.right { text-align: right;
    width: 10%%; }
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
  %s<br /></p>
  <h2>%s</h2>
  <table>
  %s
  </table>
  <h2>%s</h2>
  <table>
  %s
  </table>
  <h2>%s</h2>
  <table>
  %s
  </table>

</body>
</html>''' % (temp, d['desc'], d['radar'], wind, feel, pressure, sun, d['today']['name'], today, d['tomorrow']['name'], tomorrow, d['dayafter']['name'], dayafter)

  return html


############################## Main program ###############################

# My Weather Underground key.
wukey = 'fa08c6bb4f65448c'

# Get the latitude and longitude.
form = cgi.FieldStorage()
lat = float(form.getvalue('lat'))
lon = float(form.getvalue('lon'))

# Generate the HTML.
html = wuHTML(lat, lon, wukey)

print('''Content-Type: text/html

%s''' % html)