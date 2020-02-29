#!/usr/bin/python

# http://www.leancrew.com/all-this/2014/02/photo-locations-with-apple-maps/

from __future__ import print_function
import Image
import sys
import subprocess
import getopt

usage = """Usage: map [option] file

Options:
  -g    use Google instead of Apple Maps
  -b    use Bing instead of Apple Maps
  -h    show this help message

Get the GPS data from the given image file and open a map
to that location."""

# The map query URLs, with placeholders for longitude and latitude.
query = { 'apple': 'http://maps.apple.com/?q=%.6f,%.6f',
          'google': 'http://maps.google.com/maps?q=loc:%.6f,%.6f',
          'bing': 'http://www.bing.com/maps/?v=2&where1=%.6f,%.6f' }

# Magic EXIF number.
GPS = 34853

def degrees(dms):
	'''Return decimal degrees from degree, minute, second tuple.
	
	Each item in the tuple is itself a two-item tuple of a
	numerator and a denominator.'''
	
	deg, min, sec = dms
	deg = float(deg[0])/deg[1]
	min = float(min[0])/min[1]
	sec = float(sec[0])/sec[1]
	return deg + min/60 + sec/3600
	
def coord_pair(gps):
	'Return the latitude, longitude pair from GPS EXIF data.'
	
	# Magic GPS EXIF numbers.
	LATREF = 1; LAT = 2
	LONGREF = 3; LONG = 4
	
	lat = degrees(gps[LAT])
	if gps[LATREF] == 'S':
		lat = -lat
	long = degrees(gps[LONG])
	if gps[LONGREF] == 'W':
		long = -long
	return (lat, long)
	
# Parse the options.
try:
	options, args = getopt.getopt(sys.argv[1:], 'gbh')
except getopt.GetoptError as err:
	print(str(err))
	sys.exit(2)
	
# Set the option values.
engine = 'apple'           # default
for o, a in options:
	if o == '-g':
		engine = 'google'
	elif o == '-b':
		engine = 'bing'
	else:
		print(usage)
		sys.exit()
		
try:
	# Open the photo file and read the EXIF data.
	exif = Image.open(args[0])._getexif()
except AttributeError:
	print("No EXIF data for %s" % args[0])
	sys.exit()
except IOError:
	print("Couldn't open %s" % args[0])
	sys.exit()
	
try:
	# Read the GPS info.
	gps = exif[GPS]
	latitude, longitude = coord_pair(gps)
except KeyError:
	print("No GPS data for %s" % args[0])
	sys.exit(1)
	
# Open the map.
subprocess.call(['open', query[engine] % (latitude, longitude)])

