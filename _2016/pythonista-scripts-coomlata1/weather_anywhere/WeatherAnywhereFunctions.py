# coding: utf-8
'''
Name: WeatherAnywhere.py
Author: @coomlata1

This script serves only as a placeholder for the functions that are needed to run the 'WeatherAnywhereScene' script. 
'''
from __future__ import print_function
import console
import dialogs
import csv
import datetime
import time
import location
from PIL import Image
import requests
import sys
import webbrowser
import ui
import os
import plistlib

icons = []
weather_icons = []
missing_icons = []
icon_path = './icons/'
# Insert api key here
api_key = ''

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

# Thanks to @cclauss for this code snippet
def pythonista_version():  # 2.0.1 (201000)
  plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
  return '{CFBundleShortVersionString} ({CFBundleVersion})'.format(**plist)

# Determine which device by screen size
def is_iP6p():
  iP6p = True
  min_screen_size = min(ui.get_screen_size())

  #print min_screen_size
  #iphone6 min = 414
  #iphone6 max = 736
  #iphone5 min = 320
  #iphone5 max = 568

  if min_screen_size < 414:
    iP6p = False
  return iP6p
  
# Loads pyui file with menu and objects to control user weather choices
def pick_your_weather():
  city_typed_in = st = zcode = ''
  lat = lon = 0
  lst = []

  global btn_weather, btn_type, city_picked, city_st, err, item

  btn_weather = btn_type = city_picked = False
  city_st = err = item = ''

  def get_city_list(filename = 'cities.txt'):
    try:
      with open(filename) as f:
        # Read each line and store in list
        cities = [row for row in csv.reader(f)]
      return cities
    except IOError as e:
      err = 'IOError in city_list(): {}'.format(e)
      console.hud_alert('{}'.format(e), 'error')
      sys.exit(err)
    if not cities:
      err = 'No cities found in {}'.format(filename)
      console.hud_alert(err, 'error')
      sys.exit(err)

  def get_current_lat_lon():
    # Retrieve lat & lon from current locale
    location.start_updates()
    # Delay sometimes improves accuracy
    #time.sleep(1)
    address_dict = location.get_location()
    location.stop_updates()
    return address_dict['latitude'], address_dict['longitude']

  # 'From Where You Are' button tapped
  def btn_weather_tapped(sender):
    global btn_weather
    btn_weather = True
    v.close()

  # City in list was tapped
  def item_selected(sender):
    global city_picked
    city_picked = True
    v.close()

  # Delete slider in TableView cell for a city in list was tapped
  def item_delete(sender):
    global item
    
    # Thanks to @Phuket2 for help and direction on capturing a delete event in a tableview
    removed = [x for x in items if x not in sender.items]
    if len(removed) == 1:
      item = removed[0]
      #print  'Item {} removed'.format(item)
      items.remove(item)
      console.hud_alert('Removing {} from list of cities.'.format(item))
      item = '{},{}'.format(item[:item.find(',').strip()], item[item.find(',') + 1:].strip())
      update_city_list('remove', item)
      console.hud_alert('Done')
    else:
      print('Something wtong, more than 1 removed item')

  # 'From A City You Can Add To List' button was tapped
  def btn_type_tapped(sender):
    global btn_type, city_st, err
    
    try:
      city_st = dialogs.input_alert('Enter A City, ST:')
      if city_st:
        if not ',' in city_st:
          err = 'Formatting error'
          city_st = ''
          pass   
        elif len(city_st.strip()) < 4:
          err = 'Unlikely city name.'
          city_st = ''
          pass
        else:
          btn_type = True
          v.close()
          pass
      else:
        err = 'Nothing Entered'
      if err:
        console.hud_alert(err, 'error')
        err = ''
        pass
    except KeyboardInterrupt:
      pass
      
  # Create a list for TableView data source
  cities = get_city_list()
  for city in cities:
    # Append city name and state or country to list
    lst.append('{}, {}'.format(city[0], city[1]))

  # Quick and dirty list dialog with limited options
  #x = dialogs.list_dialog(title = 'Pick Your Desired City:', items = lst)

  items = lst
  data_source = ui.ListDataSource(items)
  data_source.delete_enabled = True
  data_source.edit_action = item_delete
  data_source.action = item_selected

  # Load pypi file and reference objects in form
  v = ui.load_view('WeatherAnywhere')
  v.background_color = 'orange'
  tv = v['tv']
  tv.data_source = data_source
  tv.delegate = data_source

  #button_go = v['btn_go']
  #button_go.delegate = ui.Button(button_go)

  #city_st = v['txt_city']
  #city_st.delegate = ui.TextView(city_st).text

  v.present()
  v.wait_modal()

  # Returns a tuple of selected cell's section & row in tableview
  row = tv.selected_row

  # 'From Where You Are' button tapped
  if btn_weather:
    console.hud_alert('Gathering weather data from where you are...', 'success', 1)
    # Get lat & lon of where you are
    lat, lon = get_current_lat_lon()

  # A city and state was typed in
  if len(city_st) != 0:
    city_st = city_st.split(',')
    city_typed_in = city_st[0].replace(' ', '%20').strip()
    st = city_st[1].strip()
    console.hud_alert('Gathering weather data for {}, {}'.format(city_st[0].title(), st.upper()), 'success', 1)
    
  # Picked a city from list
  if city_picked:
    the_city, st, zcode = cities[row[1]]
    if zcode:
      console.hud_alert('Gathering weather data for {}, {}'.format(the_city, st), 'success', .50)

  if len(err) == 0:
    # If 'X' on form tapped
    if not btn_weather and not btn_type and not city_picked:
      err = 'Script Cancelled.'
      exit(err)
     
  return lat, lon, city_typed_in, st, zcode

