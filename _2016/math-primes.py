# https://twitter.com/olikilo/status/814578663794606082

import math

primes = [2]
for pp in range(3,1000,2): # pp Potential prime
	md = math.floor(math.sqrt(pp)) # md Max Divider
	pdi = 0 # Potential Divider Index
	ip = True # ip is Prime
	while primes[pdi] <= md and ip:
		ip = (pp % primes[pdi] != 0)
		pdi = pdi + 1
	if ip:
		primes.append(pp)
print(primes)
print('Number of primes',len(primes))
