from __future__ import print_function
# http://stackoverflow.com/questions/36856011/convert-csv-to-a-html-table-format-and-store-in-a-html-file

import sys
import csv
if len(sys.argv) < 3:
	print("Usage: csvToTable.py csv_file html_file")
	exit(1)
	
# Open the CSV file for reading

	reader = csv.reader(open(sys.argv[1]))
	
# Create the HTML file for output

	htmlfile = open(sys.argv[2],"w")
	
# initialize rownum variable
	rownum = 0
	
# write <table> tag

	htmlfile.write('<table>')
	
# generate table contents

for row in reader: # Read a single row from the CSV file

# write header row. assumes first row in csv contains header
	if rownum == 0:
		htmlfile.write('<tr>') # write <tr> tag
		for column in row:
			htmlfile.write('<th>' + column + '</th>')
		htmlfile.write('</tr>')
		
#write all other rows
	else:
		htmlfile.write('<tr>')
		for column in row:
			htmlfile.write('<td>' + column + '</td>')
		htmlfile.write('</tr>')
		
#increment row count
	rownum += 1
	
# write </table> tag
	htmlfile.write('</table>')
	
# print results to shell
	print("Created " + str(rownum) + " row table.")
	exit(0)