def update_city_list(operation, city_line, filename = 'cities.txt'):
  # Adding a city to list
  if operation == 'add':
    try:
      # Append new city entry to file
      with open(filename, 'a') as f:
        # Create new line and append data, otherwise new city info is added to end of last line in file.
        f.write('\n')
        f.write(city_line)

      # Sort list
      with open(filename, 'r') as f:
        lines = [line for line in f]

      lines.sort()
  
      # Rewrite newly sorted list with no blank lines
      with open(filename, 'w') as f:
        for line in lines:
          if not line.isspace():
            f.write(line)
        #f.writelines(lines)

    except IOError as e:
      err = 'IOError in update_city_list(): {}'.format(e)
      # Present error msg and kill thread
      console.hud_alert(err, 'error')
      sys.exit(err)
  
  # Remove a city from list
  else:
    try:
      with open(filename) as f, open('newfile.txt', 'w') as g:
        for line in f:
          # Write all lines but one not wanted to a new file
          if city_line not in line:
            g.write(line)
      # Delete old file
      os.remove(filename)
      # Rename new file to same name as old file
      os.rename('newfile.txt', filename)
    except IOError as e:
      err = 'IOError in update_city_list(): {}'.format(e)
      # Present error msg and kill thread
      console.hud_alert(err, 'error')
      sys.exit(err)

