# -*- coding: utf-8 -*-
# iTC Sales Report Downloader

# When you run this for the first time, you'll need to enter your
# iTunes Connect login and vendor ID. You can find the vendor ID
# on the iTunes Connect website by navigating to "Sales and Trends";
# it's the number next to your name (top-left).

CURRENCY = 'EUR'
RESET_LOGIN = False # Set to True to remove login from keychain

import keychain
import requests
import gzip
import os
import tempfile
import datetime
import time
import json
import csv
from StringIO import StringIO
from collections import defaultdict
import console

try:
	import prettytable
except ImportError:
	print 'Downloading required prettytable module...'
	import urllib
	urllib.urlretrieve('http://prettytable.googlecode.com/svn/trunk/prettytable.py', 'prettytable.py')
	import prettytable

class ITCDownloadError (Exception): pass

def load_report(user, pw, vendor_id, date_str, data_dir):
	# Check if the report has already been downloaded, and return cached data if possible:
	report_path = os.path.join(data_dir, date_str + '.txt')
	try:
		with open(report_path, 'r') as f:
			s = f.read()
			return s
	except IOError:
		pass
	# Get the report from iTunes Connect:
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	payload = {'USERNAME': user, 'PASSWORD': pw, 'VNDNUMBER': vendor_id, 'TYPEOFREPORT': 'Sales', 'DATETYPE': 'Daily', 'REPORTTYPE': 'Summary', 'REPORTDATE': date_str}
	url = 'https://reportingitc.apple.com/autoingestion.tft'
	r = requests.post(url, data=payload, headers=headers)
	filename = r.headers.get('filename', None)
	if filename:
		# Decompress the .gz file:
		h, temp_path = tempfile.mkstemp()
		with open(temp_path, 'wb') as f:
			f.write(r.content)
		f = gzip.open(temp_path, 'rb')
		file_content = f.read()
		f.close()
		os.remove(temp_path)
		# Cache the report:
		with open(report_path, 'w') as f:
			f.write(file_content)
		return file_content
	elif r.headers.get('errormsg'):
		# Note: When queried too often, iTC will return error messages
		# that don't really make sense. It usually helps to wait a little.
		raise ITCDownloadError(r.headers.get('errormsg'))
	else:
		raise ITCDownloadError('Unknown download error')
	return None

def load_exchange_rates(cache_file):
	try:
		with open(cache_file, 'r') as f:
			data = json.load(f)
			last_update = data['last_update']
			if time.time() - last_update < 12 * 60 * 60:
				return data['rates']
	except (IOError, ValueError):
		pass
	print 'Updating exchange rates...'
	rates = {}
	currencies = ['USD', 'AED', 'AUD', 'BHD', 'BND', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'CZK', 'DKK', 'GBP', 'HUF', 'HKD', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'KWD', 'KZT', 'LKR', 'MUR', 'MXN', 'MYR', 'NOK', 'NPR', 'NZD', 'OMR', 'PKR', 'QAR', 'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TWD', 'ZAR', 'TRY']
	url = 'http://quote.yahoo.com/d/quotes.csv?s='
	url += '+'.join([c + 'EUR=X' for c in currencies])
	url += '&f=nl1'
	csv_string = requests.get(url).text
	for line in csv_string.splitlines():
		currency = line[1:4]
		rate = float(line[13:])
		rates[currency] = rate
	rates['EUR'] = 1.0
	data = {'last_update': time.time(), 'rates': rates}
	with open(cache_file, 'w') as f:
		json.dump(data, f)
	return rates

def convert_currency(value, from_currency, to_currency, rates):
	exchange_rate = rates.get(from_currency)
	eur = value * exchange_rate
	eur_rate = rates.get(to_currency)
	return eur / eur_rate

def parse_report(file_content):
	s = StringIO(file_content)
	csv_reader = csv.DictReader(s, delimiter='\t', quotechar='\\')
	return list(csv_reader)
		
def print_report_summary(title, file_content, rates, user_currency):
	if not file_content:
		return
	report = parse_report(file_content)
	proceeds_by_app = defaultdict(float)
	downloads_by_app = defaultdict(int)
	updates_by_app = defaultdict(int)
	for row in report:
		product_type_id = row['Product Type Identifier']
		units = int(row['Units'])
		app_name = row['Title']
		if '7' not in product_type_id:
			downloads_by_app[app_name] += units
		else:
			updates_by_app[app_name] += units
		currency = row['Currency of Proceeds']
		revenue_per_unit = float(row['Developer Proceeds'])
		revenue = revenue_per_unit * units
		conv_revenue = convert_currency(revenue, currency, user_currency, rates)
		proceeds_by_app[app_name] += conv_revenue
	revenue_title = '(' + CURRENCY  + ')'
	table = prettytable.PrettyTable([title, revenue_title, 'DL', 'UP'])
	table.align.update({title: 'l', revenue_title: 'r', 'DL': 'r', 'UP': 'r'})
	for app in sorted(proceeds_by_app):
		revenue_col = '%.02f' % (proceeds_by_app[app],)
		downloads_col = str(downloads_by_app[app])
		updates_col = str(updates_by_app[app])
		table.add_row([app, revenue_col, downloads_col, updates_col])
	total_revenue = '%.02f' % (sum(proceeds_by_app.values()),)
	total_downloads = sum(downloads_by_app.values())
	total_updates = sum(updates_by_app.values())
	table.add_row(['']*4)
	table.add_row(['TOTAL', total_revenue, total_downloads, total_updates])
	print table

def get_login():
	# Get login data from the keychain, if it has been saved already:
	login_data_json = keychain.get_password('iTunesConnect', 'Default')
	if login_data_json is None:
		# Show input dialogs for vendor id and user/password:
		vendor_id = console.input_alert('Vendor ID (8xxxxxxx)')
		user, password = console.login_alert('iTunes Connect Login')
		if user and password and vendor_id:
			# Save login data to keychain as json string:
			login_data = {'user': user, 'password': password, 'vendor_id': vendor_id}
			keychain.set_password('iTunesConnect', 'Default', json.dumps(login_data))
	else:
		login_data = json.loads(login_data_json)
		user = login_data['user']
		password = login_data['password']
		vendor_id = login_data['vendor_id']
	return user, password, vendor_id

def main():
	console.clear()
	if RESET_LOGIN:
		keychain.delete_password('iTunesConnect', 'Default')
	user, password, vendor_id = get_login()
	# Create the data folder:
	data_dir = 'ITCData'
	try:
		os.mkdir(data_dir)
	except OSError:
		pass
	# Load exchange rates (cached for 12 hours):
	rates = load_exchange_rates(os.path.join(data_dir, 'ExchangeRates.json'))
	# Load sales reports for the last 30 days:
	print 'Loading sales reports...\n'
	today = datetime.datetime.now()
	for i in xrange(30, 0, -1):
		d = today - datetime.timedelta(i)
		date_str = '%04i%02i%02i' % (d.year, d.month, d.day)
		display_date_str = '%04i-%02i-%02i' % (d.year, d.month, d.day)
		try:
			report = load_report(user, password, vendor_id, date_str, data_dir)
			print_report_summary(display_date_str, report, rates, CURRENCY)
		except ITCDownloadError, e:
			print 'Download failed for', display_date_str, '---', e
	del password

if __name__ == '__main__':
	main()
