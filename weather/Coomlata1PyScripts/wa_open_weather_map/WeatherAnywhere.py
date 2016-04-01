#coding: utf-8

# Name: WeatherAnywhere.py
# Author: John Coomler
# v1.0: 02/07/2015 to 02/15/2015-Created
# v1.1: 02/19/2015-Tightened up code and
# made function calls to retrieve weather
# data for printing from main(). Many
# thanks to @cclauss for his continued
# expertise, input, & support in sorting
# out and improving the code.
# v1.2: 02/20/2015-More code cleanup,
# improved string formatting techniques,
# and much improved error handling.
# v1.3: 02/21/2015-Added function to
# download weather icons if any or all
# are missing. More code cleanup.
# v1.4: 02/23/2015-Conversion functions
# renamed & now return numbers instead of
# strings, added ability to convert
# from imperial to metric units.
# v1.5: 02/24/2015-Cleanup of date string
# formatting and now show all precip
# types.
# v1.6: 03/04/2015-Added ability to store
# weather icons in a sub folder of script
# folder. Created 2 new functions,
# 'pick_your_weather' &
# 'get_weather_icons' to aid in porting
# script over to a scene.
# v1.7: 03/05/2015-Improved code in icon
# download process code to prevent IO errors.
'''
This script provides current and multi day
weather forecasts for any city you name,
or coordinates you are currently located
in, using the api available from
www.openweathermap.org. The inspiration
for this script came from https://
github.com/cclauss/weather_where_you_are/
weather_where_you_are.py. The conversion
functions used here were found at http://
jim-easterbrook.github.io/pywws/doc/en/
html/_modules/pywws/conversions.html
'''
import console
import csv
import datetime
import location
from PIL import Image
import requests
import sys

# Global variables
icons=[]
weather_icons=[]
missing_icons=[]
icon_path='./icons/'

# Number of days in advanced forecast
day_count=7
# Change to 'metric' if desired
imperial_or_metric='imperial'

if imperial_or_metric=='imperial':
  unit=['F','mph','in','in']
else:
  unit=['C','mps','hPa','mm']

def pick_your_weather():
  city = country = id = ''
  lat = lon = 0

  # Pick a weather source
  try:
    ans=console.alert('Choose Your Weather Source:','','From Your Current Location','From Entering a City Name','From A Pick List of Cities')
    if ans==1:
      # Weather where you are
      print 'Gathering weather data from where you are...'
      # Get lat & lon of where you are
      lat,lon=get_current_lat_lon()
    elif ans==2:
      # Enter a city & country
      msg='Enter a city and country in format "'"New York, US"'": '
      ans=console.input_alert(msg).title()
      if ans:
        print('='*20)
        print 'Gathering weather data for '+ans
        city=ans.replace(' ','+')
    elif ans==3:
      # Pick from list
      theCity,country,id=city_ids()
      print('='*20)
      if id:
        print 'Gathering weather data for '+theCity+', '+country
  except Exception as e:
    sys.exit('Error: {}'.format(e))

  # Call api from www.openweathermap.org
  w,f=get_weather_dicts(lat,lon,city,id)
  return w,f

def get_current_lat_lon():
  # Retrieve lat & lon from current locale
  location.start_updates()
  # Delay sometimes improves accuracy
  #time.sleep(1)
  address_dict = location.get_location()
  location.stop_updates()
  return address_dict['latitude'],address_dict['longitude']

def city_ids(filename='cities.csv'):
  try:
    with open(filename) as in_file:
      # Read each line and store in list
      ids = [row for row in csv.reader(in_file)]
  except IOError as e:
    sys.exit('IOError in city_ids(): {}'.format(e))
  if not ids:
    sys.exit('No cities found in: {}'.format(filename))
  for i, id in enumerate(ids):
    # Align numbers neatly in printed list of cities & countries
    print('{:>7}. {}, {}'.format(i, id[0], id[1]))
  while True:
    try:
      ans = int(raw_input('\nEnter number of desired city: '))
      # Retrieve data from proper row,
      city, country, id = ids[ans]
      return city, country, id
    except (IndexError, ValueError):
      print('Please enter a vaild number.')

