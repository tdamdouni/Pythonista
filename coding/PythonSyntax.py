# -*- coding: utf -*-

# https://gist.github.com/TutorialDoctor/dda76e58fc43d7375856

from __future__ import print_function
intro = '''Remove tripple quotes around the sections to run the code therein\n'''
__version__ = "0.2"
__py_version__ = "2.7x"
print("Version: "+__version__+'\nPython: '+__py_version__+'\n')
print(intro)

def title1(name=''):
	print('\n' + name.upper() + ':')
	print('-'*65)
	
def title2(name=''):
	print('\n' + name.capitalize())
	print('-'*65)
	
def newline():
	print('')
#----------------------------------------------------------------------


# TABLE OF CONTENTS
#----------------------------------------------------------------------
# *** BEGINNER ***
"""
PRINTING
INPUT
OPERATORS
COMMENTS
VARIABLES
FUNCTIONS
CONDITIONALS
LOOPS
CLASSES
MODULES
"""

# *** INTERMEDIATE ***
"""
LIST COMPREHENSION
ARGUMENT PARAMETERS
KEYWORD ARGUMENTS
DOCSTRINGS
FILES
PARSING CSV FILES
DATA MODELS
"""

# *** ADVANCED ***
"""
Comming soon
"""

# *** POPULAR MODULES ***
"""
datetime
re
copy
pickle
os
socket
json
webbrowser
urllib
pydoc
lib2to3
timeit
"""

# *** EXAMPLES ***
"""
Comming soon
"""
#----------------------------------------------------------------------


print("\n*** Beginner code follows this line: ***\n")
# *** BEGINNER ***
# PRINTING
title1('printing')
#----------------------------------------------------------------------
"""
# Print a string
print "Hello World"

# Print multiple strings
print "Hello","World"

# Join/Concatenate two strings (gives errors if not strings)
print "Hello" + "World"

# Joining two strings with spaces
print "Hello" + " World"

# Printing numbers
print 27

# Another way to print (only way in python 3+)
print("Hello World")
#I've updated the print statements in this script for python 3 users

# Print an empty line (useful for separating code output)
print('')
"""
#----------------------------------------------------------------------


# INPUT
title1('input')
#----------------------------------------------------------------------
"""
# Get number input (works for words and numbers in python 3+)
input("How old are you ")

# Get word/string input
raw_input("What is your name ")
"""
#----------------------------------------------------------------------


# OPERATORS
title1('operators')
#----------------------------------------------------------------------
"""
# Adding
print(1+2)

# Subtracting
print(4-3)

# Multiplying
print(3*3)

# Dividing (not accurate if one of the terms isn't a decimal)
print(18/3)

# Remainder/Modulus
print(9%4)

# Power
print(2**8)

# Suare root
print(144**(1/2.0)) # must use at least one float

# Comparisons
print(2<4) #less than
print(4>9) #greather than
print(5==6) #is equal to
print(3==3)
print(4!=4) #not equal to
print(4!=9)
"""
#----------------------------------------------------------------------


# COMMENTS/NOTES
title1('comments')
#----------------------------------------------------------------------
"""A comment is a note for future or peer reference. The # symbol turns a line into a comment. Comments are not recognized as code, and are often used to disable bits of code. Tripple quotes are a multiline comment. They allow you to write comments that span multiple lines."""
#----------------------------------------------------------------------