def get_weather_dicts(lat, lon, city = '', st = '', zcode = ''):
  url_fmt = 'http://api.wunderground.com/api/{}/{}/q/{}.json'
  if city: # From an entered city
    fmt = '{}/{}'
    query = fmt.format(st, city)
  elif zcode: # From list
    fmt = '{}'
    query = fmt.format(zcode)
  else: # From where you are now button
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
      # Check if query returned ambiguous results.
      err = weather['response']['results']
      if err:
        console.hud_alert("Ambiguous Results...Tap 'Menu' To Continue", 'error')
        sys.exit('Error in get_weather_dicts: Ambiguous Results: {}'.format(err))
    except KeyError:
      pass

      try:
        # Check if query returned nothing
        err = weather['response']['error']['description']
        if err:
          console.hud_alert("No Query Results...Tap 'Menu' To Continue", 'error')
          sys.exit('Error in get_weather_dicts: {}'.format(err))
      except KeyError:
        pass
  # Servers down or no internet so kill thread
  except requests.ConnectionError:
    print('=' * 20) # console.clear()
    err = "Weather Servers Busy...Tap 'Menu' To Continue"
    console.hud_alert('{}'.format(err), 'error')
    sys.exit('Error in get_weather_dicts: {}'.format(err))

  # Query successful
  # If city was typed in...
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
        if ans == 1:
          update_city_list('add', new_line)
          
    # Kill thread
    except IOError as e:
      err = 'IOError in get_weather_dicts(): {}'.format(e)
      console.hud_alert("{}...Tap 'Menu' To Continue".format(e), 'error')
      sys.exit(err)

  return weather, forecast

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
  if heat_index != 'NA':
    heat_index = '{}°{}'.format(heat_index, unit[0].title())
  # UV Index
  uv = current['UV']

  # Get times for sunrise & sunset & day length
  sunrise, sunset, length_of_day = get_sunrise_sunset(w)

  moon = w['moon_phase']
  age = moon['ageOfMoon']
  phase = moon['phaseofMoon']
  illum = moon['percentIlluminated']
  '''
  If this is Pythonista 2, and an iPhone 6+ or better there is more screen to work with, as Pythonista recognizes the native screen eesolutions of the iOS device being used.
  '''
  if pythonista_version()[:1] == '2' and is_iP6p():
    spaces = 12
  else:
    spaces = 6

  # Text to display in console or scene
  return('''Now...{0}:
  \nToday's Forecast: High: {1}{32}Low: {2}
Today's Averages: High: {3}{32}Low: {4}
Today's Records: High: {5} [{6}]{32}Low: {7} [{8}]
Reporting Station: {9}
Lat: {10}{32}Lon: {11}{32}Elevation: {12}
Humidity: {13}{32}Dew Point: {14}
Barometric Pressure: {15}
Wind: {16}
Feels Like: {17}
Precipitation: {18}{32}Average: {19}{32}Range: {20} to {21}
Visibility: {22}{32}Cloud Cover: {23}%
Heat Index: {24}{32}UV Index: {25}
Sunrise: {26}{32}Sunset: {27}{32}Length Of Day: {28}
Moon Age: {29} days{32}Phase: {30}{32}Illuminated: {31}%
'''.format(forecast_time, h_temp, l_temp, avg_high, avg_low, record_high, record_high_year, record_low, record_low_year, w_station, lat, lon, elevation, humidity, dew_point, pressure, wind, feels_like, precip, precip_avg, precip_min, precip_max, visibility, clouds, heat_index, uv, sunrise, sunset, length_of_day, age, phase, illum, (' ' * int(spaces)), **w))

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

  '''
  If this is Pythonista 2, and an iPhone 6+ or better there is more screen to work with, as Pythonista recognizes the native screen eesolutions of the iOS device being used.
  '''
  if pythonista_version()[:1] == '2' and is_iP6p():
    day_header_spaces = 32
    night_header_spaces = 24
    pop_spaces = 30
  else:
    day_header_spaces = 17
    night_header_spaces = 9
    pop_spaces = 15

  for i in range(day_count):
    # Get forecast timestamp & reformat
    the_date = simple_f[i/2]['date']['epoch']

    the_date = datetime.datetime.fromtimestamp(int(the_date)).strftime('%m-%d-%Y') + ':'

    # Get header for forecast text...can be day or night
    title = txt_f[i]['title']

    # Day forecast header
    if not 'Night' in title:
      # Abbreviate day of wk with a slice
      title = title[:3]

      # Get high temp
      temp = 'High: {}° {}'.format(simple_f[i/2]['high'][unit[6]], unit[0].title())

      # Add date, spaces, & high temp to day header
      title = '{} {}{}{}'.format(title, the_date, (' ' * int(day_header_spaces)), temp)

    else:
      # Abbreviate day of week & add 'Night' back to night header
      title = '{} Night'.format(title[:3])

      # Get low temp
      temp = 'Low: {}° {}'.format(simple_f[i/2]['low'][unit[6]], unit[0].title())
      '''
      Add date, spaces, & low temp to night
      header. Now we have even spacial appearance
      between day & night.
      '''
      title = '{} {}{}{}'.format(title, the_date, (' ' *int(night_header_spaces)), temp)

    # Get percent of precip
    pop = txt_f[i]['pop']

    # If pop, add more spaces & display it on either header
    if pop <> '0':
      ef.append('\n{}{}Precip: {}%'.format(title, (' ' *int(pop_spaces)), pop))
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
    if not 'Night' in title:
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
    if not 'Night' in title:
      if rain_day > 0.0:
        ef.append('Expected Rainfall: {} {}'.format(rain_day, unit[4]))

      if snow_day > 0.0:
        ef.append('Expected Snowfall: {} {}'.format(snow_day, unit[8]))

    # Get accumulated night precip amts
    rain_night = simple_f[i/2]['qpf_night'][unit[4]]

    snow_night = simple_f[i/2]['snow_night'][unit[8]]

    # Show night accumulated precip amts
    if 'Night' in title:
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
