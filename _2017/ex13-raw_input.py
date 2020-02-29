from __future__ import print_function
# https://github.com/mwarkentin/Learn-Python-The-Hard-Way/blob/master/ex13-raw_input.py

# https://forum.omz-software.com/topic/4034/simple-ui-to-run-script2-args/5

from sys import argv

try:  # https://docs.python.org/3/whatsnew/3.0.html#builtins
    raw_input          # Python 2
except NameError:
    raw_input = input  # Python 3

script, first_name, last_name = argv

middle_name = raw_input("What is your middle name? ")

print("Your full name is %s %s %s." % (first_name, middle_name, last_name))

# https://forum.omz-software.com/topic/4034/simple-ui-to-run-script2-args/5

from sys import argv

script2 = argv

first_name = raw_input("What is your first name? ")

middle_name = raw_input("What is your middle name? ")

last_name = raw_input("What is your last name? ")

print("Your full name is %s %s %s." % (first_name, middle_name, last_name))