# VARIABLES
title1('variables')
#----------------------------------------------------------------------
# Types
#----------------------------------------------------------------------
"""
# Character
at = "@"
print(at)

# String (wrapped in quotes)
name = "Raphael"
print(name)

# Integer (no quotes quotes)
age = 29
print(age)

# Float
height = 6.3
print(height)

# Boolean
is_cool = True
print(is_cool)

# List/Array
array = [] #an empty array
colors = ["red","orange","yellow","green","blue","indigo","violet"]
numbers = [0,1,2,3,4,5,6,7,8,9]
mixed_array  = [9,"alpha",63.3,True]
print(array,colors,numbers,mixed_array)

# Tuple
location = (0,0)
print(location)

# Dictionary
dictionary = {"key":"value"}
print(dictionary)

# Overwriting a variable
is_cool = False
name = "Tutorial Doctor"
age = 10585 #in days
height = 6.1
print(is_cool,name,age,height)

# Set a boolean to the opposite of itself
is_cool = not is_cool #False
print(is_cool)

# Casting (changing the type of a variable)
# To a float
age = float(age)
print(age)

# To an integer
height = int(height)
print(height)

# To a string
is_cool = str(is_cool)
print(is_cool)

# Other Casting functions
#bool() #To a boolean
#list() #To a list
#dict() #To a dictionary
#long() #To a long

# Printing the type of a variable
print(type(is_cool))
print(type(height),type(age),type(colors),type(dictionary))

# Python keywords cannot be used as variable names.
# Variable names can't start with a number
# Variable names can't start with special characters
# Use undrescores or camelcasing to separate parts of a variable name

# ID of a variable
print(id(name))

# Declaring multiple variables at once
a,s,l = 29,'Male','Georgia'
print(a)
print(s)
print(l)
print a,s,l

# Setting variables to same value at once
a=b=c = 45
print a,b,c

"""
#----------------------------------------------------------------------

# Strings
title2('strings')
#----------------------------------------------------------------------
"""
# Empty string (two ways)
first_name = ""
last_name = ''

# Assign value to a string
first_name = "Raphael"
last_name = "Smith"
occupation = "Programmer"

# Adding strings (concatenation)
print(first_name + last_name)

# Adding a space between string variables
print(first_name + " " + last_name)

# Starting a new line (escape characters)
print(first_name + "\n" + last_name)

# Escaping
message = "I\'m not old enough"
# The backslash escapes the apostrophe so it doesn't get inerpreted as a quote
print(message)

# String Formatting (adding variables inside of a string)
print("Hello %s %s") %(first_name,last_name) #string variables

# Number formatting
age = 29
print("I am %d years old") %(age) #digit variable
print("I am %3d years old")  %(age)
print("I am %03d years old") %(age) #leading zeros
print("I am %f years old") %(age) #float
print("I am %.2f years old") %(age) #truncate decimal places
print("I am %.6f yeras old") %(age) #truncate

# Another way to format
greeting = "My name is {} and I am {} years old".format(first_name,age)
print(greeting)

# Another way to use the format() function
greeting = "My name is {name} and I am {age} years old".format(name="Josiah",age=39)
print(greeting)

# Print a string several times
print(first_name*10)

# Get an index of a string (indices start at 0)
print(first_name[0]) #prints the fist item in the string
print(first_name[1]) #prints the second item

# Indexing backwards
print(first_name[-1]) #prints the last item in the string
print(first_name[-2]) #prints the second to last item in the string

# Multi-line String
sentence = '''Multi-Line strings are sometimes used as multi-line comments, since python doesn\'t have syntax for multi-line comments. They are usually used for long strings of text, and as docstrings (strings at the beginning of functions that are used for documenting what the function does)'''
print sentence

# More legal syntax
fourth_letter = "Python"[3]
print(fourth_letter)
#----------------------------------------------------------------------

# String Functions
#----------------------------------------------------------------------
# Capitalize
name = "raphael"
bio = "My name is {}, how are you today?".format(name)
print(name.capitalize())

# Uppercase
print(name.upper())

# Lowercase
print(name.lower())

# Length of string
print(len(name))

# Split a string into individidual words
bio_words = bio.split() # returns a list/array of the words
print(bio_words)

# Joining split words into a single string
empty_string = " "
joined_words = empty_string.join(bio_words)
print(joined_words)

# Mostly seen this way
joined_words_2 = " ".join(bio_words)
print(joined_words_2)

# You can use the above method to sort of add postifixes
joined_words_3 = "$ ".join(bio_words)
print(joined_words_3)

# Replace items in a string
sentence = 'Jello, how are you today?'
corection = sentence.replace('J','H')
print(corection)
"""
#----------------------------------------------------------------------

