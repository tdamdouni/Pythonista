# https://forum.omz-software.com/topic/4011/have-csv-file-s-url/9

# @omz

import csv
import requests
import time
import dateutil
import matplotlib.pyplot as plt

url = 'http://data.sparkfun.com/output/YGa69ObX6WFj9mYa4EmW.csv?page=1'

r = requests.get(url)
retry_count = 0
while r.status_code != 200 and retry_count < 10:
	print('status code %i, retrying...' % r.status_code)
	retry_count += 1
	time.sleep(2)
	r = requests.get(url)
	
if r.status_code == 200:
	dates = []
	tips = []
	lines = r.text.splitlines()[1:] # Strip header line
	for row in csv.reader(lines):
		dates.append(dateutil.parser.parse(row[2]))
		tips.append(int(row[1]))
		
	plt.plot_date(dates, tips, fmt='-')
	plt.show()
else:
	print('Failed to load data')

