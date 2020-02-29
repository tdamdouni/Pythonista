from __future__ import print_function
#Exercise 9.1 Write a program that reads the words in words.txt.
#Stores them as keys in a dictionary. It does not matter what the values are. 
#Then you can use the in operator as a fast way to check whether a string is in the dictionary

my_dictionary = dict()
fhand = open('words.txt')
#inp = fhand.read()

for line in fhand:
    words = line.split()
    for word in words:
        my_dictionary[word] = 1

print(my_dictionary.keys())