# Integers
title2('integers')
#----------------------------------------------------------------------
"""
timer = 0

# Increment (Add 1 to the time variable)
timer = timer + 1

# Another way
timer +=1
print(timer)

# Decrement (Subtract increment)
timer = timer - 1
# Or: time -=1
print(timer)

# Multiply increment
timer *= 4
print(timer)

# Divide Decrement
timer /= 2
print(timer)
"""
#----------------------------------------------------------------------

# Floats
title2('floats')
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------

# Lists
title2('lists')
#----------------------------------------------------------------------
"""
# Create a list
inventory = ["flashlight","map","knife","string"]
clothes = ["shirt","pants","shoes","bandana","hat"]

# Get index of a list (starts at 0)
print(inventory[0])

# Get last item in list
print(inventory[-1])

# List index range (starting at... up to...)
print(inventory[1:4]) # 2nd to the fourth item

# List index range (starting at...)
print(inventory[2:])

# List index range (up to...)
print(inventory[:4])
#----------------------------------------------------------------------

# List Functions
#----------------------------------------------------------------------
# Append to a list
inventory.append("rope")
print(inventory)
# Alternately:
# inventory[len(inventory):] = ["Joe"]

# Remove from a list
inventory.remove("knife")
print(inventory)

# Insert item at location
inventory.insert(0,"knife")
print(inventory)

# Reverse List
inventory.reverse()
print(inventory)

# Sort a List (alphabetical or numerical depending)
inventory.sort()
print(inventory)

# Remove an item at a location
inventory.pop(1)
print(inventory)

# Return the index of an item in the list
print(inventory.index("rope"))

# Extend a list with another list
inventory.extend(clothes)
print(inventory)
# Alternately:
# inventory[len(inventory):] = clothes

# Count how many times an item appears in a list
print(inventory.count("knife"))
print(inventory.count("rope"))

# Loop through a list
# Remove list from a list
"""
#----------------------------------------------------------------------

# Tuples (Immutable) can't update indicies
title2('tuples')
#----------------------------------------------------------------------
"""
x=0
y=0
position = (x,y)
"""
#----------------------------------------------------------------------

# Dictionaries
title2('dictionaries')
#----------------------------------------------------------------------
"""
# Create a dictionary: dictionary_name = {key:value}
# Empty dictionary
groceries = {"bread":"Nature's Own"}

# Print the value of a dictionary key
print(groceries["bread"])

# Update Dictionary
groceries.update({"milk":"whole"})
groceries.update({"meat":"ham"})
print(groceries)

# Update key if it is in the dictionary
groceries.update({"milk":"2%"})
print(groceries)

# Get all keys (returns a list)
print(groceries.keys())

# Get all values (returns a list)
print(groceries.values())

# Convert a dictonary to a list of tuples
print(groceries.items())

# Length of a dictionary
print(len(groceries))

# Delete dictionary key
del groceries['meat']
print(groceries)

# Iterate over a dictionary
print(iter(groceries))
print(groceries.iterkeys())
print(groceries.itervalues())

# Remove item, and return it's value
print(groceries.pop("bread"))
# Alternately:
# groceries.popitem()

# Display keys of a dictionary
print(groceries.viewkeys())

# Display values of a dictionary
print(groceries.viewvalues())

# Display items of a dictionary
print(groceries.viewitems())
"""
#----------------------------------------------------------------------

# Booleans: On and Off
title2('booleans')
#----------------------------------------------------------------------
"""
"Coming Soon"
"""
#----------------------------------------------------------------------


