# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

'''
Name: WeatherAnywhere.py
Author: John Coomler

v1.0: 02/07/2015 to 02/15/2015-Created.

v1.1: 02/19/2015-Tightened up code and made
function calls to retrieve weather data for
printing from main(). Many thanks to @cclauss for
his continued expertise, input, & support in
sorting out and improving the code.

v1.2: 02/20/2015-More code cleanup, improved string
formatting techniques, & much improved error
handling.

v1.3: 02/21/2015-Added function to download weather
icons if any or all are missing. More code cleanup.

v1.4: 02/23/2015-Conversion functions renamed &
now return numbers instead of strings, added
ability to convert from imperial to metric units.

v1.5: 02/24/2015-Cleanup of date string formatting
& now show all precip types.

v1.6: 03/04/2015-Added ability to store weather
icons in a sub folder of script folder. Created 2
new functions, 'pick_your_weather' &
'get_weather_icons' to aid in porting script over
to a scene.

v1.7: 03/05/2015-Improved code in icon download
process to prevent IO errors.

v1.8: 03/07/2015-03/25/2015-Numerous changes &
code cleanup to accomodate scene development &
api changeover to www.wunderground.com.

v1.9: 04/04/2015-String formatting enhancements.

v2.0: 04/11/2015-Code readability & string
formatting improvements.

v2.1: 11/21/2015-Added code for record highs &
lows and length of day in weather 'now' section.

v2.2: 11/28/2015-Added code for precip daily
average and min-max range. Added code for average
high & low daily temp and record high & low daily
temp. Also added dew point and heat index readings.

v2.3: 12/03/2015-Fixed problem with moon stats.
When planner api module was combined with the
astronomy api module in the weather url query the
moon stats were incorrect for the current time
period. Moved planner module to the forecast url
query and that solved the issue. Added % clouds
to current forecast stats.

v2.4: 12/06/2015-Added function to get severe
weather alerts when necessary. Added code to get
name & stats for weather station that is reporting.

This script provides current & multi day weather
forecasts for any city you name, or coordinates you
are currently located in, using the api available
from www.wunderground.com.

The inspiration for this script came from https://
github.com/cclauss/weather_where_you_are/
weather_where_you_are.py.
'''
from __future__ import print_function
import console
import csv
import datetime
import time
import location
from PIL import Image
import requests
import sys
import webbrowser

# Global variables
icons = []
weather_icons = []
missing_icons = []
icon_path = './icons/'
api_key = 'Your API key goes here'

# Change to 'metric' if desired
imperial_or_metric = 'imperial'

# Conversion units
if imperial_or_metric == 'imperial':
  unit = ['f', 'in', 'in', 'in', 'in', 'mph',
        'fahrenheit', '', 'in', 'english',
        'mi', 'miles']
else:
  unit = ['c', 'mb', 'hPa', 'metric', 'mm', 'kph',
    'celsius', '_metric', 'cm', 'metric',
    'km', 'kilometers']

def pick_your_weather():
  city = st = zcode = ''
  lat = lon = 0

  # Pick a weather source
  try:
    ans = console.alert('Choose Your Weather Source:', '', 'From Your Current Location', 'From Entering a City Name', 'From A Pick List of Cities')
    if ans == 1:
      # Weather where you are
      print('Gathering weather data from where you are...')
      # Get lat & lon of where you are
      lat, lon = get_current_lat_lon()
    elif ans == 2:
      # Enter a state-country & city
      msg = 'Enter a city and state-country in format "'"New York, NY"'": '
      ans = console.input_alert(msg).title()
      if ans:
        print('='*20)
        print('Gathering weather data for {}'.format(ans))
        ans = ans.split(',')
        city = ans[0].replace(' ', '%20').strip()
        st = ans[1].strip()
    elif ans == 3:
      # Pick from list
      theCity, st, zcode = city_zips()
      print('='*20)
      if zcode:
        print('Gathering weather data for {}, {}'.format(theCity, st))
  except Exception as e:
    sys.exit('Error: {}'.format(e))

  # Call api from www.wunderground.com
  w, f = get_weather_dicts(lat, lon, city, st, zcode)
  return w, f

