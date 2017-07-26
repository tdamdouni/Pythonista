#!python2

# https://forum.omz-software.com/topic/4011/have-csv-file-s-url/3

# http://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str

import csv, requests

url = 'http://data.sparkfun.com/output/YGa69ObX6WFj9mYa4EmW.csv'
filename = url.split('/')[-1]
with open(filename, 'wb') as out_file:
	out_file.write(requests.get(url).content)
	
with open(filename, 'rb') as in_file:
	for row in csv.reader(in_file):
		print(', '.join(row))

