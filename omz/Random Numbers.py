# Lottery Number Generator

from random import choice
import console

#Helper function to input a number within a given range:
def input_number(prompt, min_value, max_value):
	value = None
	while value is None:
		try:
			value = int(raw_input(prompt))
		except ValueError:
			print 'Please enter a number!'
		if value < min_value or value > max_value:
			print ('Please enter a number between %i and %i!' % 
			       (min_value, max_value))
			value = None
	return value

#Print the title and input the range of numbers:
console.clear()
title = 'Lottery Number Generator'
print title
print '=' * 40
minimum = input_number('Smallest number: ', 1, 9999)
maximum = input_number('Largest number: ', minimum, 9999)
n = input_number('How many numbers do you want to draw? ', 
                 1, maximum - minimum + 1)

#Pick the numbers and print the results:
all_numbers = range(minimum, maximum + 1)
selection = []
for i in xrange(n):
	r = choice(all_numbers)
	selection.append(r)
	all_numbers.remove(r)
print '=' * 40
print 'Your numbers:', selection
