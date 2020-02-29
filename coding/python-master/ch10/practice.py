from __future__ import print_function
#Suppose you have a list of words and 
#you want to sort them from longest to shortest:

txt = 'but soft what light in yonder window breaks'

words = txt.split()

t = list()


for word in words:
    t.append((len(word), word)) #this builds a list of tuples. Each tuple is a word preceded by its length e.g. (3, 'but')
    
print(t)                         #this is what our list of tuples looks like prior to sorting.    

t.sort(reverse=True)            #the sort() method on a list sorts that list into ascending order, but since we uesd the
                                #arguement reverse=True, it's sorted in decreasing order. Sort compares the first element 
                                #of each tuple (which is the 3 in the tuple (3, 'but')) -- it only considers the second
                                #element to break ties that may occur when comparing the first elements. 
print(t)

res = list()                    #this creates another list. 
for length, word in t:          #this loop traverses the list of tuples. 
    res.append(word)            #we append each word to our list.
    
print(res)                       #the result is a list, sorted in descending word length order. 

#the above is an example of the (DSU) Decorate, Sory and Undecorate pattern. 
#Decorate a sequence by building a list of tuples with one or more sort keys preceding the elements from the sequence
#Sort the list of tuples using the sort built in method
#Undecorate by extracting the sorted elements of the sequence. 

#Tuple assignment

#You can have a tuple on the left side of an assignment statement, allowing you to assign more than one variable
#at a time when the left side is a sequence. 

#Here is a two element list. 

m = ['have', 'fun']

#We assign the first and second elements to the variables x and y.

x, y = m

print(x)
print(y)

#Essentially x = m[0] and y = m[1]
#We can swap values in a single statement 

x, y = y, x 

print(x)
print(y)

#both sides of this statement are tuples, but the left side is a tuple of variables
#the right side is a tuple of expressions. Each value on the right side is assigned 
#to its respective variable on the left side.The expressions on the right are evaluated first. 
#Note, the number of variables on the right side must be the same on the left. 

#the right side can be any kind of sequesnce.

addr = 'monty@python.org'
uname, domain = addr.split('@') #the right side is a list with two elements, monty and python.org

print(uname)
print(domain)

#Dictionaries and Tuples

#Dictionaries have a method called items that returns a list of tuples, 
#where each tuple is a key value pair. The items are in no particular order.

d = {'a':10, 'b':1, 'c':22}
t = d.items()

print(t)

#Since t is a list of tuples, and tuples are comparable, we can 
#sort the list of tuples. Converting a dictionary to a list of tuples
#is a way for us to output the contenet of a dictionary  sorted by key.

t.sort()

print(t)

#This new list is in ascending alphapetical order by the key value (letter a, b and c). 

#Multiple assignment with dictionaries

#You can traverse keys and values of a dictionary with a single loop
#using items, tuple assignment and for.

for key, val in d.items():
    print(val, key)

#this loop has two iteration variables, key and val, because items returns a list of tuples
#Key and val successively iterate through each of the key value pairs in the dictionary. 
#note that the output is hash key orger (e.g. in no particular order.)

d = {'a':10, 'b':1, 'c':22} #here is a list of tuples, sorted by value and key.

l = list()

for key,val in d.items(): #items method gives us a list of key and value tuples. 
                          #For each key and value in our key, value list of tuples
                          #append the value and the key to our new list called l.
    l.append((val, key))
    
print(l)

l.sort(reverse=True)

print(l)

#The most common word practice

import string 
fhand = open('romeo-full.txt')
counts = dict()
for line in fhand:
    line = line.translate(None, string.punctuation) #we use translate to remove all punctuation.
    line = line.lower()                             #we use lower to force the line to lowercase.
    words = line.split()
    for word in words:
        if word not in counts:
            counts[word] = 1
        else:
            counts[word] += 1

#sort the dictionary by value

lst = list()
for key, val in counts.items():
    lst.append((val, key))

lst.sort(reverse=True)

print(lst[:10]) #this is a list of the most common words in romeo-full.txt. 
                #but we are looking at just the ten most common words.

for key, val in lst[:10]: 
    print(key, val)
    
#using tuples as keys in dictionaries

#Remember: The in operator uses different algorithms for lists and dictionaries. 
#For lists, it uses a linear search algorithm. As the list gets londer, the search 
#time gets longer in direct proportion to the length of the list. For dictionaries, 
#python uses an algorithm called a hash table where the in operator takes the same 
#amount of time no matter how many items there are in a dictionary. 

#Imagine we need to create a telephone directory, that maps from last-name, first-name
#pairs to telephone numbers.

first = "alicia"
last = "barrett"
number = "100-123-4567"
directory = dict()

directory[last, first] = number

#the expression in the bracket is a tuple.

for last, first in directory:
    print(first, last, directory[last, first])

#this loop traverses the keys in the directory, which are tuples. 
#it assigns the elements of each tuple to last and first, then prints 
#the name and corresponding telephone number.