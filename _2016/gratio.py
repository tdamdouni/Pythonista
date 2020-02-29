from __future__ import print_function
print("Let's compute the first few terms in the Fibonacci sequence.")

n = 30 # How many terms shall we include?

###################################
# 1. Compute the Golden Ratio
###################################

# Iterative method, with values saved in a list
fiblist = [0,1]
for i in range(n - 1):
	fiblist.append(fiblist[i] + fiblist[i+1])
print(fiblist)

gratio = [fiblist[i]/float(fiblist[i-1]) for i in range(2,len(fiblist))]
print(gratio)

