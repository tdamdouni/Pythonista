# https://forum.omz-software.com/topic/4011/have-csv-file-s-url/10

# @DaveGadgeteer Perhaps the best approach would be to separate the data download from the data parsing as done in https://forum.omz-software.com/topic/4011/have-csv-file-s-url/6. That way, you do not have to hit the URL resource/server so often.

# You can then read the local file and convert it into a list of wearher_readings ...

import collections, csv

filename = 'YGa69ObX6WFj9mYa4EmW.csv'

with open(filename, 'r') as in_file:
	data = []  # a list of weather_readings
	weather_reading = None
	for row in csv.reader(in_file):
		if weather_reading:
			data.append(weather_reading(*row))
		else:  # create a custom datatype from the header record
			weather_reading = collections.namedtuple('weather_reading', row)
			
print('\n'.join(str(x) for x in data))
# weather_reading(time='1952', tips='773', timestamp='2017-04-30T20:42:59.017Z')

# https://forum.omz-software.com/topic/4011/have-csv-file-s-url/11

# Works nicely but the third field is bytes instead of datetime64[ms]

import numpy
filename = 'YGa69ObX6WFj9mYa4EmW.csv'
a = numpy.recfromcsv(filename)
print(a[0])

