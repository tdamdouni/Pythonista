import csv
with open('my_file.csv') as in_file:
    for row in csv.reader(in_file):
        print ', '.join(row)
