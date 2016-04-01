# coding: utf-8
#coding: utf-8
# https://gist.github.com/kultprok/e559a1274aa2e16568c4
# http://kulturproktologie.de/?p=4680
import clipboard
from console import alert
import datetime
from json import loads
from sys import argv, exit
from urllib import urlopen, quote
import webbrowser

weather_codes = {200: 'Gewitter mit leichtem Regen',
201: 'Gewitter mit Regen',
202: 'Gewitter mit schwerem Regen',
210: 'Leichtes Gewitter',
211: 'Gewitter',
212: 'Schweres Gewitter',
221: 'Zerklüftetes Gewitter',
230: 'Gewitter mit leichtem Nieselregen',
231: 'Gewitter mit Nieselregen',
232: 'Gewitter mit schwerem Nieselregen',
300: 'Leichtes Nieseln',
301: 'Nieseln',
302: 'Schweres Nieseln',
310: 'Leichter Nieselregen',
311: 'Nieselregen',
312: 'Schwerer Nieselregen',
321: 'Nieselschauer',
500: 'Leichter Regen',
501: 'Regen',
502: 'Schwerer Regen',
503: 'Sehr schwerer Regen',
504: 'Extremer Regen',
511: 'Überfrierender Regen',
520: 'Leichte Regenschauer',
521: 'Regenschauer',
522: 'Schwere Regenschauer',
600: 'Leichter Schnefall',
601: 'Schnefall',
602: 'Schwerer Schneefall',
611: 'Graupel',
621: 'Schneeschauer',
701: 'Leichter Nebel',
711: 'Rauch',
721: 'Dunst',
731: 'Sandverwirbelungen',
741: 'Nebel',
800: 'Klarer Himmel',
801: 'Vereinzelt Wolken',
802: 'Leicht bewölkt',
803: 'Aufgerissene Wolkendecke',
804: 'Bedeckt',
900: 'Tornado',
901: 'Tropensturm',
902: 'Hurrikan',
903: 'Kalt',
904: 'Heiß',
905: 'Windig',
906: 'Hagel'}

def error_dialog(title, message):
	'''A diaolog box for error messages.'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts4://')
	exit(message)

def filter_data(data):
	'''create output string from response'''
	weather = loads(data)
	city = weather['name']
	lat = weather['coord']['lat']
	lon = weather['coord']['lon']
	sunrise = datetime.datetime.fromtimestamp(int(weather['sys']['sunrise']))
	sunset = datetime.datetime.fromtimestamp(int(weather['sys']['sunset']))
	temperature = int(weather['main']['temp'])
	description = weather_codes[weather['weather'][0]['id']]
	clouds = weather['clouds']['all']
	humidity = weather['main']['humidity']
	output = 'Wetter in {}\nBreitengrad: {}\tLängengrad: {}\n{}\nTemperatur: {}°C {}\nWolkendichte: {}%\nLuftfeuchtigkeit: {}%\nSonnenaufgang: {}\nSonnenuntergang: {}\n\nDaten bereitgestellt von www.openweathermap.org'.format(city, lat, lon, '=' * 20, temperature, description, clouds, humidity, sunrise, sunset)
	return output

def get_current_weather_in(data):
	'''get current weather data'''
	api_url_base = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric'
	try:
		response = urlopen(api_url_base.format(data))
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() == 200:
		weather_data = filter_data(response.read())
		webbrowser.open('drafts4://x-callback-url/create?text={0}'.format(quote(weather_data)))
	else:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))

if __name__ == '__main__':
	get_current_weather_in(argv[1])