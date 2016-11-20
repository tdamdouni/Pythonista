#!/usr/bin/env python
# Written by: DGC

import math
import time

class Prime(object):
	def __init__(self):
		self.primes = [2]
		
	def _test(self, possible_prime):
		"""Test if any elements of primes divides possible_prime."""
		prime = True
		for i in self.primes:
			if (i > math.sqrt(possible_prime)):
				break
			if (possible_prime % i) == 0:
				prime = False
				break
		if (prime):
			self.primes.append(possible_prime)
			
	def primes_below(self, limit):
		"""Return a list of primes below the input argument."""
		i = self.primes[len(self.primes) - 1]
		if (i == 2):
			i += 1
		else:
			i +=2
		while i <= limit:
			self._test(i)
			i += 2
		return self.primes
		
	def primes_number_of(self, limit):
		"""Returns the number  of primes below the input argument."""
		i = self.primes[len(self.primes) - 1]
		if (i == 2):
			i += 1
		else:
			i +=2
		while len(self.primes) < limit:
			self._test(i)
			i += 2
		return self.primes
		
# if this is run as a program.
if __name__ == "__main__":
	type = -1
	while (type != 0 and type != 1):
		question = "Do you want number of primes [0]"
		question += ", primes below a number[1]?\n"
		type = input(question)
	limit = 1
	print("")
	if (type == 0):
		limit = input("How many primes do you want?\n")
	else:
		limit = input("Primes (inclusivly) below what number?\n")
	t_start = time.time()
	calculator = Prime()
	if (type == 0):
		primes = calculator.primes_number_of(limit)
		end_calc = time.time()
		msg = "\n"
		if (limit < 1000):
			msg += "The first " + str(limit) + " primes are:\n" + str(primes) + "\n"
		msg += "The " + str(limit) + "th primes is: " + str(primes[-1])
		print(msg)
	else:
		if (type == 1):
			primes = calculator.primes_below(limit)
		else:
			assert(False)
		end_calc = time.time()
		msg = "\n"
		if (limit < 1000):
			msg += "The primes below " + str(limit) + " are:\n" + str(primes) + "\n"
		msg += "There are " + str(len(primes)) + " primes below " + str(limit)
		msg += "\nThe largest of which is: " + str(primes[-1])
		print(msg)
	print("\nCalculation time:"),
	print(str(end_calc-t_start))