def get_current_lat_lon():
  # Retrieve lat & lon from current locale
  location.start_updates()
  # Delay sometimes improves accuracy
  #time.sleep(1)
  address_dict = location.get_location()
  location.stop_updates()
  return address_dict['latitude'], address_dict['longitude']

def city_zips(filename = 'cities.txt'):
  try:
    with open(filename) as f:
      # Read each line and store in list
      zips = [row for row in csv.reader(f)]
  except IOError as e:
    sys.exit('IOError in city_zips(): {}'.format(e))
  if not zips:
    sys.exit('No cities found in: {}'.format(filename))

  for i, zcode in enumerate(zips):
    # Align numbers neatly in printed list of cities & states/countries
    print('{:>7}. {}, {}'.format(i, zcode[0], zcode[1]))

  while True:
    try:
      ans = int(raw_input('\nEnter number of desired city: '))
      # Retrieve data from proper row,
      city, st, zcode = zips[ans]
      return city, st, zcode
    except (IndexError, ValueError):
      print('Please enter a valid number.')

def update_zips(new_line, filename = 'cities.txt'):
  try:
    # Append new city entry
    with open(filename, 'a') as f:
      f.write(new_line)

    # Sort list
    with open(filename, 'r') as f:
      lines = [line for line in f]

    lines.sort()

    # Rewrite newly sorted list
    with open(filename, 'w') as f:
      f.writelines(lines)

  except IOError as e:
    sys.exit('IOError in update_zips(): {}'.format(e))

def get_weather_dicts(lat, lon, city = '', st = '', zcode = ''):
  url_fmt = 'http://api.wunderground.com/api/{}/{}/q/{}.json'
  if city: # From entered city
    fmt = '{}/{}'
    query = fmt.format(st, city)
  elif zcode: # From list
    fmt = '{}'
    query = fmt.format(zcode)
  else: # From where you are now
    fmt = '{},{}'
    query = fmt.format(lat, lon)

  # Set today's month and day for Planner module
  month_day = time.strftime('%m%d')

  # Create urls
  w_url = url_fmt.format(api_key, 'geolookup/conditions/hourly/astronomy/almanac/', query)
  f_url = url_fmt.format(api_key, 'forecast10day/planner_{0}{0}/alerts/'.format(month_day), query)
  #print w_url
  #print f_url

  try:
    weather = requests.get(w_url).json()
    forecast = requests.get(f_url).json()
    #import pprint;pprint.pprint(weather)
    #import pprint;pprint.pprint(forecast)
    try:
      # Check if query returned nothing
      err = weather['response']['error']['description']
      if err:
        sys.exit('Error: {}'.format(err))
    except KeyError:
      pass
  # Servers down or no internet
  except requests.ConnectionError:
    print('=' * 20) # console.clear()
    sys.exit('Weather servers are busy. Try again in a few minutes...')

  try:
    # Check if query returned ambiguous results. If so, use zipcode link to redefine query.
    if weather['response']['results']:
      zcode = 'zmw:{}'.format(weather['response']['results'][0]['zmw'])
      w_url = url_fmt.format(api_key, 'conditions/hourly/astronomy/almanac/planner_{0}{0}/'.format(month_day), zcode)
      f_url = url_fmt.format(api_key, 'forecast10day', zcode)
      # Requery using zipcode link
      weather = requests.get(w_url).json()
      forecast = requests.get(f_url).json()
  except KeyError:
    pass

  # Query successful
  # If city was entered...
  if city:
    w = weather['current_observation']['display_location']

    city = w['full'].split(',')
    city, st = city
    zipcode = 'zmw:{zip}.{magic}.{wmo}'.format(**w)

    new_line = '{},{},{}\n'.format(city.strip(), st.strip(), zipcode.strip())

    # Check for existence of city in 'cities.txt'
    try:
      with open('cities.txt', 'r') as f:
        lines = [line for line in f]

      found = False
      for line in lines:
        if new_line in line:
          found = True
          break
      # Option to add entered city to city list
      if not found:
        msg = 'Ok to add {} to cities list?'.format(city)
        ans = console.alert('Update Cities File', msg, 'Yes', 'No', hide_cancel_button = True)
        if ans == 0:
          update_zips(new_line)

    except IOError as e:
      sys.exit('IOError in city_zips(): {}'.format(e))

  return weather, forecast

