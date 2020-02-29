from __future__ import print_function
#Exercise 9.2 Write a program that categorizes each mail message by which day
#of the week the commit was done. To do this look for lines that start with From,
#then look for the third word and keep a running count of each of the days of the
#week. At the end of the program print out the contents of your dictionary order
#does not matter.

fhand = open('mbox-short.txt')
weekday = dict()

for line in fhand:
    if line.startswith('From '):
        #print line.split()[2]
        running_count = line.split()[2]
        
        weekday[running_count] = weekday.get(running_count,0) + 1
        
        #if running_count not in weekday:
        #    weekday[running_count] = 1
        #else:
        #    weekday[running_count] += 1

print(weekday)
        
        