def get_weather_dicts(lat,lon,city='',id=''):
  url_fmt = 'http://api.openweathermap.org/data/2.5/{}?{}'
  if city: # From entered city
    fmt = 'q={}&type=accurate&units={}'
    query = fmt.format(city, imperial_or_metric)
  elif id: # From list
    fmt = 'id={}&type=accurate&units={}'
    query = fmt.format(id, imperial_or_metric)
  else: # From where you are now
    fmt = 'lat={}&lon={}&type=accurate&units={}'
    query = fmt.format(lat, lon, imperial_or_metric)

  w_url = url_fmt.format('weather', query)

  query += '&cnt={}'.format(day_count)
  f_url = url_fmt.format('forecast/daily', query)
  try:
    weather = requests.get(w_url).json()
    forecast = requests.get(f_url).json()
    #import pprint;pprint.pprint(weather)
    #import pprint;pprint.pprint(forecast)
    #See: http://bugs.openweathermap.org/projects/api/wiki
    #sys.exit()
  except requests.ConnectionError:
    print('=' * 20) # console.clear()
    sys.exit('Weather servers are busy. Try again in a few minutes...')
  return weather, forecast

# Conversion functions:
def hPa_to_inches(hPa):
  # Convert pressure from hectopascals/millibar to inches of mecury
  return hPa/33.86389

def mm_to_inches(mm):
  # Convert rain or snowfall from mm to in
  return mm/25.4

def mps_to_mph(mps):
  # Convert wind from meters/sec to mph
  return mps*3.6/1.609344

def wind_chill(temp,wind):
  '''
  Compute wind chill using formula from
  http://en.wikipedia.org/wiki/wind_chill
  '''
  temp=float(temp)
  wind=float(wind)

  if imperial_or_metric=='imperial':
    if wind<=3 or temp>50:
      return temp
    return min(35.74+(temp*0.6215)+(((0.4275*temp)-35.75)*(wind**0.16)),temp)
  else:
    wind_kph=wind*3.6
    if wind_kph<=4.8 or temp>10:
      return temp
    return min(13.12+(temp*0.6215)+(((0.3965*temp)-11.37)*(wind_kph**0.16)),temp)

def wind_dir(deg):
  # Convert degrees to wind direction
  assert 0 <= deg <= 360, 'wind_dir({}): deg is out of bounds!'.format(deg)
  if   deg < 11.25:   return 'N'
  elif deg < 33.75:   return 'NNE'
  elif deg < 56.25:   return 'NE'
  elif deg < 78.75:   return 'ENE'
  elif deg < 101.25:  return 'E'
  elif deg < 123.75:  return 'ESE'
  elif deg < 146.25:  return 'SE'
  elif deg < 168.75:  return 'SSE'
  elif deg < 191.25:  return 'S'
  elif deg < 213.75:  return 'SSW'
  elif deg < 236.25:  return 'SW'
  elif deg < 258.75:  return 'WSW'
  elif deg < 281.25:  return 'W'
  elif deg < 303.75:  return 'WNW'
  elif deg < 326.25:  return 'NW'
  elif deg < 348.75:  return 'NNW'
  return 'N'

def get_weather_icons(w,f,icon_path):
  weather_icons=[]
  # Find icon name in current weather
  ico=icon_path+w['weather'][0]['icon']+'.png'
  weather_icons.append(ico)
  # Find icon names in forecasted weather
  for idx in xrange(len(f['list'])):
    ico=icon_path+f['list'][idx]['weather'][0]['icon']+'.png'
    weather_icons.append(ico)
  return weather_icons

def download_weather_icons(icon_path):
  # Downloads any missing weather icons
  # from www.openweathermap.org
  import os
  fmt = 'Downloading {} from {} ...'
  for i in (1,2,3,4,9,10,11,13,50):
    filenames = ('{:02}d.png'.format(i), '{:02}n.png'.format(i))
    for filename in filenames:
      if os.path.exists(icon_path + filename):
        continue
      url = 'http://openweathermap.org/img/w/' + filename
      # Create icon folder if it doesn't exist
      if not os.path.exists(icon_path):
        os.makedirs(icon_path)
      # Write .png file to icon folder  
      with open(icon_path + filename, 'w') as out_file:
        try:
          print(fmt.format(filename, url))
          out_file.write(requests.get(url).content)
        except requests.ConnectionError as e:
          print('ConnectionError on {}: {}'.format(i ,e))
      print('Done.')

