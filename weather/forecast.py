# -*- coding: utf-8 -*-
import urllib2, json, location, datetime
import ui
v = ui.load_view('forecast')
hightemp = v['hightemp']
temperature = v['temp']
lowtemp = v['lowtemp']
loc = v['location']
des = v['description']
today = datetime.datetime.now()

def place():
	address_dict = location.get_location()
	location.start_updates()
	
	location.stop_updates()
	latitude = address_dict['latitude']
	longitude = address_dict['longitude']
	api(latitude, longitude)

def api(latitude, longitude):
	url = 'http://api.openweathermap.org/data/2.5/forecast/daily?lat={0}&lon={1}&mode=json&units=imperial' .format (latitude, longitude)
	api = urllib2.urlopen(url)
	forecastapi = json.load(api)
	url = 'http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&mode=json&units=imperial' .format (latitude, longitude)
	api = urllib2.urlopen(url)
	weatherapi = json.load(api)
	forecast(weatherapi, forecastapi)
 
def forecast(weatherapi, forecastapi):
	temperature.text = str(round(weatherapi['main']['temp'], 0)) + '°'
	loc.text = str(weatherapi['name'])
	hightemp.text = str(weatherapi['main']['temp_max']) + '°'
	lowtemp.text = str(round(weatherapi['main']['temp_min'], 0)) + '°'
	des.text = weatherapi['weather'][0]['main']
	today = datetime.datetime.now()
	week = [(today + datetime.timedelta(days=i)).strftime('%A') for i in xrange(7)]
	for day in week:
		v['monday'].text = str(round(forecastapi['list'][week.index('Monday')]['temp']['day'],0)) + '°'
		v['tuesday'].text = str(round(forecastapi['list'][week.index('Tuesday')]['temp']['day'],0)) + '°'
		v['wednesday'].text = str(round(forecastapi['list'][week.index('Wednesday')]['temp']['day'],0)) + '°'
		v['thursday'].text = str(round(forecastapi['list'][week.index('Thursday')]['temp']['day'],0)) + '°'
		v['friday'].text = str(round(forecastapi['list'][week.index('Friday')]['temp']['day'],0)) + '°'
		v['saturday'].text = str(round(forecastapi['list'][week.index('Saturday')]['temp']['day'],0)) + '°'
		v['sunday'].text = str(round(forecastapi['list'][week.index('Sunday')]['temp']['day'],0)) + '°'
		desc = forecastapi['list'][week.index(day)]['weather'][0]['main']

place()
v.present('sheet')
