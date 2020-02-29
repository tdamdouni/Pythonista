from __future__ import print_function
import csv

fhand = open('TSE_sample_data.csv')
csv_f = csv.reader(fhand)

my_list = []
date2words = dict()

with open('TSE_sample_data.csv') as fhand:
    next(csv_f)
    for row in csv_f:
        #print row[0]
        #print row[1]
        #print row[13]
        if int(row[13]) < 1283731200:
            #print row[:2]
            #print row[16]
            begin_date = int(row[13])
            
            if begin_date not in date2words:
                date2words[row[13]] = row[16]

            start_date = int(row[13])
            my_list.append(start_date)
            my_list.sort()
            a_list = date2words.keys()
        
        #else:
            
            #print "skip"
            
print(my_list)
print(date2words)

a_list.sort()

for key in a_list:
    print(key, date2words[key])

#for key in date2words:
#   print int(key), date2words[key]

#with open('TSE_sample_data.csv','r') as fhand:
#    rows = []
#    i = 0
#    reader = csv.reader(fhand)
#    for line in reader:
#        if i == 0:
#            i = i +1
#            continue
#        time = line[1]
#        if float(time) < 1283731200:
#            rows.append(line)
#            print line
