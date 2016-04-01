# -*- coding: utf-8 -*-
import clipboard
from console import alert
import datetime
from json import loads
from sys import argv, exit
from urllib import urlopen, quote
import webbrowser
 
# You can leave this an empty string, if you do
# do not want metric units.
UNITS = '&units=metric'
 
def error_dialog(title, message):
	'''
	A diaolog box for error messages.
	'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts://')
	exit(message)
 
def filter_data(data):
	'''
	Create output string from response.
	'''
	weather = loads(data)
	city = weather['name']
	lat = weather['coord']['lat']
	lon = weather['coord']['lon']
	sunrise = datetime.datetime.fromtimestamp(int(weather['sys']['sunrise']))
	sunset = datetime.datetime.fromtimestamp(int(weather['sys']['sunset']))
	temperature = int(weather['main']['temp'])
	description = weather['weather'][0]['description'].capitalize()
	clouds = weather['clouds']['all']
	humidity = weather['main']['humidity']
	output = 'Weather in {}\nLatitude: {}\nLongitude: {}\n{}\nTemperature: {}°C {}\nClouds: {}%\nHumidity: {}%\nSunrise: {}\nSunset: {}\n\nData provided by www.openweathermap.org'.format(city, lat, lon, '=' * 20, temperature, description, clouds, humidity, sunrise, sunset)
	return output
 
def get_current_weather_in(data):
	'''
	Get current weather data.
	'''
	api_url_base = 'http://api.openweathermap.org/data/2.5/weather?q={data}{unit}'
	try:
		response = urlopen(api_url_base.format(data=data,
		                              unit=UNITS))
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() == 200:
		weather_data = filter_data(response.read())
		webbrowser.open('drafts://x-callback-url/create?text={0}'.format(quote(weather_data)))
	else:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
 
if __name__ == '__main__':
	get_current_weather_in(argv[1])