#! /usr/bin/env python
'''gps.py
A quick and dirty Pythonista script for sending your GPS location to IFTTT. Uses
Pythonista: http://n8h.me/1dntsEH
and 
Launch Center Pro: http://n8h.me/1fcRfrn

Recommended LCP URL action:
pythonista://{{gps}}?action=run
'''

import location
import time
import console
import datetime
import webbrowser
import urllib

console.clear()
console.show_activity()

# Start getting the location
location.start_updates()

time.sleep(5)
my_loc = location.get_location()
acc = my_loc['horizontal_accuracy']

best_loc = my_loc
best_acc = my_loc['horizontal_accuracy']

location.stop_updates()

# example output of location.get_location()
# 'vertical_accuracy': 14.31443007336287
# 'horizontal_accuracy': 1414.0
# 'timestamp': 1408639887.267081
# 'altitude': 1514.9893798828125
# 'longitude': -146.64942423483025
# 'course': -1.0
# 'latitude': 39.10669415937833
# 'speed': -1.0

datestamp = datetime.datetime.fromtimestamp(best_loc['timestamp'])
time_str = datestamp.strftime('%Y-%m-%d %H:%M:%S')
lat = best_loc['latitude']
lon = best_loc['longitude']
address = location.reverse_geocode({'latitude': lat, 'longitude': lon})
address = address[0]['Street'] + ', ' + address[0]['City'] + ', ' + address[0]['Country']

cmd = 'launch://ifttt/trigger?name=Panic&Value1={}&Value2={}&Value3={}&Value4={}&Value5={}'.format(urllib.quote(time_str), best_acc, lat, lon, urllib.quote(address))
webbrowser.open(cmd)
