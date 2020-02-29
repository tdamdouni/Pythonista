from __future__ import print_function
# https://omz-forums.appspot.com/pythonista/post/5804501365686272
import csv
with open('my_file.csv') as in_file:
    for row in csv.reader(in_file):
        print(', '.join(row))