# Called from console version only
def get_console_icons(w, f, icon_path):
  '''
  Call function to get night hrs for this forecast,
  so we can show night icons when necessary.
  '''
  hour_now, sunrise_hr, sunset_hr = get_night_hrs(w)
  '''
  Find icon name for current weather and make sure
  it's a night icon if the current hour is between
  sunset and sunrise
  '''
  current = w['current_observation']
  ico = '{}.gif'.format(current['icon'])

  if hour_now >= sunset_hr or hour_now <= sunrise_hr:
    # Night icon
    current_ico = '{}nt_{}'.format(icon_path, ico)
  else:
    current_ico = '{}{}'.format(icon_path, ico)

  # Add icon to list
  console_icons = [current_ico]

  #day_count = len(f['forecast']['txt_forecast']['forecastday'])
  day_count = 14

  txt_f = f['forecast']['txt_forecast']['forecastday']
  for i in range(day_count):
    ico = '{}{}.gif'.format(icon_path, txt_f[i]['icon'])
    console_icons.append(ico)

  return console_icons

def get_icons_24h_data(w, f, icon_path):
  current = w['current_observation']
  temp_now = int(current['temp_' + unit[0]])
  temp_now = '{}° {}'.format(temp_now, unit[0].title())
  '''
  Call function to get night hrs for this forecast,
  so we can show night icons when necessary.
  '''
  hour_now, sunrise_hr, sunset_hr = get_night_hrs(w)
  '''
  Find icon name in current weather and make sure
  it's a night icon if the current hour is between
  sunset and sunrise.
  '''
  # The 'Now' icon(not included in query) for 24 hour forecast
  ico = '{}.gif'.format(current['icon'])

  if hour_now >= sunset_hr or hour_now <= sunrise_hr:
    # Night icon
    current_ico = '{}nt_{}'.format(icon_path, ico)
  else:
    current_ico = '{}{}'.format(icon_path, ico)

  # Create a 'Now' hour section
  the_hours = ['Now']
  the_temps = [temp_now]
  the_pops = ['---']
  the_icons = [current_ico]
  '''
  For other 23 hours...'hourly' portion of api
  query returns 36 hrs of data so we subtract 13 to
  get to first 23. With the 'Now' hr above we have
  24 hrs.
  '''
  hourly_f = w['hourly_forecast']
  for i in range(len(hourly_f) - 13):
    hour = hourly_f[i]['FCTTIME']['hour']
    hour = int(hour)

    ico = '{}.gif'.format(hourly_f[i]['icon'])
    # Nightime icons between sunset & sunrise
    if hour >= sunset_hr or hour <= sunrise_hr:
      the_icons.append('{}nt_{}'.format(icon_path, ico))
    else:
      the_icons.append('{}{}'.format(icon_path, ico))

    # Convert 24 hr time to 12 hr format
    if hour >= 13 and hour <= 23:
      hour = '{}PM'.format(hour - 12)
    elif hour == 12:
      hour = '{}PM'.format(hour)
    elif hour == 0:
      hour = '12AM'
    else:
      hour = '{}AM'.format(hour)

    the_hours.append(hour)
    the_temps.append('{}°{}'.format(hourly_f[i]['temp'][unit[9]], unit[0].title()))
    the_pops.append('{}%'.format(hourly_f[i]['pop']))
  '''
  Now we need an icon for the current weather
  portion of scene, which will be the same one as
  we used for the 'Now' hr of the 24 hr forecast.
  '''
  the_icons.append(current_ico)
  '''
  Next find icon names for the extended forecast.
  These icons, unlike the 24 hr ones, already have
  day-night distinctions in their names
  '''
  #day_count = len(f['forecast']['txt_forecast']['forecastday'])
  day_count = 14
  txt_f = f['forecast']['txt_forecast']['forecastday']
  for i in range(day_count):
    ico = '{}{}.gif'.format(icon_path, txt_f[i]['icon'])
    the_icons.append(ico)

  return the_icons, the_hours, the_temps, the_pops

