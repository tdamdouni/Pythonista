# https://forum.omz-software.com/topic/3579/pythonista-is-telling-my-input-is-not-defined/2

name = input("what is your name? ")
age = int(input("what is your age?"))

if (age >= 18) and (age < 90):
	print("You can vape {}" .format(name))
if age > 90:
	print("{} vaping is not recommended" .format(name))
else:
	print("wait {} years" .format(18 - age))
# --------------------
# coding: utf-8

try:
	raw_input
	input = raw_input  # Python 2
except NameError:      # Python 3
	pass
	
name = input("What is your name? ").strip()
age = int(input("What is your age? "))

if 18 <= age < 90:
	print("You can vape {}." .format(name))
if age >= 90:
	print("{} vaping is not recommended." .format(name))
else:
	print("Wait {} years." .format(18 - age))
# --------------------

