# https://forum.omz-software.com/topic/3442/attribute-error-on-csv-write/8

import csv

chars = 'abcdefghij'
matrix = [[x for x in chars.lower()], [i for i in range(10)],
          [x for x in chars.upper()], [i + .5 for i in range(10)]]

with open('testfile.cvs', 'w', newline='') as out_file:
	csv.writer(out_file).writerows(matrix)