def get_current_weather(w):
  # Pressure & convert to inches
  if imperial_or_metric=='imperial':
    w['main']['pressure']=hPa_to_inches(w['main']['pressure'])

  # Capitalize weather description
  w['weather'][0]['description']=w['weather'][0]['description'].title()

  # Convert wind degrees to wind direction
  w['wind']['deg']=wind_dir(w['wind']['deg'])

  # Convert wind speed to mph
  if imperial_or_metric=='imperial':
    w['wind']['speed']=mps_to_mph(w['wind']['speed'])

  # Get wind chill factor using temp & wind speed
  chill='{:.0f}'.format(wind_chill(w['main']['temp'],w['wind']['speed']))

  try:
    # Get wind gusts and covert to mph, although they aren't always listed'
    if imperial_or_metric=='imperial':
      w['wind']['gust']=mps_to_mph(w['wind']['gust'])+float(w['wind']['speed'])
    else:
      w['wind']['gust']=w['wind']['gust']+w['wind']['speed']
    gusts='w/ gusts to {:.0f} {}'.format(w['wind']['gust'],unit[1])
  except:
    gusts=''
  # Convert timestamp of weather into a datetime
  w['dt']=datetime.datetime.fromtimestamp(int(w['dt']))

  # Do same for sunrise and sunset timestamps
  for item in ('sunrise', 'sunset'):
    w['sys'][item]=datetime.datetime.fromtimestamp(int(w['sys'][item]))

  # Return the reformated data
  return '''Today's Weather in {name}:\n
Current Conditions for {dt:%A\n  %m-%d-%Y @ %I:%M %p}:
  {weather[0][description]}
  Clouds: {clouds[all]}%
  Temperature: {main[temp]:.0f}° {}
  Humidity: {main[humidity]}%
  Barometric Pressure: {main[pressure]:.2f} {}
  Wind: {wind[deg]} @ {wind[speed]:.0f} {} {}
  Feels Like: {}° {}
  Sunrise: {sys[sunrise]:%I:%M %p}
  Sunset: {sys[sunset]:%I:%M %p}\n'''.format(unit[0],unit[2],unit[1],gusts,chill,unit[0],**w)

def get_day_forecast(f):
  # Convert timestamp of forecast day into a datetime
  f['dt'] = datetime.datetime.fromtimestamp(int(f['dt']))

  # Capitalize weather description
  f['weather'][0]['description'] = f['weather'][0]['description'].title()

  # Get type of preciptation
  precip_type=f['weather'][0]['main']
  # Get measured amts of precip
  if precip_type in ('Rain', 'Snow'):
    try:
      # Convert precip amt to inches
      fmt = 'Expected {} Vol for 3 hrs: {:.2f} {}'
      if imperial_or_metric=='imperial':
        precip_type = fmt.format(precip_type, mm_to_inches(f[precip_type.lower()]),unit[3])
      else:
        precip_type = fmt.format(precip_type,f[precip_type.lower()],unit[3])
    except:
      # Sometimes precip amts aren't listed
      pass
  elif precip_type=='Clouds':
    precip_type = 'No Rain Expected'

  # Pressure formatted to inches
  if imperial_or_metric=='imperial':
    f['pressure'] = hPa_to_inches(f['pressure'])

  # Wind direction and speed
  f['deg'] = wind_dir(f['deg'])
  if imperial_or_metric=='imperial':
    f['speed'] = mps_to_mph(f['speed'])

  return '''
Forecast for {dt:%A %m-%d-%Y}
    {weather[0][description]}
    {}
    Clouds:   {clouds:>3}%
    High:     {temp[max]:>3.0f}° {}
    Low:      {temp[min]:>3.0f}° {}
    Humidity: {humidity:>3}%
    Barometric Pressure: {pressure:.2f} {}
    Wind: {deg} @ {speed:.0f} {}'''.format(precip_type,unit[0], unit[0],unit[2],unit[1],**f)

def get_forecast(f):
  daily_forecasts = [get_day_forecast(daily) for daily in f['list']]
  fmt = 'Extended {} Day Forecast for {city[name]}:\n{}'
  return fmt.format(len(daily_forecasts), '\n'.join(daily_forecasts), **f)

def main():
  console.clear()
  w,f=pick_your_weather()

  # Get array of weather icons
  icons=get_weather_icons(w,f,icon_path)

  print('='*20)

  # Print current conditions to console
  try:
    # Open, resize & show icon for current weather, which is 1st one in array
    img=Image.open(icons[0]).resize((25,25),Image.ANTIALIAS)
    img.show()
  except:
    missing_icons.append(icons[0])

  print(get_current_weather(w))
  '''
  Printing the extended forecast to the
  console involves a bit more code because
  we are inserting a weather icon at each
  blank line.
  '''
  extended_f=get_forecast(f).split('\n')
  '''
  Start getting icons from element 1, as
  we already used element 0 for current
  weather.
  '''
  count=1
  for line in extended_f:
    # Look for blank lines
    if not line and count<=(day_count):
      ico=icons[count]
      try:
        # Open, resize and show weather icon
        img=Image.open(ico).resize((25,25),Image.ANTIALIAS)
        img.show()
      except:
        missing_icons.append(ico)
      count += 1
    print line

  print '\nWeather information provided by openweathermap.org'

  if missing_icons:
    ans=console.alert('Weather Icon(s) Missing:','','Download Them Now')
    if ans==1:
      download_weather_icons(icon_path)

if __name__ == '__main__':
  main()
