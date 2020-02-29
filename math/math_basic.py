from __future__ import print_function
# Don't you just love math, expecially when the computer does it for you? You can do [basic math](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/math_basic.py) in python

# Get the sum of two numbers a and b
def sum(a,b):
	return a+b
	
# Get the difference of two numbers a and b
def difference(a,b):
	return a-b
	
# Get the quotient of two numbers a and b where b cannot equal 0
# You have to use a float somewhere in your dividion so that the answer comes out as a float
# A float is a number with a decimal
def quotient(a,b):
	if b != 0:
		return a/float(b)
		
# Get the product of two numbers:
def product(a,b):
	return a*b
	
# That's it for basic math in a computer program!
# No cheating on your homework! Hehe ;)

print(quotient(2232,2322))
print(product(23.134,132.34))
print(sum(2314,46426))
print(difference(8,3546456345))

