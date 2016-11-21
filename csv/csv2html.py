#!/usr/bin/python

# https://gist.github.com/enigmaticape/4016913#file-csv2html-py

# http://www.enigmaticape.com/blog/simple-python-script-for-simple-csv-to-html-table-rows

import sys
import os
import csv
import string

if len( sys.argv ) < 2 :
	sys.stderr.write( sys.argv[ 0 ]  +
	": usage - "   +
	sys.argv[ 0 ]  + "GDPdU-14.csv" )
	sys.exit()
	
if not os.path.exists(sys.argv[ 1 ]):
	sys.stderr.write( sys.argv[ 1 ] + " not found \n" )
	sys.exit()
	
	
with open( sys.argv[ 1 ], 'rb') as csvfile:
	table_string = ""
	reader       = csv.reader( csvfile )
	
	for row in reader:
		table_string += "<tr>" + \
		"<td>" + \
		string.join( row, "</td><td>" ) + \
		"</td>" + \
		"</tr>\n"
		
	sys.stdout.write( table_string )