# FUNCTIONS: Actions  (WIP)
title1('functions')
#----------------------------------------------------------------------
"""
# Arguments & Parameters
#----------------------------------------------------------------------
# An argument is a variable that can be put into a function
# The things going in are called arguments, and the thing(s) they go into are the parameters
# a and b are the paremeters and 2 and 4 are the arguments.

def sum(a,b):
    print(a+b)
print(sum(2,4))
#----------------------------------------------------------------------

# Return
#----------------------------------------------------------------------
def product(a,b):
    return a*b
print(product(3,4))
#----------------------------------------------------------------------

# Lambda
#----------------------------------------------------------------------
x = lambda a,b: a+b
print(x(6,8))
#----------------------------------------------------------------------

# Local and Global Variables
#----------------------------------------------------------------------
world = 'BIG'
def change():
    # get the global variable
    global world
    # change it
    world = 'small'
# You have to all the function to chagne it.
change()
print(world)

# Argument Parameters (Spell check)
#----------------------------------------------------------------------
# Putting a star in front of the parameter allows a variable amount of arguments
def display(*x):
    print(x)
display(1,2,3,4,True,"Nothing")
#----------------------------------------------------------------------

# Keyword Arguments
#----------------------------------------------------------------------
# Pass variable amounts of key-value pairs to a function
def info(**information):
    return information
gathered_info=info(name="Tutorial Doctor",age=29,height=6.3,cool=True)
print gathered_info['name']
#----------------------------------------------------------------------

# Named Arguments (for clarity on input)
#----------------------------------------------------------------------
def Info(name='',age=0):
        return(name,age)

print(Info(age=45,name='Joe'))
#----------------------------------------------------------------------

# Generators
#----------------------------------------------------------------------
# A python generator is used to give a function return multiple values
def F():
    yield 1
    yield 2

f = F()

f.next()
print f.next()
#----------------------------------------------------------------------

# Built In
#----------------------------------------------------------------------
# Execute string as code
code = "print('Hello user...')"
exec(code)

#Execute a file in the directory of
#execfile('script.py') #file must exist of course, so create it

# Convert integer to a binary string
print(bin(64))
"""
#----------------------------------------------------------------------


# CONDITONALS: Logic/Control Flow
title1('conditionals')
#----------------------------------------------------------------------
# If, Else if(elif), and Else
title2('if, elif, else')
#----------------------------------------------------------------------
"""
age = 9
# 'if' something...
if age>=18:
        print('You are too old.')

# otherwise, if something else...
elif age<=7:
        print('You are too young.')

# if anything else...
else:
        print('You are the right age.')
# The elif statement is optional.
#----------------------------------------------------------------------

# Try, Except, and Finally: Error Checking
title2('try, except, finally')
#----------------------------------------------------------------------
# Try to do something, except if there is an error; do something else. Finally...
try:
        print(variable)
except:
        print('You have to define the variable first silly.')
        variable = 'a_no_longer_undefined_variable'
        print('Here, I fixed it for you:\n{}').format(variable)
finally:
        print('You have succesfully checked for errors using try and except')
# The variable is now defined, so we can print it
print(variable + '... is defined')
"""
#----------------------------------------------------------------------


# LOOPS: Repeating Instructions
title1('loops')
#----------------------------------------------------------------------

# While Loop: As long as...
title2('while loop')
#----------------------------------------------------------------------
"""
timer =0
while timer <10:
        print(timer)
        timer = timer + 1
"""
#----------------------------------------------------------------------

# For Loop: Until...
title2('for loop')
#----------------------------------------------------------------------
"""
for number in range(20):
        print(number)
newline()

for number in range(0,20,2):
        print(number)
newline()

name = 'Raphael'
for letter in name:
        print(letter)
newline()

number = 2929392
# The following for loop doesn't work
try:
        for digit in number:
                print digit
except:
        print("You can't loop through numbers")


items = ['gold','wood','ivory','wool']
inventory = {'weapon':'knife','light':'flashlight','navigation':'map'}

# Loop through each value in a list
for item in items:
        print(item)
newline()

# Loop through each key and it's index in a list
for item in items:
        print items.index(item),item
newline()

# Loop through each key in a dictionary
for eachthing in inventory:
        print(eachthing)
newline()

# Loop through each value in a dictionary
for eachthing in inventory:
        print(inventory[eachthing])
newline()

# Loop through each key and value in a dictionary
for eachthing in inventory:
        print(eachthing,inventory[eachthing])
newline()

# With numbers
numbers = [3,53,534,2253]
for number in numbers:
        print(number/2.0)

# A list comprehension is a for loop (comming up)
half=[number/2.0 for number in numbers]
print(half)
"""
#----------------------------------------------------------------------


