#! /usr/bin/env python

#       Kristi Short
#       Math 180 Numerical Analysis
#       Fall 2014
#       Square Root Approximation
#       Pythonista Version

from __future__ import print_function
import math
#import matplotlib.pyplot as plt


#   new graphic
#plt.figure()




#       prompt user for radicand
n = float(raw_input("Please enter an integer value for the radicand: "))
toleranceVal = float(raw_input("Please enter a positive integer value for the power of the tolerance: "))

#   tolerance = 19^(1toleranceVal)
tolerance = math.pow(10, -toleranceVal)

#   for error calculation
sqRt = math.sqrt(n)

#   variable to keep the value of the error
err = 0

#   global itr variable
itr = 0

#   blah blah
print("Note: Computer memory is system dependent, floats are limited in accuracy. So unless you are running something seriously badass dont ask for a tolerance value larger than 6 or so.")

print("Note: Should you need to have a degree of accuracy larger (but the still retain the same computer) try the bigfloat lib, (watch out, its kind of icky).")

#   function finds square root of n (user input) to the requested degree of accuracy.
def findRoot(n, tolerance):
	itr = 0
	with open('SquareRootAprxData.csv', 'w') as f:
		f.write('#itr,floor, celing, prevMid, mid, root\n')
		sqRt = math.sqrt(n)
		root = 0    #   Dummy var for illustrative purposes
		floor = 0
		ceiling = n
		mid = n
		prevMid = -1
		err = 0
		while (math.fabs(mid - prevMid) >= tolerance):
			f.write('{0},{1},{2},{3},{4}\n'.format(itr,floor,ceiling,prevMid,mid, root))
			
			prevMid = mid
			mid = float((floor+ceiling)/2)
			root = mid  #   Do not need this variable to be here at all this is simply to make the algorithms structure transparent. In line 61 we output mid from this function and declare it root.
			if mid**2 > n:
				ceiling = mid
				root = mid
			else:
				floor = mid
				root = mid
			itr = itr + 1
	return root
	
root = findRoot(n, tolerance)   #   The Root!

err = math.fabs(root - sqRt)    #   The Error!

#   Blah Blah
print("The approximated root of " + str(n) + " is " + str(root))
print("The error in Approximation is: " + str(err))

#   create scatter plot
#plt.subplot(236)

#plt.scatter(itr, root)

#   plot it!
#plt.show()

