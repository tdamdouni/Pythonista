# https://forum.omz-software.com/topic/4011/have-csv-file-s-url/7

# Always easier with requests...

import csv, requests

url = 'http://data.sparkfun.com/output/YGa69ObX6WFj9mYa4EmW.csv'
filename = url.split('/')[-1]
with open(filename, 'wb') as out_file:
	out_file.write(requests.get(url).content)
	
# _csv.Error: iterator should return strings, not bytes (did you open the file in text mode?)
# change 'rb' to 'r'
with open(filename, 'rb') as in_file:
	for row in csv.reader(in_file):
		print(', '.join(row))
		
# Or if you want to do it all in RAM...

#!/usr/bin/env python3

import csv, io, requests

url = 'http://data.sparkfun.com/output/YGa69ObX6WFj9mYa4EmW.csv'
with io.StringIO(requests.get(url).text) as mem_file:
	for row in csv.reader(mem_file):
		print(', '.join(row))
		
# I just learned that csv.reader accepts any iterator, and not just file-like objects, so you could make this slightly shorter:

import csv, requests

url = 'http://data.sparkfun.com/output/YGa69ObX6WFj9mYa4EmW.csv'
for row in csv.reader(requests.get(url).text.splitlines()):
	print(', '.join(row))