def download_weather_icons(icon_path):
  # Downloads any missing weather icons
  # from www.wunderground.com
  import os
  gifs = []
  fmt = 'Downloading {} from {} ...'
  the_gifs = ['flurries', 'rain', 'sleet', 'snow', 'tstorms']
  for gif in the_gifs:
    gif = '{}.gif'.format(gif)
    gifs.append(gif)
    gifs.append('chance{}'.format(gif))
    gifs.append('nt_{}'.format(gif))
    gifs.append('nt_chance{}'.format(gif))

  the_gifs = ['sunny', 'cloudy']
  for gif in the_gifs:
    gif = '{}.gif'.format(gif)
    gifs.append(gif)
    gifs.append('nt_{}'.format(gif))
    gifs.append('mostly{}'.format(gif))
    gifs.append('nt_mostly{}'.format(gif))
    gifs.append('partly{}'.format(gif))
    gifs.append('nt_partly{}'.format(gif))

  the_gifs = ['clear', 'fog', 'hazy']
  for gif in the_gifs:
    gif = '{}.gif'.format(gif)
    gifs.append(gif)
    gifs.append('nt_{}'.format(gif))

  for filename in gifs:
    if os.path.exists(icon_path + filename):
      continue
    url = 'http://icons.wxug.com/i/c/i/{}'.format(filename)
    # Create icon folder if it doesn't exist
    if not os.path.exists(icon_path):
      os.makedirs(icon_path)
    # Write .gif file to icon folder
    with open(icon_path + filename, 'w') as out_file:
      try:
        print(fmt.format(filename, url))
        out_file.write(requests.get(url).content)
      except requests.ConnectionError as e:
        print('ConnectionError on {}: {}'.format(i, e))
    print('Done.')

def get_current_weather(w, f):
  current = w['current_observation']
  forecast_time = current['observation_time']

  simple_f = f['forecast']['simpleforecast']['forecastday'][0]

  # Get high temp & apply conversion units
  h_temp = '{}°{}'.format(simple_f['high'][unit[6]], unit[0].title())
  # Get low temp & apply conversion units
  l_temp = '{}°{}'.format(simple_f['low'][unit[6]], unit[0].title())

  # Get temperature records & apply conversions
  avg_high, avg_low, record_high, record_high_year, record_low, record_low_year = get_records(w)
  avg_high = '{}°{}'.format(avg_high, unit[0].title())
  record_high = '{}°{}'.format(record_high, unit[0].title())
  avg_low = '{}°{}'.format(avg_low, unit[0].title())
  record_low = '{}°{}'.format(record_low, unit[0].title())

  location = current['observation_location']

  # Reporting weather station stats
  w_station = location['city']
  lat = location['latitude']
  lon = location['longitude']
  elevation = location['elevation']

  # Relative humidity
  humidity =  current['relative_humidity']
  # Barometric pressure
  pressure = '{} {}'.format(current['pressure_' + unit[1]], unit[2])

  # Dew point
  dew_point = int(current['dewpoint_' + unit[0]])
  dew_point = '{}°{}'.format(dew_point, unit[0].title())

  # Wind
  wind = current['wind_string']
  if wind <> 'Calm':
    # Get direction & speed
    wind = '{} @ {} {}'.format(current['wind_dir'],current['wind_' + unit[5]], unit[5])
    # Add wind gusts if necessary
    gusts = current['wind_gust_' + unit[5]]
    if gusts <> 0:
      wind = '{} Gusts to {} {}'.format(wind, gusts, unit[5])

  # Get 'Feels Like' temp
  feels_like = current['feelslike_' + unit[0]]
  feels_like = int(float(feels_like))
  # Add degrees symbol & conversion unit
  feels_like = '{}°{}'.format(feels_like, unit[0].title())

  # Get precip amount
  precip = '{}'.format(current['precip_today_' + unit[3]])
  if not precip or precip == '-9999.00':
    precip = '0.00'
  precip = '{} {}'.format(precip, unit[4])

  # Get precip avg and range for day from planner api module
  precip_avg = '{} {}'.format(f['trip']['precip']['avg'][unit[4]], unit[4])
  precip_min = '{}'.format(f['trip']['precip']['min'][unit[4]])
  precip_max = '{} {}'.format(f['trip']['precip']['max'][unit[4]], unit[4])

  # Get visibility
  visibility = '{} {}'.format(current['visibility_' + unit[10]], unit[11])

  # Get percentage of cloudiness from first hour of hourly forecast
  clouds = w['hourly_forecast'][0]['sky']

  # Heat Index
  heat_index = current['heat_index_' + unit[0]]
  heat_index = '{}°{}'.format(heat_index, unit[0].title())
  # UV Index
  uv = current['UV']

  # Get times for sunrise & sunset & day length
  sunrise, sunset, length_of_day = get_sunrise_sunset(w)

  moon = w['moon_phase']
  age = moon['ageOfMoon']
  phase = moon['phaseofMoon']
  illum = moon['percentIlluminated']

  # Text to display in console or scene
  return('''Now...{0}:
\nToday's Forecast: High: {1}    Low: {2}
Today's Averages: High: {3}    Low: {4}
Today's Records: High: {5} [{6}]    Low: {7} [{8}]
Reporting Station: {9}
Lat: {10}     Lon: {11}     Elevation: {12}
Humidity: {13}     Dew Point: {14}
Barometric Pressure: {15}
Wind: {16}
Feels Like: {17}
Precipitation: {18}    Average: {19}    Range: {20} to {21}
Visibility: {22}     Cloud Cover: {23}%
Heat Index: {24}    UV Index: {25}
Sunrise: {26}      Sunset: {27}      Length Of Day: {28}
Moon Age: {29} days     Phase: {30}     Illuminated: {31}%
'''.format(forecast_time, h_temp, l_temp, avg_high, avg_low, record_high, record_high_year, record_low, record_low_year, w_station, lat, lon, elevation, humidity, dew_point, pressure, wind, feels_like, precip, precip_avg, precip_min, precip_max, visibility, clouds, heat_index, uv, sunrise, sunset, length_of_day, age, phase, illum, **w))

