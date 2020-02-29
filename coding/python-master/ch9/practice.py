from __future__ import print_function
#How to create a dictionary?

eng2esp = dict()

#print eng2span

#How to add items to a dictionary? This creates an item that maps from key one to value uno. If we print out the dictionary again, we'll see the key-value pair with a colon in between. 

eng2esp['one'] = 'uno'

#print eng2esp

#Adding more items to the dictionary with curly brackets. Note the order of the key-value pairs is not the same. The items of a dictionary are never indexed with integer indices.

eng2esp = {'one':'uno', 'two':'dos', 'three':'tres', 'four':'cuatro'}

#print eng2esp

#the in operator works on dictionaries and it tells you whether something appears as a key in the dictionary

#if 'one' in eng2esp:
#    print 'yes'
#else:
#    print 'no'

# to see whether something appears as a value in a dictionary, use the method called values. it returns the values as a list. then use the in operator. 

my_values = eng2esp.values()

#print my_values
#if 'uno' in my_values:
#    print "yes!"

#Here's some code that can count letters in a string using a dictionary. 

#word = 'brontosaurus'
#d = dict()
#for c in word:
#    if c not in d: #if the character c is not in the dictionary
#        d[c] = 1   #create a new item with key c and the initial value 1
#else: #if c is already in the dictionary we increment d[c]
#    d[c] = d[c] + 1

#print d

#disctionaries have a method called get that takes 1) a key value and 2) a default value. If the key appears in the dictionary, get returns the corresponding value; otherwise it returns the default value you've entered. 

#counts is the name of a dictionary
#get is a built in capability for dictionaries
#it takes two parameters -- 1) a key value and 2) a default value.
#the first parameter is a key name
#the second parameter is a value to give back if the key name does not exist. It's a default value you've set if the key name does not exist. 


#counts = {'chuck': 1 ,'annie': 42 , 'jan': 100}
#print counts.get('rim', 0) 

#the get automatically handles the case where a key is not in a dictionary. So we can reduce the code above to:

#word = 'brontosaurus'
#d = dict()
#for c in word:
#    d[c] = d.get(c,0) + 1 #d sub c equals d dot "get the value stored at c and if you don't find it, give me back a 0. And then, add 1 to that. Then take that sum and stick it in d sub c. "

#print d

#We will write a Python program to read through the lines of the file, break each 
#line into a list of words, and then loop through each of the words in the line and
#count each word using a dictionary.


#fhand = open('romeo.txt')
    
#counts = dict()
#for line in fhand:
#    words = line.split()
#    for word in words:
#        if word not in counts:
#            counts[word] = 1
#        else:
#            counts[word] += 1

#print counts # this output is inconvenient to look through. the following code should produce a better output. 

import string 

fhand = open("romeo_punctuation.txt")

counts = dict()
for line in fhand:
    line = line.translate(None, string.punctuation)
    line = line.lower()
    words = line.split()
    for word in words:
        counts[word] = counts.get(word,0) + 1
        #if word not in counts:
        #    counts[word] = 1
        #else:
        #    counts[word] += 1
print(counts)