# CLASSES
title1('classes')
#----------------------------------------------------------------------
"""
# Create a class
class Being(object):
        pass

# Create a class that inherits from another class
class Human(Being):
        pass

# Create a class with initial/default properties
class Girl(Human):
        def __init__(self):
                self.type = 'I am Girl'

class Boy(Human):
        def __init__(self):
                self.type = 'I am Boy'
# The __init__ function is built in
# self refers to the object itself (joe or sarah or...)

# Create an instance of a class
joe = Boy()
sarah = Girl()

# Giving instances properties (outside of the class)
joe.name = 'Joe'
joe.age = 17
print(joe.type) #this is that initial property we made inside the class

sarah.name = 'Saralee'
sarah.age= 7
print(sarah.type)

print(joe.name,joe.age)
print(sarah.name,sarah.age)

newline()

# Get the class of an instance
print(joe.__class__)

# Get the name of the class of an instance
print(sarah.__class__.__name__)

# Get the type of an object
print(type(joe))

# Get the base classes of a class (superclasses)
print(Boy.__bases__)

newline()

# Giving classes properties
Boy.sign = 'o->'
Girl.sign = 'o+'
print(joe.sign)
print(sarah.sign)

# Properties can be arrays
Human.types = [Boy,Girl]
print(Human.types)

# Properties can be dictionaries
Human.info = {'class':'Humanoidus-Strangus','extinct':False}
print(Human.info)

# Properties can be numbers
Human.age=0
print joe.age #prints 17, but 0 if joe.age wasn't already set by us.

# Super class of an object
None

# When it comes to classes inheritance, remember contrapositives.
#All A is B, but not all B is A

# more coming (methods)
"""
#----------------------------------------------------------------------


# MODULES
title1('modules')
#----------------------------------------------------------------------
"""
# Import a module
import math

# Using a module
radius= 3
Area = math.pi*radius**2
Circumference = 2*math.pi*radius
print(Circumference,Area)

# Custom
None

# To run the current script only if it is not from imported modules...
# Check if this script is the main script or not
if __name == '__main__':
        pass #function or code here
"""
#----------------------------------------------------------------------


print("\n*** Intermediate code follows this line: ***\n")
# *** INTERMEDIATE ***
# LIST COMPREHENSION
title1('list comprehension')
#----------------------------------------------------------------------
"""
numbers = [1,2,3,4,5,6,7,8,9]
squares = [x*x for x in numbers]
print(squares)
# Read as: squares equals x times x for every item x in numbers
# Alternately read as: for x in numbers, x equals x squared (set that to squares)

# More pythonic:
cubes = [number**3 for number in numbers]
print(cubes)

# With text
names = ["Python","Ruby","C","Javascript"]
prefixed_names = ["Language: " + name for name in names]
print(prefixed_names)
"""
#----------------------------------------------------------------------


# DOCSTRINGS
title1('docstrings')
#----------------------------------------------------------------------
"""
def display():
    # A doctstring is a string that documents what the function does
    "This function displays something"
print(display.__doc__)
"""
#----------------------------------------------------------------------


# FILES
title1('files')
#----------------------------------------------------------------------
"""
# Files work like notebooks

# It has to have a name
file_name = "notebook.txt"

# You have to open it
# If you want to write in it, you have to use the w mode
notebook = open(file_name,'w+')

# Then you write in it
notebook.write("Writing in my notebook")
# Writing something else into it
notebook.write(" again")

# When you are finished, you have to close it
notebook.close()

# Next time you want to open it for reading (r mode)
file_content=open(file_name,'r')

# Then you read it
print(file_content.read())

# The files are created in the same directory as the script

# Modes
WRITE = 'w'
READ = 'r'
APPEND = 'a'
READWRITE = 'w+'

# Another way (automatically closes the file and handles errors)
with open('spiral_notebook.txt',mode=WRITE) as spiral_notebook:
        spiral_notebook.write('This is my spiral notebook')

with open('spiral_notebook.txt',mode=READ) as spiral_notebook:
        print(spiral_notebook.read())
"""
#----------------------------------------------------------------------


