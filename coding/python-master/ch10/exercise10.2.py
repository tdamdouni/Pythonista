from __future__ import print_function
#Write a program to read through the mbox-short.txt and 
#figure out the distribution by hour of the day for each of the messages. 
#You can pull the hour out from the 'From ' line by finding the time and 
#then splitting the string a second time using a colon.

#Once you have accumulated the counts for each hour
#print out the counts, sorted by hour as shown below.

fhand = open('mbox-short.txt')
my_dictionary = dict()

for line in fhand:
    if line.startswith('From '):
        at_position = line.find(':')
        #print at_position
        hour = line[at_position-2 : at_position]
        #print hour
        #timing.append(hour)
        my_dictionary[hour] = my_dictionary.get(hour,0) + 1 

#print my_dictionary #this is my key value dictionary

lst = list()
for key, val in my_dictionary.items():
    lst.append((key, val))

lst.sort()

for key, val in lst: 
    print(key, val)

