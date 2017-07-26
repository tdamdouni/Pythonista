# https://forum.omz-software.com/topic/4011/have-csv-file-s-url/8

# Download and display csv data from rain gauge
from contextlib import closing

import csv, io, requests, urllib.request, codecs
from contextlib import closing
url = 'http://data.sparkfun.com/output/YGa69ObX6WFj9mYa4EmW.csv?page=1'

with closing(requests.get(url, stream=True)) as r:
	reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
	for row in reader:
		print (row)