# Wrappers and Decorators
title1('wrappers and decorators')
# A function that calls a function?
#----------------------------------------------------------------------
"""

"""
#----------------------------------------------------------------------


# DATA MODELS
title1('data models')
#----------------------------------------------------------------------
"""
class Coin(object):
        def __init__(self,val):
                self.value=val
        def __str__(self):
                return str(self.value)
        def __cmp__(self,other):
                return self.value #WIP (for comparisons)
        def __add__(self,other):
                return self.value+other.value
        def __mul__(self,other):
                return self.value*other.value
        def __div__(self,other):
                return self.value/other.value
        def __sub__(self,other):
                return self.value-other.value
        def __len__(self):
                return self.value
        def __contains__(self,item):
                pass #WIP (for in statement)
        def __call__(self):
                print('You called me?')
                print(self.__class__.__name__)

penny = Coin(1)
nickle = Coin(5)
dime = Coin(10)
quarter = Coin(25)

print(quarter-dime)
print(dime*nickle)
print(penny+quarter)
print(quarter/nickle)
penny()
print str(len(penny)) + ' is my value'
"""

# PARSING CSV FILES (WIP)
title1('parsing csv files')
#----------------------------------------------------------------------
"""
WRITE = 'w'
READ = 'r'
APPEND = 'a'
READWRITE = 'w+'

csv_notebook_name = "csv_notebook.csv"
csv_notebook = open(csv_notebook_name,mode=WRITE)
#Yeah you can do that
csv_notebook.write("name,Raphael,")
csv_notebook.write("age,29,")
csv_notebook.close()

content = open(csv_notebook_name,'r')
print(content.read())
"""
#----------------------------------------------------------------------

#----------------------------------------------------------------------


print("\n*** Advanced code follows this line: ***\n")
# *** ADVANCED ***
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------


print("\n*** Popular Modules code follows this line: ***\n")
# *** POPULAR MODULES ***
#----------------------------------------------------------------------
# Date and Time
title1('date and time')
# Remove clipboard and console import if you aren't using Pythonista
#----------------------------------------------------------------------
"""
import datetime,clipboard,console

time_stamp = datetime.datetime.today().strftime('%m_%d_%Y_%H_%M_%S')

# Pythonista(IOS) only:
#clipboard.set(time_stamp)
print('Timestamp added to clipboard ') + time_stamp

today = datetime.datetime.today()
print(today.month,today.day,today.year,today.hour,today.minute,today.second)

month = today.strftime('%B')
print(month)

day = today.strftime('%A')
print(day)

# Pythonista(IOS) only:
# console.hud_alert('Timestamp added to clipboard '+ time_stamp,duration=1)

#%b month abbreviation
#%B full month name
#%m two digit month
#%y two digit year
#%Y four digit year
#%a day of the week abbreviation
#%A day of the week
#%d date
#%M minutes
#%S two dogit seconds
#%H two digit hour
"""
#----------------------------------------------------------------------

# re: Pattern Matching
title1('pattern matching')
#----------------------------------------------------------------------
"""
import re
# Find all expressions/patterns in the email and print the matches
email = 'jacob&suzie#12@gmail.com'
expression = '^j.+'
matches = re.findall(expression,email)
print(matches)

# Find all extensions
extensions = '\.\w{3}'
extensions = re.findall(extensions,email)
print(extensions)

# Find all numbers
numbers = '\d+'
numbers = re.findall(numbers,email)
print(numbers)

# Find these symbols
symbols = '[@#&]'
symbols = re.findall(symbols,email)
print symbols
"""
#----------------------------------------------------------------------

