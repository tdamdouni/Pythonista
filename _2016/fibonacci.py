from __future__ import print_function
# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci

print("Let's compute the first few terms in the Fibonacci sequence.")

n = 20 # How many terms shall we include?

###################################
# 1. An iterative method
###################################

# Iterative method, with values saved in a list
fiblist = [0,1]
for i in range(n - 1):
	fiblist.append(fiblist[i] + fiblist[i+1])
print(fiblist)


###################################
# 2. A recursive method
###################################
def fibRec(n):
	if n < 2:
		return n
	else:
		return fibRec(n-1) + fibRec(n-2)
print([fibRec(i) for i in range(n + 1)])


###################################
# 3. Using Binet's formula
###################################
def fibBinet(n):
	phi = (1 + 5**0.5)/2.0
	return int(round((phi**n - (1-phi)**n) / 5**0.5))
print([fibBinet(i) for i in range(n + 1)])

