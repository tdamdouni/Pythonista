from __future__ import print_function
# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci

###################################
# Code from the Python tutorial: http://docs.python.org/2/tutorial/introduction.html#first-steps-towards-programming
###################################

# Fibonacci series:
# the sum of two elements defines the next
a, b = 0, 1
while b < 10:
	print(b)
	a, b = b, a+b

