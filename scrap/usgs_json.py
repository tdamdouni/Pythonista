#
# Example file for parsing and processing JSON
#

import urllib2
import json

def printResults(data):
	# Use the json module to load the string data into a dictionary
	theJSON = json.loads(data)

	# now we can access the contents of the JSON like any other Python object
	if 'title' in theJSON['metadata']:
		print theJSON['metadata']['title']

	# output the number of events, plus the magnitude and each event name
	count = theJSON['metadata']['count']
	print str(count) + ' events recorded.' + '\n'

	# for each event, print the place where it occurred
	for i in theJSON['features']:
		print i['properties']['place']
	print
	
	# print the events that only have a magnitude greater than 5
	for i in theJSON['features']:
		if i['properties']['mag'] >= 5.0:
			print "%2.1f" % i['properties']['mag'], i['properties']['place']

	# print only the events where at least 1 person reported feeling something
	print "\nEvents that were felt:"
	for i in theJSON['features']:
		feltReports = i['properties']['felt']
		if (feltReports != None) & (feltReports > 0):
			print "%2.1f" % i['properties']['mag'], i['properties']['place'], ' reported.'

def main():
	# define a variable to hold the source URL
	# In this case we'll use the free data feed from USGS
	# This feed lists all earthquakes for the last day larger than Mag 4.5
	url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson'

	# Open the URL and read the data
	webUrl = urllib2.urlopen(url)
	if webUrl.getcode() == 200:
		data = webUrl.read()
		printResults(data)
	else:
		print "Received an error from server, cannot retrieve results " + str(webUrl.getcode())


if __name__ == '__main__':
	main()
