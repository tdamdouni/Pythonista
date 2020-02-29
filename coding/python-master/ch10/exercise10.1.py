from __future__ import print_function
#Exercise 10.1 Revise a previous program as follows: 
#Read and parse the From lines and pull out the addresses from the line. 
#Count the number of messages from each person using a dictionary.

#After all the data has been read, print the person with the most commits by creating
#a list of (count, email) tuples from the dictionary. Then sort the list in reverse order
#and print out the person who has the most commits.

fhand = open('mbox-short.txt')
my_dictionary = dict()

for line in fhand:
    if line.startswith('From '):
        at_position = line.find(" ")
        #print line[ :at_position]
        space_position = line.find(" ", 5)
        address = line[at_position+1:space_position]
        #print address
        my_dictionary[address] = my_dictionary.get(address,0) + 1

#print my_dictionary

lst = list()
for key, val in my_dictionary.items():
    lst.append((val, key))

lst.sort(reverse=True)


for key, val in lst: 
    print(key, val)
    


