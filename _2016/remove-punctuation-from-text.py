# https://forum.omz-software.com/topic/3897/set-error-while-attempting-to-remove-punctuation

# attempt 1

import string
input_file = open("Test1.txt", "r") #Open the file 'Test1'
input_file = input_file.read() #Convert the file to a string
input_file = input_file.translate({None for a in string.punctuation}) #Attempt to remove punctuation. 
#The error is thrown by the above line
input_file.translate({ord(x):None for x in string.punctuation})

# attempt 2

import string

with open("Test1.txt", "r") as in_file:
	s = in_file.read()
print(s)
s = ''.join(' ' if c in string.punctuation else c for c in s)
print(s)

