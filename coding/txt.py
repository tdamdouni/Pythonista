# coding: utf-8
# https://forum.omz-software.com/topic/2373/how-to-call-a-text-file-from-my-ipad-to-pythonista-script
# Script to print lines using functions

from __future__ import print_function
from sys import argv

script, input = argv

def print_all(f):
	print(f.read())

def rewind(f):
	f.seek(0)

def print_a_line(line_count, f):
	print(line_count, f.readline())

current_file = open(input)

print("First lets print the whole file:\n")
print_all(current_file)

print("Now lets rewind the file like tape")
rewind(current_file)

print("Lets print three Lines")
current_count = 1
print_a_line(current_count, current_file)
current_count = current_count + 1
print_a_line(current_count, current_file)
current_count = current_count + 1
print_a_line(current_count, current_file)

# END

# On my linux system I use:-
# $ python script-name file-name