def get_extended_forecast(w, f):
  ef = []
  '''
  Query yields 10 days of weather, but 10 days
  won't display in scene. Last few days are
  missing, so we go with 7 days.
  '''
  #day_count = len(f['forecast']['txt_forecast']['forecastday'])

  #ef.append('Extended ' + str(day_count/2) + ' Day Forecast for ' + w['current_observation']['display_location']['full'] + ':')

  # Get 7 days of extended forecast * 2, for both day and night.
  day_count = 14

  simple_f = f['forecast']['simpleforecast']['forecastday']
  txt_f = f['forecast']['txt_forecast']['forecastday']

  for i in range(day_count):
    # Get forecast timestamp & reformat
    the_date = simple_f[i/2]['date']['epoch']

    the_date = datetime.datetime.fromtimestamp(int(the_date)).strftime('%m-%d-%Y') + ':'

    # Get header for forecast text...can be day or night
    title = txt_f[i]['title']

    # Day forecast header
    if title.find('Night') == -1:
      # Abbreviate day of wk with a slice
      title = title[:3]

      # Get high temp
      temp = 'High: {}° {}'.format(simple_f[i/2]['high'][unit[6]], unit[0].title())

      # Add date, 17 spaces, & high temp to day header
      title = '{} {}{}{}'.format(title, the_date, (' ' * 17), temp)
    else:
      # Abbreviate day of week & add 'Night' back to night header
      title = '{} Night'.format(title[:3])

      # Get low temp
      temp = 'Low: {}° {}'.format(simple_f[i/2]['low'][unit[6]], unit[0].title())
      '''
      Add date, 9 spaces, & low temp to night
      header. Now we have even spacial appearance
      between day & night.
      '''
      title = '{} {}{}{}'.format(title, the_date, (' ' *9), temp)

    # Get percent of precip
    pop = txt_f[i]['pop']

    # If pop, add 15 more spaces & display it on either header
    if pop <> '0':
      ef.append('\n{}{}Precip: {}%'.format(title, (' ' *15), pop))
    else:
      ef.append('\n{}'.format(title))

    # Text forecast
    fc_txt = txt_f[i]['fcttext' + unit[7]]

    # Find redundant text
    chances = ['rain', 'snow', 'precip']
    for chance in chances:
      txt_pos = fc_txt.find('Chance of {}'.format(chance))
      # Slice out unwanted text if found
      if txt_pos <> -1:
        fc_txt = fc_txt[0:txt_pos].strip()

    # Strip out high temp info from day & low temp info from night forecasts
    if title.find('Night') == -1:
      start = fc_txt.find('High')
    else:
      start = fc_txt.find('Low')

    end = fc_txt.find('Wind')

    # Slice out redundant temp info
    if start <> -1:
      fc_txt1 = fc_txt[:start]
      fc_txt2 = fc_txt[end:].replace('at', '@')
      fc_txt2 = fc_txt2.replace(' to ', '-')
      fc_txt = '{}{}'.format(fc_txt1, fc_txt2)

    ef.append(fc_txt)

    # Get accumulated day precip amts
    rain_day = simple_f[i/2]['qpf_day'][unit[4]]

    snow_day = simple_f[i/2]['snow_day'][unit[8]]

    # Show day accumulated precip amts
    if title.find('Night') == -1:
      if rain_day > 0.0:
        ef.append('Expected Rainfall: {} {}'.format(rain_day, unit[4]))

      if snow_day > 0.0:
        ef.append('Expected Snowfall: {} {}'.format(snow_day, unit[8]))

    # Get accumulated night precip amts
    rain_night = simple_f[i/2]['qpf_night'][unit[4]]

    snow_night = simple_f[i/2]['snow_night'][unit[8]]

    # Show night accumulated precip amts
    if title.find('Night') <> -1:
      if rain_night > 0.0:
        ef.append('Expected Rainfall: {} {}'.format(rain_night, unit[4]))

      if snow_night > 0.0:
        ef.append('Expected Snowfall: {} {}'.format(snow_night, unit[8]))

    # Get % relative humidity
    ef.append('Humidity: {}%'.format(simple_f[i/2]['avehumidity']))
  return ef