# ZipFile: Compression
title1("ZipFile")
#----------------------------------------------------------------------
"""
from zipfile import ZipFile
# Zip files work lile regular files

#Modes
READ= 'r'
WRITE='w'
APPEND = 'a'
UNIVERSAL = 'U'
UNIVERSAL_READLINE = 'rU'

# We will put a notebook into a zipped backpack (the analogy)

# Write inside of the notebook
with open('Notebook.txt','w') as outfile:
        outfile.write('This is my language arts notebook')

# Write a file to a zip file
# Put the notebook in the backpack
with ZipFile('backpack.zip', 'w') as myzip:
        myzip.write('Notebook.txt')

# Extract all files in a zip file into another directory
# Take everything out of the backpack and put it on a desk
with ZipFile('backpack.zip') as mzip:
        mzip.extractall('Desk')

# Read a zip file
# Read something from the backpack
with ZipFile('backpack.zip','r') as mzip:
        print mzip.open('Notebook.txt','r').read()
"""
#----------------------------------------------------------------------

# copy: Copy Objects
title1('copy objects')
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------

# pickle:
title1('pickle')
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------

# os:
title1('operating system')
#----------------------------------------------------------------------
"""
import os

# Get current working directory (returns the path to the current folder)
print(os.getcwd())
this_directory=os.getcwd()

# Create a directory/folder in a path
try:
        new_directory = os.mkdir(this_directory+'/New Folder')
        print('Directory created.')
except:
        print('Directory already exists.')

# Create multiple directories
try:
        os.makedirs(this_directory+'/Folder1/Folder2/Folder3')
        print('Directories created.')
except:
        print('Those directories already exist.')

# Change the current directory/folder to a path
#os.chdir() ?

# Remove a directory
#os.rmdir(path) ?

# Move up or down a path
# print os.walk() ?

# directory of a file

#Remove path
# os.remove()
# os.remove(new_directory+'/a.txt')
"""
#----------------------------------------------------------------------

# socket:
title1('socket')
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------

# json:
title1('json')
#----------------------------------------------------------------------
"""
import json
"""
#----------------------------------------------------------------------

# webbrowser:
title1('web browser')
#----------------------------------------------------------------------
"""
import webbrowser
url = 'editorial://open/new.txt'
webbrowser.open(url)
"""
#----------------------------------------------------------------------

# urllib:
title1('urllib')
#----------------------------------------------------------------------
"""
import urllib
"""
#----------------------------------------------------------------------

# pydoc:
title1('pydoc')
#----------------------------------------------------------------------
"""
import pydoc
# Locate path to a library
print(pydoc.locate('urllib'))

# Print/render documentation on a module
print(pydoc.render_doc('str'))

# Import a module
print(pydoc.importfile('lambda.py'))

# Turn documentation on a module into html
# File stored in directory of the script
print(pydoc.writedoc('str'))

# more uses coming...
"""
#----------------------------------------------------------------------

# lib2to3
title1('python 2 to 3')
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------

# timeit
title1('time it')
#----------------------------------------------------------------------
"""
# Time small bits of code (execution time)
import timeit
code = "print('Hello World')"
print timeit.timeit(code,number=1)
# takes about .033 seconds on average

# Time a Custom function
def add(a,b):
        print a+b

print(timeit.timeit("add(2,4)", setup="from __main__ import add",number=1))
"""


# Tokenize
title1('tokenize')
#----------------------------------------------------------------------
"""
# Tokenization is the task of chopping a sequence up into pieces, called tokens. You can tokenize a string. The split() function tokenized strings. Tokens arent repeated.

word = 'red/blue'
split_word = word.split('/') # / is the delimiter
# A delimiter is a boundary between parts(usually punctuation)
print(split_word)

word2 = "brother's"
split_word_2 = word2.split("'")
print(split_word_2)

import tokenize
"""
#----------------------------------------------------------------------


print("\n*** Example code follows this line: ***\n")
# *** EXAMPLES ***
#----------------------------------------------------------------------
None
#----------------------------------------------------------------------

