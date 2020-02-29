from __future__ import print_function
# Demo of how to generate a list of prime numbers and cache them
# in a data file for fast access (using the marshal module).

def gen_primes(n):
	# Source: http://code.activestate.com/recipes/366178-a-fast-prime-number-list-generator/#c19
	s = range(0, n+1)
	s[1] = 0
	bottom = 2
	top = n // bottom
	while (bottom * bottom <= n):
		while (bottom <= top):
			if s[top]:
				s[top * bottom] = 0
			top -= 1
		bottom += 1
		top = n // bottom
	return [x for x in s if x]
	
def load_primes(n):
	import marshal
	filename = 'primes_' + str(n)
	try:
		# Load cached primes file:
		with open(filename, 'r') as f:
			return marshal.load(f)
	except:
		# Generate primes and save to file:
		primes_list = gen_primes(n)
		with open(filename, 'w') as f:
			marshal.dump(primes_list, f)
			return primes_list
			
def main():
	primes = load_primes(104729) #Happens to be the 10,000th prime number
	print(primes)
	print(len(primes), 'prime numbers loaded.')
	
if __name__ == '__main__':
	main()