def get_forecast(w, f):
  # Text to display in console or scene
  ef = get_extended_forecast(w, f)
  return '\n'.join(ef)

# City name, temp, & conditions displayed in first lines of scene
def get_scene_header(w):
  current = w['current_observation']

  city_name = current['display_location']['full']

  temp_now = int(current['temp_' + unit[0]])
  temp_now = '{}° {}'.format(temp_now, unit[0].title())

  conditions = current['weather']
  return city_name, temp_now, conditions

def get_sunrise_sunset(w):
  fmt = '{hour}:{minute}'
  # Get times from astronomy api module
  sunrise = fmt.format(**w['sun_phase']['sunrise'])
  sunset = fmt.format(**w['sun_phase']['sunset'])

  # Add any date here...we eventually want time only
  fmt = '04/30/2014 {}'
  sunrise = fmt.format(sunrise)
  new_time = time.strptime(sunrise, '%m/%d/%Y %H:%M')
  timestamp = time.mktime(new_time)
  sunrise = timestamp
  t1 = datetime.datetime.fromtimestamp(int(sunrise)).strftime('%H:%M')
  sunrise = datetime.datetime.fromtimestamp(int(sunrise)).strftime('%I:%M %p')

  sunset = fmt.format(sunset)
  new_time = time.strptime(sunset, '%m/%d/%Y %H:%M')
  timestamp = time.mktime(new_time)
  sunset = timestamp
  t2 = datetime.datetime.fromtimestamp(int(sunset)).strftime('%H:%M')
  sunset = datetime.datetime.fromtimestamp(int(sunset)).strftime('%I:%M %p')

  t1 = t1.split(':')
  t2 = t2.split(':')

  # Compute time difference between sunrise & sunset...length of day
  t1_mins = int(t1[1]) + (int(t1[0]) * 60)
  t2_mins = int(t2[1]) + (int(t2[0]) * 60)

  hrs = (t2_mins - t1_mins) / 60
  mins = (t2_mins - t1_mins) - (hrs * 60)

  length_of_day = '{}h {}m'.format(hrs, mins)
  return sunrise, sunset, length_of_day

