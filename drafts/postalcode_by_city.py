# -*- coding: utf-8 -*-
from console import alert
from json import loads
from sys import argv, exit
from urllib import urlopen, quote
import webbrowser
 
def error_dialog(title, message):
	'''
	a diaolog box for error messages.
	'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts://')
	exit(message)
 
def handle_data(data):
	'''
	process json response from zippopotamus.
	will return a markdown list of items.
	'''
	city_json = loads(data)
	output = ''
	for item in city_json['places']:
		output += '- City: {place}, Post code: {postcode}\n'.format(place=item['place name'], postcode=item['post code'])
	return output
 
def get_by_city(data):
	'''
	get all possible post codes for a city in
	the given country.
	'''
	api_url_base = 'http://api.zippopotam.us/{country}/{state}/{city}'
	try:
		city_, state_, country_= [item.strip() for item in data.split(',')]
	except Exception as err:
		error_dialog(str(err.__class__), err.message)
 
	try:
		response = urlopen(api_url_base.format(country=country_, state=state_, city=city_))
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() == 200:
		city_data = handle_data(response.read())
		webbrowser.open('drafts://x-callback-url/create?text={0}'.format(quote(city_data)))
	else:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
 
if __name__ == '__main__':
	get_by_city(argv[1])