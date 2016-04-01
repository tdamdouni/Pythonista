# @weather
# Should you take your umbrella? http://philgr.com/blog/should-you-take-your-umbrella-today
# https://gist.github.com/philgruneich/9038536 
# -*- coding: utf-8 -*-
from json import loads
from requests import get
import location
from datetime import date
import time
from console import alert

# Customization here
APItoken = 'Insert your API token here'

leave_home_hour = 8
arrive_work_hour = 10
leave_work_hour = 19
arrive_home_hour = 21
# End of customization

location.start_updates()
place = location.get_location()
location.stop_updates()

latitude = str(place['latitude'])
longitude = str(place['longitude'])

request_url = 'https://api.forecast.io/forecast/' + APItoken + '/' + latitude + ',' + longitude

r = get(request_url)
data = loads(r.text)
weather = data['hourly']['data']

# Time math
## 1 hour = 3600
today = time.mktime(date.today().timetuple())

leave_home = leave_home_hour * 3600 + today
arrive_work = arrive_work_hour * 3600 + today
leave_work = leave_work_hour * 3600 + today
arrive_home = arrive_home_hour * 3600 + today

day_precip = [hour['precipProbability'] for hour in weather if leave_home <= hour['time'] <= arrive_home]
leave_precip = [errands['precipProbability'] for errands in weather if leave_home <= errands['time'] <= arrive_work]
arrive_precip = [errands['precipProbability'] for errands in weather if leave_work <= errands['time'] <= arrive_home]

def checkDivide(precip):
	if len(precip) == 0:
		return 1
	else:
		return len(precip)

maybe_umbrella = sum(day_precip)/checkDivide(day_precip)
leave_umbrella = sum(leave_precip)/checkDivide(leave_precip)
arrive_umbrella = sum(arrive_precip)/checkDivide(arrive_precip)

if leave_umbrella >= 0.4 or arrive_umbrella >= 0.4:
	alert('YES','It\'s rainings cats and dogs out there.')
elif maybe_umbrella >= 0.4:
	alert('MAYBE', 'You just can\'t trust the weather.')
else:
	alert('NO', 'You\'ll only forget it somewhere.')