def get_records(w):
  a = w['almanac']
  avg_high = a['temp_high']['normal'][unit[0].upper()]
  record_high = a['temp_high']['record'][unit[0].upper()]
  record_high_year = a['temp_high']['recordyear']
  avg_low = a['temp_low']['normal'][unit[0].upper()]
  record_low = a['temp_low']['record'][unit[0].upper()]
  record_low_year = a['temp_low']['recordyear']
  return avg_high, avg_low, record_high, record_high_year, record_low, record_low_year

def get_night_hrs(w):
  hour_now = w['current_observation']['local_time_rfc822']
  # Slice and dice time string for hour only
  hour_now = hour_now[hour_now.find(':') - 2:hour_now.find(':')].strip()
  hour_now = int(hour_now)

  # Get times, split hrs & min, return hrs only
  sunrise, sunset, daylight_hrs = get_sunrise_sunset(w)
  sunrise = sunrise.split(':')
  sunrise_hr = int(sunrise[0].strip())
  sunset = sunset.split(':')
  sunset_hr = int(sunset[0].strip()) + 12
  return hour_now, sunrise_hr, sunset_hr

def get_web_weather(w):
  url = w['current_observation']['forecast_url']
  #webbrowser.open(url)
  return url

def get_alerts(w, f):
  # Get any severe weather alerts for current city
  num = len(f['alerts'])

  if num != 0:
    current = w['current_observation']
    the_city = current['display_location']['full']
    alert = '\n{0}\nSevere Weather Alert for {1}:\n{0}'.format('='*40, the_city)
    for i in range(num):
      msg = f['alerts'][i]['message']
      alert = '{}{}'.format(alert, msg)
  else:
    alert = ''
  return alert

# Used only for console display
def main():
  console.clear()
  w, f = pick_your_weather()

  # Get array of weather icons
  icons = get_console_icons(w, f, icon_path)

  print('='*20)

  # Print current conditions to console
  try:
    # Open, resize & show icon for current weather, which is 1st one in array
    img = Image.open(icons[0]).resize((25, 25), Image.ANTIALIAS)
    img.show()
  except:
    missing_icons.append(icons[0])

  print(get_current_weather(w, f))
  #print(get_forecast(w, f))
  #sys.exit()

  '''
  Printing the extended forecast to the console
  involves a bit more code because we are inserting
  a weather icon at each blank line.
  '''
  extended_f = get_forecast(w, f).split('\n')
  '''
  Start getting icons from element 1, as we already
  used element 0 for current weather.
  '''
  count = 1
  for line in extended_f:
    # Look for blank lines
    if not line and count <= 20:
      ico = icons[count]
      try:
        # Open, resize and show weather icon
        img = Image.open(ico).resize((25, 25), Image.ANTIALIAS)
        img.show()
      except:
        missing_icons.append(ico)
      count += 1
    print(line)

  print('\nWeather information provided by api.wunderground.com')

  if missing_icons:
    ans = console.alert('Weather Icon(s) Missing:','','Download Them Now')
    if ans == 1:
      download_weather_icons(icon_path)

  alerts = get_alerts(w, f)
  if len(alerts) != 0:
    print(alerts)

if __name__ == '__main__':
  main()

# - **WeatherAnywhere.py** - This script was inspired by @cclauss' script '[weather_where_you_are.py](https://github.com/cclauss/weather_where_you_are)' and uses the [weather api](http://www.wunderground.com/weather/api) from www.wunderground.com.  The script displays all it's information on the console screen, ideally suited for an iPhone in portrait orientation. In order to use the script you will need to aquire an api key from the wunderground website. The key is free if your usage is 500 or less server hits per day and provides a wealth of weather information. Lots of weather info is provided in text, including forecast, humidity, pressure, temperature, precipitation amounts, wind speed, wind chill, & percent of precipitation. The info is in imperial units, but can easily be changed to metric via a flag in the script. The script makes use of a txt file, 'cities.txt', to be located in the same folder as the script, and 38 gif files that display weather types, located in the '/icons' subfolder of the script's folder. The script will download the icons if it doesn't find them.  The txt file can contain popular local, regional, national and international cities of your choosing, including their state, if national, or country, if international, and their zip links.  The file is easily editable with the Pythonista editor. The zip link is automatically added to the cities list when you choose to add a new city. I've included a sample cities.txt file in this repository. 